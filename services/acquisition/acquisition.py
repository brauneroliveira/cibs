from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import requests
import os, json

app = Flask(__name__)
app.secret_key = 'd5581c21abc693c36798ae91b765966c811c3755b95d63eb399df7ec69b5aa52'

config = json.loads(open('config.json', 'r').read())

app.config['UPLOAD_FOLDER'] = config['upload_folder']
ALLOWED_EXTENSIONS = set(config['allowed_extensions'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadHospitalBed', methods=['POST'])
def uploadHospitalBed():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'NO_FILE_PART'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return 'NO_FILE'
        if file and allowed_file(file.filename):
            
            url = 'http://localhost:5001/persistHospitalBed'
            files = {'file': file}
            r = requests.post(url, files=files)
            return r.content
        return 'VOID'
    else:
        return 'REQUEST_NOT_POST'