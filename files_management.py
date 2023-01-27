from PIL import Image
import time
import glob
import os

QR_MAX_WIDTH  = 300
QR_MAX_HEIGHT = 300
IMAGES_DIR         = "static/images/"
MAX_IMAGES_TO_KEEP = 5


# Saving the image to the static folder.
def save_static_image(img):
    img.resize((QR_MAX_WIDTH, QR_MAX_HEIGHT), Image.ANTIALIAS)
    timestamp = int(time.time())
    img.save(f'{IMAGES_DIR}generated_qr_{timestamp}.png')
    time.sleep(1)
    keep_latest_images()


# Removing the old images from the static folder.
def keep_latest_images():
    files = os.listdir(IMAGES_DIR)
    files_to_keep = files[-MAX_IMAGES_TO_KEEP:] if len(files) > MAX_IMAGES_TO_KEEP else files
    files_to_remove = set(files) - set(files_to_keep)
    for file in files_to_remove:
        os.remove(os.path.join(IMAGES_DIR, file))


# Getting the latest image from the static folder.
def get_image_path():
    file = glob.glob(f'{IMAGES_DIR}generated_qr_*.png')[-1]
    return file


# Getting the name of the image.
def get_image_name():
    return get_image_path().split('\\')[-1]
