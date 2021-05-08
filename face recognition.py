import cv2
import face_recognition
import os
import numpy as np

known_face_encodings=[]
folders=os.listdir('/content/drive/MyDrive/face reco/lfw')
for i,folder in enumerate(folders[:100]):
    filename=os.listdir('/content/drive/MyDrive/face reco/lfw/'+folder)
    filename='/content/drive/MyDrive/face reco/lfw/'+folder+'/'+filename[0]
    known_face_names.append(filename)
    image = face_recognition.load_image_file(filename)
    encode=face_recognition.face_encodings(image)[0]
    print(i,'done')
    known_face_encodings.append(encode)


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True



frame = cv2.imread('/content/drive/MyDrive/face reco/Alfonso_Cuarón_(2013)_cropped.jpg')
small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

rgb_small_frame = small_frame[:, :, ::-1]

if process_this_frame:
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

process_this_frame = not process_this_frame



for (top, right, bottom, left), name in zip(face_locations, face_names):
    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
    top *= 4
    right *= 4
    bottom *= 4
    left *= 4

    # Draw a box around the face
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # Draw a label with a name below the face
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

# Display the resulting image
cv2_imshow(frame)