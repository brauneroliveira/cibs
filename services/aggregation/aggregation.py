from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from HospitalBed import HospitalBed
from XMLFile import XMLFile
import os, json

app = Flask(__name__)
app.secret_key = 'd5581c21abc693c36798ae91ec69b5aa521c3755b95d63eb399df7ec69b5aa52'

#config = json.loads(open('config.json', 'r').read())

#app.config['UPLOAD_FOLDER'] = config['upload_folder']
#ALLOWED_EXTENSIONS = set(config['allowed_extensions'])

# def allowed_file(filename):
    # return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/persistHospitalBed', methods=['POST'])
def persistHospitalBed():
    requestxml = request.files['file']
    xmlfile = XMLFile(string=requestxml.read())

    hb = HospitalBed(xmlfile)

    return hb.id