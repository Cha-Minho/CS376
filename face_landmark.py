import cv2
import dlib
import numpy as np
import os
import pickle

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

def get_face_landmarks(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)
    if len(rects) > 0:
        for rect in rects:
            landmarks = predictor(gray, rect)
            landmarks = [(p.x, p.y) for p in landmarks.parts()]
        return landmarks
    else:
        return None

directories = ['Data/concentrating', 'Data/unconcentrating']
landmarks_data = []

for dir in directories:
    label = 0 if dir.endswith('unconcentrating') else 1
    print(dir, label)
    for file_name in os.listdir(dir):
        if file_name.endswith('.jpg'):
            image_path = os.path.join(dir, file_name)
            image = cv2.imread(image_path)
            landmarks = get_face_landmarks(image)
            if landmarks is not None:
                landmarks_data.append((label,landmarks))

print(landmarks_data)
# Save all landmarks to a single file
with open('landmarks.dat', 'wb') as f:
    pickle.dump(landmarks_data, f)
