#!/usr/bin/python3

import os
from flask import Flask,render_template,request

# Importation de notre fonction d'OCR
from ocr_script import ocr_core

# Définition d'un dossier pour stocker et servir les images
UPLOAD_FOLDER =  '/static/uploads/'

# Autoriser juste les fichiers d'un certain format ou extension
ALLOWED_EXTENSIONS =  set(['png','jpg','jpeg'])

app = Flask(__name__)


# VERSION DE L'API
_VERSION = 1


# Création d'une fonction pour vérifier l'extension du fichier uploadé
# Elle prend en paramètre d'entré :
# -> le fichier dont on souhaite vérifier l'extension
def check_extension(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


# Definition des routes et fonctions pour la gestion de la page d'acceuil
@app.route("/")
def page_acceuil():
    return render_template('upload.html')

# Fonction pour l'upload des fichiers
@app.route("/upload",methods=['GET','POST'])
def upload_page():

    # On recoit l'image via la méthode "POST" et retourner le fichier HTML UPLOAD si la requête est "GET"
    if request.method == 'POST':
        # Vérifier s'il y a un fichier dans la requête
        if 'file' not in request.files:
            return render_template('upload.html', msg='Aucun fichier selectionné')

        file = request.files['file']

        # Si aucun fichier n'est selectionné :
        if file.filename ==' ':
            return render_template('upload.html',msg='Aucun fichier selectionné')
        # On vérifie si l'utilisateur a bien uploadé un fichier et utiliser
        # la fonction "check_extension" pour vérifier si le fichier est d'un format acceptable
        if file and check_extension(file.filename):

            # On appelle notre fonction d'OCR dessus
            extracted_text = ocr_core(file)

            # On extrait le texte de l'image et on l'affiche
            return render_template('upload.html',
                                   msg = 'Successfully Processed',
                                   img_src = UPLOAD_FOLDER + file.filename)

    elif request == 'GET':
        return render_template('upload.html')


# Appel de la fonction main pour éxécution
if __name__ == '__main__':
    app.run(debug=True)

