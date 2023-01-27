from flask import Flask, request, render_template, send_file, send_from_directory
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode

from files_management import *

app = Flask(__name__)


"""
This function takes a URL from a form, creates a QR code image from it, and saves the image to a static folder
:return: The index function is being returned.
"""
@app.route("/", methods=['GET', 'POST'])
def index():
    url = ""
    if request.method == 'POST':
        url = request.form['qr_content']
        img = qrcode.make(url)
        save_static_image(img)
    return render_template('index.html', url=url)


"""
This function takes a QR code image, decodes it, saves the image to a static folder, and returns the decoded data
:return: The return value is the barcode data.
"""
@app.route('/generate_url', methods=['POST'])
def generate_url():
    file = request.files['qr_file']
    img = Image.open(file)
    barcodes = decode(img)
    barcode_data = barcodes[0].data
    save_static_image(img)
    return render_template('index.html', url=barcode_data.decode())


"""
This function takes a URL from the form, generates a QR code image, and saves it to the static folder
:return: Nothing is being returned.
"""
@app.route('/generate_qrcode', methods=['POST'])
def generate_qrcode():
    url = request.form['qr_content']
    img = qrcode.make(url)
    save_static_image(img)
    return render_template('index.html', url=url)


"""
This function takes a URL, and returns a QR code image
"""
@app.route("/update_qr_image")
def update_qr_image():
    return send_file(get_image_path(), mimetype='image/png')


"""
    This function takes a string, and returns a string
    :return: the filename of the image.
"""
@app.route('/download_qrcode', methods=['POST'])
def download_qrcode():
    filename = get_image_name()
    return send_from_directory(IMAGES_DIR, filename, as_attachment=True)


if __name__ == '__main__':
    app.run()
