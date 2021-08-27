#!/usr/bin/python3
import time

import cv2
import pytesseract
from flask import *
import os
from werkzeug.utils import secure_filename
#import cv2
from PIL import Image
import numpy as np
#import ultim
import imghdr
import numpy as np
import re
from statistics import mode


# ======================================================================================== #
#   Threshold Methods                                                                      #
# ======================================================================================== #
# 1. Binary-Otsu w/ Gaussian Blur (kernel size = 9)                                        #
# 2. Binary-Otsu w/ Guassian Blur (kernel size = 7)                                        #
# 3. Binary-Otsu w/ Gaussian Blur (kernel size = 5)                                        #
# 4. Binary-Otsu w/ Median Blur (kernel size = 5)                                          #
# 5. Binary-Otsu w/ Median Blur (kernel size = 3)                                          #
# 6. Adaptive Gaussian Threshold (31,2) w/ Gaussian Blur (kernel size = 5)                 #
# 7. Adaptive Gaussian Threshold (31,2) w/ Median Blur (kernel size = 5)                   #

# ========================================================================================= #

app = Flask(__name__)


path = os.getcwd()

# file Upload
UPLOAD_FOLDER = os.path.join(path,'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#UPLOAD_DIRECTORY = "/ocr-anaclic-project/api_uploaded_files"
UPLOAD_DIRECTORY = "uploads"

app.config['MAX_CONTENT_LENGHT'] = 16*1024*1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg','.png','.jpeg']
app.config['UPLOAD_PATH'] = 'uploads'


def apply_threshold(img,argument):
    switcher = {
        1: cv2.threshold(cv2.GaussianBlur(img,(9,9),0),0,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        2: cv2.threshold(cv2.GaussianBlur(img,(7,7),0),0,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        3: cv2.threshold(cv2.GaussianBlur(img, (5,5),0),0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        4: cv2.threshold(cv2.medianBlur(img,5),0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        5: cv2.threshold(cv2.medianBlur(img,3),0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        6: cv2.adaptiveThreshold(cv2.GaussianBlur(img,(5,5),0),255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,31,2),
        7: cv2.adaptiveThreshold(cv2.medianBlur(img,3),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,31,2),

    }
    return switcher.get(argument,"Invalid method")

def get_string(img_path,method):

    path = os.getcwd()
    output_dir = os.path.join(path, 'output')
    # Read image using openCV
    img = cv2.imread(img_path)
    file_name = os.path.basename(img_path).split('.')[0]
    file_name = file_name.split()[0]

    output_path = os.path.join(output_dir,file_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # convert to gray
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1,1),np.uint8)
    img = cv2.dilate(img,kernel,iterations=1)
    img = cv2.erode(img,kernel,iterations=1)

    # Apply threshold to get image with only black and white
    img = apply_threshold(img,method)
    save_path = os.path.join(output_path,file_name + "_filter_"+str(method) +".jpg")

    cv2.imwrite(save_path,img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(img,lang="fra",config="--oem 3 --psm 6")

    return result,save_path


def pretty_print(result_dict):
    s =''
    for key in result_dict:
        s+= '#' + key + ' : ' + result_dict[key] + '\n'
    return s


if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.route("/files/<path:path>")
def get_file(path):
    """ Download a file"""
    return send_from_directory(UPLOAD_DIRECTORY)

@app.route("/files")
def list_files():
    """ Endpoint to list files on the server ."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY)
        if os.path.isfile(path):
            files.append(filename)

    return jsonify(files)

@app.route("/files/<filename>",methods=["POST"])
def post_file(filename):
    """ Upload a file ."""
    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400,"no subdirectories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY,filename),"wb") as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return "",201

def preprocess_image():
    return "Image Preprocessing end .............."

def validate_image(stream):
    header = stream.read(512) # 512 bytes serait suffisant pour vérifier l'entête de l'image
    stream.seek(0) # Reset stream pointer
    # la valeur retournée par 'imghdr.what()' le format de l'image détectée
    format = imghdr.what(None,header)
    if not format:
        return None
    return '.' + (format if format!= 'jpeg' else 'jpg')

@app.errorhandler(413)
def too_large(e):
    return 'File is too large',413

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpeg','jpg','png']

@app.route('/uploadImageOCR',methods=['POST'])
def upload_image():

    overall_start_t = time.time()
    try:
        file_names = []
        curr_path = os.getcwd()
        output_dir = os.path.join(curr_path, 'output')

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

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

        file_name = file.filename
        start_time = time.time()
        i = 1
        while i < 8:
            print("> The filter method " + str(i) + "is now being applied.")
            result = get_string(file.filename,i)

            f = open(os.path.join(output_dir,file.filename,file.filename+"_filter_"+str(i) + ".txt"),'w')
            f.write(result)
            f.close()
            i +=1

        end_time = time.time()

        print('# ===========================================================\n'
              '# Resultats pour :'+ file_name + '\n'
              '# ===========================================================\n'
              '# Cela a pris '+str(end_time-start_time) + 'secondes.        \n'
              '# ===========================================================\n')

        overall_end_t = time.time()

        print('# ==========================================================\n'
              '# Résumé \n'
              '# ===========================================================\n'
              '# Le résultat avec succès de l\'opération est : \n'+pretty_print(result) +
              '# =========================================================== \n'
              '# Cela a pris '+str(overall_end_t - overall_start_t) +' secondes. \n'
              '# =========================================================== \n')

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

@app.route('/download')
def download():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('uploadfile.html',files=files)

@app.route('/uploader')
def uploader():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('form.html', files=files)


@app.route('/download',methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)

    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp

    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(uploaded_file.stream):
            return "Invalid image",400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'],filename))

    return '',204


@app.route('/uploader', methods=['POST'])
def uploader_file():
    my_files = request.files
    formData = request.form['myFormData']

    if request.method == "POST":
        file = request.files["file"]

        print("File Uploaded")
        print(file)

        res = make_response(jsonify({"message":"File Uploaded"}),200)

        return res

    with open("my_data.txt", "x+") as my_data:
        my_data.write(formData)

    for item in my_files:
        uploaded_file = my_files.get(item)
        uploaded_file.filename = secure_filename(uploaded_file.filename)

        if uploaded_file.filename != '':
            file_ext = os.path.splitext(uploaded_file.filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)

        uploaded_file.save(uploaded_file.filename)

    return redirect(url_for('form'))

if __name__ =='__main__':
    app.run(debug=True)

# 201 => response status only with successful operation
# 400 => bad request with error message
