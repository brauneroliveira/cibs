import glob
import os
import requests

fileList = glob.glob("xmlfiles/*")

url = 'http://localhost:5000/uploadHospitalBed'

reqno = 0

for f in fileList:
    reqno+=1
    file = open(f, 'r')
    files = {'file': file}
    r = requests.post(url, files=files)
    file.close()


