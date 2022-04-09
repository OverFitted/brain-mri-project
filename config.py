CONFIG = 'configs/mask_rcnn_regnetx-3.2GF_fpn_mstrain_3x_coco.py'
CHECKPOINT = 'checkpoints/latest.pth'
BATCH_SIZE = 6
DEVICE = "cuda:0"

TEMP_FOLDER = "temp"
UPLOAD_FOLDER = 'out'
RESULT_FOLDER = 'result'
ALLOWED_EXTENSIONS = set(['zip', 'rar', '7z'])
ALLOWED_IMG_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

CATEGORIES = ["Менингиома", "Глиома", "Опухоль гипофиза"]
THRESHOLD = .8

SECRET_KEY = "B1BB7B836CFA2600E09DAE1243DD4ECCA7F23E55"
SESSION_TYPE = "filesystem"
SERVER_FILE_PATH = "upload_file"
PORT = 3350