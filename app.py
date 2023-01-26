from flask import Flask, request, render_template, send_file, send_from_directory
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
import time
import glob

QR_MAX_WIDTH  = 300
QR_MAX_HEIGHT = 300

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    url = ""
    if request.method == 'POST':
        url = request.form['qr_content']
        print(url)
        img = qrcode.make(url)
        save_static_image(img)
    return render_template('index.html', url=url)


@app.route('/generate_url', methods=['POST'])
def generate_url():
    file = request.files['qr_file']
    img = Image.open(file)
    barcodes = decode(img)
    barcode_data = barcodes[0].data
    save_static_image(img)
    return render_template('index.html', url=barcode_data.decode())


@app.route('/generate_qrcode', methods=['POST'])
def generate_qrcode():
    url = request.form['qr_content']
    img = qrcode.make(url)
    save_static_image(img)
    return render_template('index.html', url=url)


@app.route("/qr_code")
def qr_code():
    return send_file(get_image_path(), mimetype='image/png')


@app.route('/download_qrcode')
def download_qrcode():
    filename = get_image_name()
    return send_from_directory(app.static_folder, filename, as_attachment=True)


def save_static_image(img):
    img.resize((QR_MAX_WIDTH, QR_MAX_HEIGHT), Image.ANTIALIAS)
    timestamp = int(time.time())
    img.save(f'static/generated_qr_{timestamp}.png')


def get_image_path():
    return glob.glob('static/generated_qr_*.png')[-1]


def get_image_name():
    return get_image_path().split('\\')[-1]


if __name__ == '__main__':
    app.run(debug=True)
