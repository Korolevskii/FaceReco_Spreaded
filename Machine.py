from flask import Flask, request
import face_recognition
import os
import pickle
import socket
import numpy as np
import requests
import time

my_ip = socket.gethostbyname(socket.gethostname())
my_ip = my_ip.split('.')
print(my_ip)

outputUrl = ''

app = Flask(__name__)

@app.route('/')
def home():
    return 'ok'



@app.route('/setUrl')
def setUrl():
    global outputUrl
    outputUrl = request.json['url']
    print(outputUrl)
    return '200'


@app.route('/ready')
def yes():
    return {'status': 'ok'}


@app.route("/handle", methods=["POST"])
def PrintNames():
    img = request.data
    sizedFrame = pickle.loads(img)[:, :, ::-1]
    face_locations = face_recognition.face_locations(sizedFrame)
    face_encodings = face_recognition.face_encodings(sizedFrame, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = list(face_recognition.face_distance(known_face_encodings, face_encoding))
        best_match_index = int(np.argmin(face_distances))
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            face_names.append(name)
    dat = pickle.dumps(face_names)
    if outputUrl != '':
        requests.post(outputUrl + 'print', data=dat)
    else:
        print('I have not output url')
    return '200'


def scanNetwork():
    for i in range(1, 255):
        print(f'http://{my_ip[0]}.{my_ip[1]}.{my_ip[2]}.{i}:5000/')
        try:
            requests.get(f'http://{my_ip[0]}.{my_ip[1]}.{my_ip[2]}.{i}:5000/new', json={'url': f'http://{my_ip[0]}.{my_ip[1]}.{my_ip[2]}.{my_ip[3]}:{port_c}/'}, timeout=0.001)
        except :
            continue


timer = 0
scale = 1

known_face_encodings = []
known_face_names = []

directory = "./resurces/faces"
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image = face_recognition.load_image_file(os.path.join(directory, filename))
        encoding = face_recognition.face_encodings(image)
        for face_encod in encoding:
            known_face_encodings.append(face_encod)
        known_face_names.append(str(filename[0:-4]))
    else:
        continue

print(known_face_names)

port_c = 5000

while True:
    port_c += 1

    try:
        r = requests.get('http://' + socket.gethostbyname(socket.gethostname()) + ':' + str(port_c) + '/', timeout=2)
    except :
        break
    continue

if __name__ == '__main__':
    scanNetwork()
    app.run(host=socket.gethostbyname(socket.gethostname()), port=port_c)
