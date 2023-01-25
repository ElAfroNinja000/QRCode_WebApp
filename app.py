from flask import Flask, Response, request, render_template, send_file, jsonify
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode

app = Flask(__name__)


@app.route('/generate_url', methods=['POST'])
def generate_url():
    file = request.files['qr_file']
    image = Image.open(file)
    barcodes = decode(image)
    for barcode in barcodes:
        barcode_data = barcode.data
        print(type(barcode_data.decode()))
        return render_template('index.html', url=barcode_data.decode())
    return render_template('index.html', url={"error": "No QR code found in the image"})


@app.route("/", methods=['GET', 'POST'])
def index():
    url = ""
    if request.method == 'POST':
        max_width  = 250
        max_height = 250
        url = request.form['qr_content']
        img = qrcode.make(url)
        img.resize((max_width, max_height), Image.ANTIALIAS)
        img.save('static/generated_qr.png')
    return render_template('index.html', url=url)


@app.route("/qr_code")

def qr_code():
    return send_file('static/generated_qr.png', mimetype='image/png', cache_timeout=3600)


@app.route('/download_qrcode', methods=['POST'])
def download_qrcode():
    response = Response(content_type="image/png")
    response.headers["Content-Disposition"] = "attachment; filename=qr_code.png"
    return response


if __name__ == '__main__':
    app.run(debug=True)
