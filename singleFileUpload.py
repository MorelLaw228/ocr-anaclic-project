#!/usr/bin/python3

# For file manipulations like get paths,rename
import os
from flask import Flask,flash,request,redirect,render_template

from werkzeug.utils import secure_filename

app = Flask(__name__)

# For encrypting the session
app.secret_key = "SECRET KEY "

# It will allow below 16MB content only , you can change it
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024

path = os.getcwd()
print("Chemin d\'accès est :",path)

# File UPLOAD
UPLOAD_FOLDER = os.path.join(path,'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif','tif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


# For app routing and application running
@app.route("/")
def upload_form():
    return render_template('upload_file.html')

@app.route("/",methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash("No File selected for uploading ")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

            flash('File Successfully UPLOADED')

            return redirect('/')

        else:
            flash('Allowed file types are txt,pdf,png,jpg,jpeg,gif')
            return redirect(request.url)

        #############################################################
        ###############   FOR MULTIPLE UPLOAD  #####################

        #if 'files[]' not in request.files:
        #    flash('No file PART')
        #    return redirect(request.url)

        #files = request.files.getlist('files[]')

        #for file in files:
        #    if file and allowed_file(file.filename):
        #        filename = secure_filename(file.filename)
        #        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

        #flash('File(s) successfully uploaded')
        #return redirect('/')
        #############################################################


if __name__ == '__main__':
    app.run(debug=True)

