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

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

    rgb_small_frame = small_frame[:, :, ::-1]
    face_distances = []
    best_match_index = 0
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = list(face_recognition.face_distance(known_face_encodings, face_encoding))
        best_match_index = int(np.argmin(face_distances))
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= int(1/scale)
        right *= int(1/scale)
        left *= int(1/scale)
        bottom *= int(1/scale)

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name + " " + str(round(face_distances[best_match_index], 4)), (left + 6, bottom - 6), font, 1.0,
                    (255, 255, 255), 1)

        face_distances.remove(face_distances[best_match_index])
        best_match_index = int(np.argmin(face_distances))
        name = known_face_names[best_match_index]

        cv2.putText(frame, name + " " + str(round(face_distances[best_match_index], 4)), (left + 6, bottom + 20), font, 1.0,
                    (255, 255, 255), 1)
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()


