import cv2
import requests
import pickle
import sys


links = sys.argv
video_capture = cv2.VideoCapture(0)
counter = 0
scale = 1
print(str(links) + ' - links are looped')
while True:
    if len(links) > 0:
        ret, frame = video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

        rgb_small_frame = small_frame[:, :, ::-1]
        # Encode image
        img = pickle.dumps(rgb_small_frame)
        # Send image

        requests.post(links[counter] + 'handle', data=img)

        counter += 1
        if counter > len(links) - 1:
            counter = 0