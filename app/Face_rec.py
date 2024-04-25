import imutils, time, cv2, sys
import dlib
import PIL.Image
import numpy as np
from imutils import face_utils
import argparse
from pathlib import Path
import os
import ntpath
import matplotlib.pyplot as plt

import smtplib, os

print('[INFO] Starting System...')
print('[INFO] Importing pretrained model..')
pose_predictor_68_point = dlib.shape_predictor("./Predictor/shape_predictor_68_face_landmarks.dat")
pose_predictor_5_point = dlib.shape_predictor("./Predictor/shape_predictor_5_face_landmarks.dat")
face_encoder = dlib.face_recognition_model_v1("./Predictor/dlib_face_recognition_resnet_model_v1.dat")
face_detector = dlib.get_frontal_face_detector()
print('[INFO] Importing pretrained model..')


def transform(image, face_locations):
    coord_faces = []
    for face in face_locations:
        rect = face.top(), face.right(), face.bottom(), face.left()
        coord_face = max(rect[0], 0), min(rect[1], image.shape[1]), min(rect[2], image.shape[0]), max(rect[3], 0)
        coord_faces.append(coord_face)
    return coord_faces


def encode_face(image):
    face_locations = face_detector(image, 1)
    if not face_locations:
        print("No face detected.")
        return None, None, None


    face_encodings_list = []
    landmarks_list = []
    for face_location in face_locations:
        # DETECT FACES
        shape = pose_predictor_68_point(image, face_location)
        face_encoding = face_encoder.compute_face_descriptor(image, shape)
        face_encodings_list.append(np.array(face_encoding))
        # GET LANDMARKS
        shape = face_utils.shape_to_np(shape)
        landmarks_list.append(shape)
    face_locations = transform(image, face_locations)
    return face_encodings_list, face_locations, landmarks_list




def easy_face_reco(frame, known_face_encodings, known_face_names):
    rgb_small_frame = frame[:, :, ::-1]
    code = cv2.COLOR_BGR2RGB
    rgb_small_frame = cv2.cvtColor(rgb_small_frame, code)
    # ENCODING FACE
    face_encodings_list, face_locations_list, landmarks_list = encode_face(rgb_small_frame)
    if face_encodings_list is not None and face_locations_list is not None and landmarks_list is not None:
        face_names = []
        for face_encoding in face_encodings_list:
            if len(face_encoding) == 0:
                return np.empty((0))
            # CHECK DISTANCE BETWEEN KNOWN FACES AND FACES DETECTED
            vectors = np.linalg.norm(known_face_encodings - face_encoding, axis=1)
            tolerance = 0.6
            result = []
            for vector in vectors:
                if vector <= tolerance:
                    result.append(True)
                else:
                    result.append(False)
            if True in result:
                first_match_index = result.index(True)
                name = known_face_names[first_match_index]
            else:
                name = "Unknown"
            face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations_list, face_names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 30), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (left + 2, bottom - 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

        for shape in landmarks_list:
            for (x, y) in shape:
                cv2.circle(frame, (x, y), 1, (255, 0, 255), -1)
    else:
        name = None
        print("No face detected.")

    return name



def capture(x, y):
    img1 = cv2.cvtColor(x, y)
    filename = './detection.jpg'

    cv2.imwrite(filename, img1)
    namme = print(filename)
    return namme


def images_process(path=Path('images')):

    print('[INFO] Importing faces...')
    face_to_encode_path = Path(path)
    print(face_to_encode_path)
    files = [file_ for file_ in face_to_encode_path.rglob('*.png')]

    for file_ in face_to_encode_path.rglob('*.png'):
        files.append(file_)
    if len(files) == 0:
        raise ValueError('No faces detect in the directory: {}'.format(face_to_encode_path))
    known_face_names = [os.path.splitext(ntpath.basename(file_))[0] for file_ in files]

    known_face_encodings = []
    for file_ in files:
        image = PIL.Image.open(str(file_))
        image = image.convert("RGB")
        nouvelle_taille = (150, 150)  # Par exemple, 300x300 pixels
        # Redimensionner l'image
        image = image.resize(nouvelle_taille)
        image = np.array(image)
        face_encodings, _, _ = encode_face(image)  # Assurez-vous de récupérer les valeurs retournées
        if face_encodings:
            face_encoded = face_encodings[0]
            known_face_encodings.append(face_encoded)
        else:
            print(f"Face encoding not found for {file_}")

    return known_face_names,known_face_encodings

known_face_names,known_face_encodings = images_process()
print('[INFO] Faces well imported')
print('[INFO] Starting Webcam...')
print('[INFO] Webcam well started')
print('[INFO] Detecting...')

"""
while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture frame. Exiting...")
        break

    easy_face_reco(frame, known_face_encodings, known_face_names)
    cv2.imshow('Alpha Recognition ISI', frame)
    capture(frame, cv2.COLOR_BGR2RGB)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print('[INFO] Stopping System')
video_capture.release()
cv2.destroyAllWindows()"""