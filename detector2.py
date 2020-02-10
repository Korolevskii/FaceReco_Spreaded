import face_recognition
import cv2
import os
import numpy as np
import telepot
import requests
import time
from multiprocessing import Process, freeze_support, Pool

#####
#load photo to faces directory
###

#telegram bot activation
bot_token = "1074343264:AAH9TgJOnoDiqjLSh9zx2DUdtl4ICmyYoAQ"
chat_id = "-1001258327965"

session = requests.session()
session.proxies = {'http':  'socks5://127.0.0.1:9050',
                   'https': 'socks5://127.0.0.1:9050'}

url = "https://api.telegram.org/bot" + bot_token + "/"

timer = 0

def send_photo(text, image):
    global timer
    if(time.time()-timer > 10):
        timer = time.time()
        params = {'chat_id': chat_id, 'caption': text}
        files = {'photo': cv2.imencode('.jpg', image)[1].tostring()}
        response = session.post(url + 'sendPhoto', files=files, data=params)
        return response

def send_message(text):
    global timer
    if(time.time()-timer > 10):
        timer = time.time()
        params = {'chat_id': chat_id, 'text': text}
        response = session.post(url + 'sendMessage', data=params)
        return response

def f():
    time.sleep(0.1)
    return True




#scale of video stream
scale = 0.5


# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []

#get faces from directory
directory = "./faces"
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"): 
        #print(filename[0:-4])
        image = face_recognition.load_image_file(os.path.join(directory, filename))
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(str(filename[0:-4]))
    else:
        continue

        
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
secproc = None
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)


def face_encoding_compare(face_encoding, face_locations, known_face_encodings):
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    # Or instead, use the known face with the smallest distance to the new face
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_face_names[best_match_index]
        return name

def face_encoding_find(face_encodings, face_locations, known_face_encodings):
    face_names = []
    p = Pool(len(face_encodings))
    face_data = []
    for face_encoding in face_encodings:
        face_data.append((face_encoding, face_locations, known_face_encodings))
    face_names = p.starmap(face_encoding_compare, face_data) # range(0,1000) if you want to replicate your example
    p.close()
    p.join()
    print(face_names)

if __name__ == '__main__': 
    secproc = Process(target=f)
    secproc.start()

    while True: 
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            print("cadr")
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            if face_encodings != []: 
                secproc.join()
                print("gg")
                secproc = Process(target=face_encoding_find, args=(face_encodings, face_locations, known_face_encodings))
                secproc.start()
            
        process_this_frame = not process_this_frame
        

    video_capture.release()
    cv2.destroyAllWindows()