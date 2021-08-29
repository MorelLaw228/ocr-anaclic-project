#!/usr/bin/python3
import datetime
import time
import io


import cv2
import pytesseract
from flask import *
import os
from werkzeug.utils import secure_filename
#import cv2
from PIL import Image
#import ultim
import imghdr
import numpy as np
import re
import csv
from spellchecker import SpellChecker
#from skimage import io
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

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Secret key for sessions encryption
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# Liste des extensiosn autorisées pour l'upload des fichiers
ALLOWED_EXTENSIONS  = set(['txt','pdf','png','jpg','jpeg','gif'])



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
    #img = io.imread(img_path)
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




def allow_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/home')
def my_home():
    return render_template("template.html", title="Image Reader")


@app.route('/scanner', methods=['GET', 'POST'])
def scan_file():
    if request.method == 'POST':
        start_time = datetime.datetime.now()
        image_data = request.files['file'].read()

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)

        if file and allow_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            flash('File successfully uploaded')

        #image_output = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        image_output = "/Users/morellatel/PycharmProjects/ocr-anaclic-project/uploads/Bilans_sanguins-page0.jpg"

        print("Image output :",image_output)
        i = 1

        curr_path = os.getcwd()
        output_dir = os.path.join(curr_path, 'output')

        while i < 8:
            print("> The filter method " + str(i) + "is now being applied.")

            # la variable "result" contient la sortie textuelle de l'opération d'OCR

            while not os.path.isfile(image_output):
                # ignore if no such file is present.
                pass

            result,_ = get_string(image_output,i)

            # On stocke ensuite le contenue de cette variable dans un fichier txt
            f = open(os.path.join(output_dir,image_output,image_output+"_filter_"+str(i) + ".txt"),'w')
            f.write(result)
            f.close()


            i+=1

        #result,_ = get_string(image_output)


        scanned_text = pytesseract.image_to_string(Image.open(io.BytesIO(image_data)),lang='fra',config='--oem 3 --psm 6')

        #scanned_text = pytesseract.image_to_string(Image.open(image_data))

        print("Found data:", scanned_text)

        session['data'] = {
            "text": scanned_text,
            "time": str((datetime.datetime.now() - start_time).total_seconds())
        }

        return redirect(url_for('result'))


@app.route('/result')
def result():
    if "data" in session:
        data = session['data']
        return render_template(
            "result.html",
            title="Result",
            time=data["time"],
            text=data["text"],
            words=len(data["text"].split(" "))
        )
    else:
        return "Wrong request method."






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
                #file.filename = secure_filename(file.filename)

                filename = secure_filename(file.filename)
                file_names.insert(0, file.filename)
                #file.save(file.filename)

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                flash('File successfully uploaded')

        file_name = file.filename
        print("Filename :",file_name)
        start_time = time.time()
        i = 1
        while i < 8:
            print("> The filter method " + str(i) + "is now being applied.")

            # la variable "result" contient la sortie textuelle de l'opération d'OCR
            result,_ = get_string(file.filename,i)

            # On stocke ensuite le contenue de cette variable dans un fichier txt
            f = open(os.path.join(output_dir,file.filename,file.filename+"_filter_"+str(i) + ".txt"),'w')
            f.write(result)
            f.close()

            output_file = os.path.join(output_dir,file.filename,file.filename+"_filter_"+str(i) + ".txt")

            # Méthode ou script qui permet de convertir la sortie .txt de l'opération d'OCR avec Pytesseract en fichier CSV

            header = ['Element', 'Unite', 'Valeur_obtenu', 'Valeur_reference', 'Anteriorite']
            with open('bilan.csv', 'w', encoding='UTF8') as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(header)
                fichier2 = open("correction0.txt", "a")
                spell = SpellChecker(language=None, distance=1)
                spell.word_frequency.load_dictionary('medicaleJson.json')
                with open('datasetDcp.txt') as f:
                    dictionnary = ['' + line.rstrip() for line in f]
                file = open(output_file, "r")
                # uniteBilan = open('uniteBilan.txt',"r")
                fichier = open("dataResult0.txt", "a")
                with open('uniteBilan.txt') as f:
                    uniteBilan = ['' + uniteB.rstrip() for uniteB in f]
                for line in file:
                    correct_output = []
                    output = '' + line.rstrip()
                    listOutput = output.split()
                    misspelled = spell.unknown(listOutput)
                    for word in listOutput:
                        correct_output.append(spell.correction(word))
                    output = ' '.join(correct_output)
                    fichier2.write(output + "\n")
                    for element in dictionnary:
                        correct_ligne = output if element.lower() in output.lower() else None
                        if correct_ligne is None:
                            pass
                        else:
                            correct_ligne = re.sub('([^\\w^*^<^>^=]{3,}[A-Za-z]*)(\\s*[a-zA-Z])*', ' ', correct_ligne)
                            if re.search('([^\\d]+\\d+){2,}', correct_ligne):
                                for unite in uniteBilan:
                                    # print(correct_ligne)
                                    # unite = ''+unit.rstrip()
                                    # print(unite)
                                    valeur = re.search(
                                        '\\W+\\d+\\W?\\d*\\s' + unite + '\\s\\d+\\W?\\d*\\s\\w?\\s\\d+\\W?\\d*(\\s\\d+\\W?\\d*)?',
                                        correct_ligne)
                                    # print(valeur)
                                    if valeur:
                                        valeurBilan = valeur.group(0)
                                        # print("mdr")
                                        print(" {} {} ".format(element, valeurBilan))
                                        print("")
                                        data = []
                                        data.append(element)
                                        data.append(unite)
                                        valeurBilan = re.sub(unite, '####', valeurBilan)
                                        valeur_obtenu = re.search(r'\d+\W?\s?\d+\s?####', valeurBilan)
                                        valeurBilan = re.sub(r'\d+\W?\s?\d+\s?####', '', valeurBilan)
                                        if valeur_obtenu:
                                            data.append(valeur_obtenu.group(0).rstrip('####'))

                                        valeur_reference = re.search(r'\d+\W\d+\s?à\s?\d+\W\d+', valeurBilan)

                                        if valeur_reference:
                                            data.append(valeur_reference.group(0))
                                        valeurBilan = re.sub(r'\d+\W\d+\s?à\s?\d+\W\d+', '', valeurBilan)

                                        anteriorite = re.search(r'\d+\W?\s?\d+\W?\d*', valeurBilan)

                                        if anteriorite:
                                            data.append(anteriorite.group(0))

                                        writer.writerow(data)
                                        # fichier.write("\n\n"+correct_ligne+"\n\n")
                                        break
                                    else:
                                        pass
                            else:
                                pass
            fichier.close()
            fichier2.close()

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
            return send_from_directory(os.getcwd(), 'bilan.csv', as_attachment=True)
        except Exception:
            abort(404)
    except Exception:
        return render_template("imagetotext.html")

#@app.route('/database/<filename>')
#def database(filename):
#    filename = 'http://127.0.0.1:5000/uploads/' + filename
#    return render_template('database.html',filename = filename)

#@app.route('/database_download/<filename>')
#def database_download(filename):
#    path = os.getcwd()
#    UPLOAD_FOLDER = path+'/'+'uploads'
#    return send_from_directory(UPLOAD_FOLDER,filename)

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/imagetotext')
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
