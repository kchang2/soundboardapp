import os
import time

import cv2
import numpy as np

# path to models, dataset
train_PATH = './data/train/'
model_PATH = './model/LBPH_model.xml'
cascade_PATH = "./model/haarcascade_frontalface_default.xml"

# face detector algorithm (from openCV)
faceCascade = cv2.CascadeClassifier(cascade_PATH)
# capture video from webcam
capture = cv2.VideoCapture(0)


def detectFace(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # returns tuple () if no face detected
    # returns numpy array [[x, y, w, h], ...] for all faces detected
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

def addFace(cap, faceCascade):
    """
    Add a new face into the training set, so we can
    now recognize the face in our database. After
    adding the face, it will run the train for our new dataset.
    """
    now = time.time()

    # 3 second duration
    while time.time() - now < 3:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
