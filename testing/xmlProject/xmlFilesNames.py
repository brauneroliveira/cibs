import glob
import os
import requests

#only the files names
fileList = glob.glob("xmlfiles/*")

#the full path 
files_path = [os.path.abspath(x) for x in os.listdir("xmlfiles")]
url = 'http://localhost:5000/uploadHospitalBed'

reqno = 0

for f in fileList:
    reqno+=1
    file = open(f, 'r')
    files = {'file': file}
    r = requests.post(url, files=files)
    file.close()
    print('{}: {}'.format(reqno, r.text))


