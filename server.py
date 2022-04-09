import io
import mmcv
import os
import shutil
import zipfile

from flask import Flask, flash, request, redirect, send_file
from glob import glob
from mmdet.apis import init_detector, inference_detector
from tqdm import tqdm
from utils import *
from werkzeug.utils import secure_filename


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if SERVER_FILE_PATH not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files[SERVER_FILE_PATH]
        if file and file.filename and allowed_file(file.filename):
            archive_filename = secure_filename(file.filename)
            archive_path = os.path.join(UPLOAD_FOLDER, archive_filename)
            file.save(archive_path)
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(TEMP_FOLDER)

            files = []
            for filetype in ALLOWED_IMG_EXTENSIONS:
                files.extend(glob(os.path.join(TEMP_FOLDER, f"*.{filetype}")))

            files.sort(key=lambda x: int(os.path.split(x)[-1].split(".")[0]))

            results = []
            for files_batch in batch_splitter(files, BATCH_SIZE):
                results.extend(inference_detector(model, files_batch))

        save_results(files)
        shutil.make_archive("result", 'zip', RESULT_FOLDER)
        delete_temp_files(files, archive_path)

        return send_file("result.zip", mimetype='application/zip')
    else:
        return "POST your image sequences"


if __name__ == "__main__":
    model = init_detector(CONFIG, CHECKPOINT, device=DEVICE)

    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = SECRET_KEY
    app.config['SESSION_TYPE'] = SESSION_TYPE

    app.run(port=PORT)
