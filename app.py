from flask import Flask, Response, request, render_template, send_file, jsonify
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
import time
import glob

QR_MAX_WIDTH  = 250
QR_MAX_HEIGHT = 250

app = Flask(__name__)


@app.route('/generate_url', methods=['POST'])
def generate_url():
    file = request.files['qr_file']
    image = Image.open(file)
    barcodes = decode(image)
    barcode_data = barcodes[0].data
    return render_template('index.html', url=barcode_data.decode())
    return render_template('index.html', url={"error": "No QR code found in the image"})


@app.route("/", methods=['GET', 'POST'])
def index():
    url = ""
    if request.method == 'POST':
        url = request.form['qr_content']
        img = qrcode.make(url)
        img.resize((QR_MAX_WIDTH, QR_MAX_HEIGHT), Image.ANTIALIAS)
        timestamp = int(time.time())
        img.save(f'static/generated_qr_{timestamp}.png')
    return render_template('index.html', url=url)


@app.route("/qr_code")
def qr_code():
    print("HELLO")
    image_path = glob.glob('static/generated_qr_*.png')[0]
    print(image_path)
    return send_file(image_path, mimetype='image/png', cache_timeout=3600)


@app.route('/download_qrcode', methods=['POST'])
def download_qrcode():
    response = Response(content_type="image/png")
    response.headers["Content-Disposition"] = "attachment; filename=qr_code.png"
    return response


if __name__ == '__main__':
    app.run(debug=True)
