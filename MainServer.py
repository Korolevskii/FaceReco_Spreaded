import requests
import cv2
import ipaddress
import pickle

video_capture = cv2.VideoCapture(0)

# links = ['http://127.0.0.50:5000/',
#          'http://127.0.0.51:5000/',
#          'http://127.0.0.52:5000/',
#        # 'http://127.0.0.53.5000/',
#          'http://127.0.0.54:5000/',
#          'http://127.0.0.55:5000/',
#          'http://127.0.0.56:5000/',
#          'http://127.0.0.57:5000/',
#          'http://127.0.0.58:5000/'
#          ]

counter = 0

scale = 1

req = requests.get('http://5.101.77.75:5000/getIp')
req = req.json()
ip = req['Ip']
list = requests.get('http://' + str(ipaddress.IPv4Address(ip)) + ':5000/get').json()['links']
list = list.split(" ")

links = []
for i in list:
    if len(i) > 1:
        links.append(i)

print(links)

while True:
    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

    rgb_small_frame = small_frame[:, :, ::-1]
    # Encode image
    img = pickle.dumps(rgb_small_frame)
    # Send image

    requests.post(links[counter], data=img)

    counter += 1
    if counter > len(links) - 1:
        counter = 0



