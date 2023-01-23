from flask import Flask, Response, request, render_template, send_file, jsonify
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
from io import BytesIO

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_url', methods=['POST'])
def generate_url():
    file = request.files['qr_file']
    image = Image.open(file)
    barcodes = decode(image)
    for barcode in barcodes:
        (barcode_data, barcode_type) = barcode.data, barcode.type
        return render_template('index.html', qr_content=barcode_data.decode())
    return render_template('index.html', qr_content={"error": "No QR code found in the image"})


@app.route('/generate_qrcode', methods=['POST'])
def generate_qrcode():

    url = request.form['text_qr_content']
    img = qrcode.make(url)
    bio = BytesIO()
    bio.seek(0)
    response = Response(content_type="image/jpeg")
    img.save(bio, format='jpeg')
    response.headers["Content-Disposition"] = "attachment; filename=image.jpg"
    #return send_file(bio, mimetype='image/png')
    return response


if __name__ == '__main__':
    app.run(debug=True)
