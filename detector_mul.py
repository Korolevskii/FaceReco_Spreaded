import face_recognition
import cv2
import os
import numpy as np
import multiprocessing as mlp

timer = 0

scale = 1

video_capture = cv2.VideoCapture(0)

known_face_encodings = []
known_face_names = []

directory = "./faces"
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


def PrintNames(sizedFrame):
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
    return face_names


processed_thread = 0

# processcount = 4

pool = mlp.Pool(processes=4)


while True:
    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

    rgb_small_frame = small_frame[:, :, ::-1]

    result = pool.apply(PrintNames, args=(rgb_small_frame,))
    # PrintNames(rgb_small_frame)
    print(result.get(3))

video_capture.release()
cv2.destroyAllWindows()





