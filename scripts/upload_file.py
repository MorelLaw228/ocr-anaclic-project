#!/usr/bin/python3

import os
from flask import Flask ,flash,request,redirect,render_template                 # import flask
from werkzeug.utils import secure_filename




app = Flask(__name__)                     # create an app instance


app.secret_key = " secret key"            # for encrypting the session

@app.route("/")                           # at the end point /
def hello():                              # call the method hello
    return "Hello World !!!!!"            # which returns "Hello World"


# It will allow below 16MB contents only , you can change it
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Récupérer le chemin d'accès courant
path  = os.getcwd()

# File Upload
UPLOAD_FOLDER = os.path.join(path,'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Liste des extensiosn autorisées pour l'upload des fichiers
ALLOWED_EXTENSIONS  = set(['txt','pdf','png','jpg','jpeg','gif'])


def allow_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# app routing and application running
@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('',methods=['POST'])
def upload_file():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)


        file = request.files['file']

        if file.filename == '':
            flash('No file selected for uploading')
            return  redirect(request.url)


        if file and allow_file(file.filename) :
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

            flash('File successfully uploaded')

            return redirect('/')

        else:
            flash('Allowed file types are : txt , pdf , png , jpg , jpeg, gif')

            return redirect(request.url)



if __name__ == '__main__':                 # Fonction main for running python app.py
    app.run(host='127.0.0.1',port='5000',debug=True)      # run the flask app


# Pour éxécuter l'application :
# -> Aller dans le Navigateur
# -> Et Saisir "http://localhost:5000"

# file uploading is the process of transmitting the binary or normal files to the server