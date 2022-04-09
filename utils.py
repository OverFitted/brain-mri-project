from config import *


def batch_splitter(iterable, batch_size):
    iterable_length = len(iterable)

    for i in range(0, iterable_length, batch_size):
        yield iterable[i:min(i + batch_size, iterable_length)]


def save_results(files):
    for i, file in enumerate(files):
        model.show_result(files[i], results[i], out_file=os.path.join(RESULT_FOLDER, f"{i}.jpg"), score_thr=THRESHOLD)  # Saving segmented image
        result = ", ".join([f"{cat} ({round(res[0][-1], 2)})" for res, cat in zip(results[i][0], CATEGORIES) if res.any() and res[0][-1] > THRESHOLD])

        with io.open(os.path.join(RESULT_FOLDER, f"{i}.txt"), "w", encoding="UTF-8") as result_file:
            result_file.write(result)


def delete_temp_files(files, archive_path):
    for i, file in enumerate(files):
        os.remove(file)
        os.remove(os.path.join(RESULT_FOLDER, f"{i}.txt"))
        os.remove(os.path.join(RESULT_FOLDER, f"{i}.jpg"))

    os.remove(archive_path)


def allowed_file(filename):
    return any([extension in filename for extension in ALLOWED_EXTENSIONS])
