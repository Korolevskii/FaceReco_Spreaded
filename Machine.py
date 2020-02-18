from flask import Flask, request
import face_recognition
import os
import pickle
import socket
import numpy as np
import requests
import cv2
from requests_futures.sessions import FuturesSession

sess = FuturesSession()

import ifaddr

adapters = ifaddr.get_adapters()

AllIps = []

for i in range(len(adapters)):
    print("(" + str(i) + ") IPs of network adapter: " + adapters[i].nice_name)
    for ip in adapters[i].ips:
        if ip.is_IPv4:
            AllIps.append(ip)
            print(ip.ip)

my_ip = AllIps[int(input("You have more than one adapter, type index of the local network adapter"))].ip

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

    sizedFrame = np.array(sizedFrame)
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= int(1 / scale)
        right *= int(1 / scale)
        left *= int(1 / scale)
        bottom *= int(1 / scale)

        cv2.rectangle(sizedFrame, (int(left), int(top)), (int(right), int(bottom)), (0, 0, 255), 2)

        cv2.rectangle(sizedFrame, (int(left), int(bottom - 35)), (int(right), int(bottom)), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(sizedFrame, name + " " + str(round(face_distances[best_match_index], 4)), (left + 6, bottom - 6),
                 font, 1.0,
                 (255, 255, 255), 1)

    dat = pickle.dumps(sizedFrame)

    print(face_names)

    if outputUrl != '':
        sess.post(outputUrl + 'print', data=str(face_names))
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


scale = 1

known_face_encodings = []
known_face_names = []

enc_dir = './resurces/Encodings'

for filename in os.listdir(enc_dir):
    if filename.endswith(".fenc"):
        with open(enc_dir + '/' + filename, 'rb') as file:
            encod = pickle.load(file)
        for face_encod in encod:
            known_face_encodings.append(face_encod)
        known_face_names.append(str(filename[0:-5]))
    else:
        continue

directory = "./resurces/faces"
for filename in os.listdir(directory):
    if (filename.endswith(".jpg") or filename.endswith(".png")) and filename[0:-4] not in known_face_names:
        image = face_recognition.load_image_file(os.path.join(directory, filename))
        encoding = face_recognition.face_encodings(image)
        with open(enc_dir + '/' + filename[0:-4] + '.fenc', 'wb') as file:
            pickle.dump(encoding, file)
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
        request.get('http://' + socket.gethostbyname(socket.gethostname()) + ':' + str(port_c) + '/', timeout=2)
    except :
        break
    continue

if __name__ == '__main__':
    scanNetwork()
    app.run(host=socket.gethostbyname(socket.gethostname()), port=port_c)
