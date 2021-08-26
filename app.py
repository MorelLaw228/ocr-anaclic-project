#!/usr/bin/python3

from flask import *
import os
from werkzeug import secure_filename
import cv2
from PIL import Image
import numpy as np
from skimage.filters import threshold_local
import ultim


app = Flask(__name__)


def preprocess_image():
    return "Image Preprocessing end .............."


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpeg','jpg','png']

@app.route('/uploadImageOCR',methods=['POST'])
def upload_image():
    try:
        file_names = []
        curr_path = os.getcwd()
        files_in_dir = os.listdir()
        for file in files_in_dir:
            if file[0] != '.' and file[0] != '_':
                if file not in ['static', 'templates', 'app.py', 'Procfile', 'requirements.txt']:
                    os.remove(file)
        uploaded_files = request.files.getlist("files")
        for file in uploaded_files:
            if allowed_file(file.filename):
                file.filename = secure_filename(file.filename)
                file_names.insert(0, file.filename)
                file.save(file.filename)
        preprocess_image()
        try:
            return send_from_directory(os.getcwd(), 'resultat_OCR.txt', as_attachment=True)
        except Exception:
            abort(404)
    except Exception:
        return render_template("imagetotext.html")




@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/ocr')
def ocr_imagetotext():
    return render_template('imagetotext.html')

if __name__ =='__main__':
    app.run(debug=True)