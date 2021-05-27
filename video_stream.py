import cv2
import numpy as np
import face_recognition
from PIL import Image,ExifTags
import pandas as pd
import pydb
import dlib

known_face_names,known_face_encodings=pydb.getitems()
print(known_face_names,type(known_face_encodings))
dlib.DLIB_USE_CUDA = True
video_capture = cv2.VideoCapture('video1.mp4')

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
width= int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

writer= cv2.VideoWriter('demo1.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))


while True:
    ret, frame = video_capture.read()
    #frame = cv2.resize(frame, (640, 480))
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        #print(type(face_locations),face_locations)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

       
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 200, 50), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    writer.write(frame)
    h, w = frame.shape[0:2]
    neww = 800
    newh = int(neww*(h/w))
    frame = cv2.resize(frame, (neww, newh))
    cv2.imshow('img',frame)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

writer.release()
cv2.destroyAllWindows()

