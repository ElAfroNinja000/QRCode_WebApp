from flask import Flask, request, render_template, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    url = request.form['url']
    img = qrcode.make(url)
    bio = BytesIO()
    img.save(bio, format='png')
    bio.seek(0)
    return send_file(bio, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
