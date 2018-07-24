import os
import time
import errno

import cv2
import numpy as np

"""
This is the structure of the repository.

data
|------- train
|           |----- kaichang
|           |          |-------- 1.png
|           |          |-------- 2.png
|           |          |-------- ...
|           |          |-------- N.png
|           |----- ryancasey
|           |          |-------- 1.png
|           |          |-------- 2.png
|           |          |-------- ...
|           |          |-------- N.png
|           |----- ...


Things to do:
1. Get Video and take every 10 frames
2. Run Function to train model / save model
3. Test to see if can correctly identify
4. Gui

* Takes every 10 frames and analyzes, if detects face,
    then takes next 10 frames to confirm face.

** NOT SURE IF NEED TO SAVE MODEL DUE TO SPACE EFFICIENCY
    consider just re-running each time.

*** Got to move int2name, name2int separate from actual training
    if you want to save model, otherwise won't have it if you
    just load the model.
"""

class FacialRecognitionMachine(object):
    def __init__(self):

        self.train_PATH = './data/train/'
        self.model_PATH = './model/LBPH_model.xml'
        self.cascadePath = "./model/haarcascade_frontalface_default.xml"

        # For face detection we will use the Haar Cascade provided by OpenCV.
        self.faceCascade = cv2.CascadeClassifier(self.cascadePath)

        # For face detection, we will use the Local Binary Patterns Histograms (LBPH) model.
        self.model = cv2.createLBPHFaceRecognizer()
        # Other models: cv2.face.createEigenFaceRecognizer(), cv2.face.createFisherFaceRecognizer()

        # load previous model
        try:
            self.model.load(self.model_PATH)
        except:
            pass

        # create training folder if doesn't exist
        try:
            os.makedirs(self.train_PATH)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def loadModel(self):
        self.model.load(self.model_PATH)

    def detectFace(self, image):
        """
        Determine and learn where the face is
        and the features that correspond to its label.
        Currently only 1 facial detection (will incorporate 
        multiple down the road).

        Parameters
        ------------
        image       : image containing face (not grayscaled)

        Returns
        ------------
        faces : tuple() if no face detected, [[x, y, w, h], ...] for all faces detected
        gray  : grayscale image of original
        """
        # convert to greyscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # returns tuple () if no face detected
        # returns numpy array [[x, y, w, h], ...] for all faces detected
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        
        return faces, gray

    def addFace(self, name, frame_list):
        """
        Add new face images to dataset. This
        could be someone already in the database.

        Parameters
        ------------------
        name : name of person.
        """        
        face_PATH = self.train_PATH + name + '/'
        face_list = []

        try:
            count = len([f for f in os.listdir(face_PATH) if name not in f])

        except WindowsError:
            os.mkdir(face_PATH)
            count = 0

        for frame in frame_list:
            faces, gray = self.detectFace(frame)
            
            if len(faces) == 1:
                (x, y, w, h) = faces[0]
                img_PATH = face_PATH + str(count) + '.png'
                face_list.append( (img_PATH,  gray[y:y + w, x:x + h]) )
                count += 1

        # Assume yes
        for path, img in face_list:
            cv2.imwrite(path, img)

    def trainModel(self):
        """
        Trains the model.
        """
        # get all the names in training set (name associated to folder
        # in 1 to 1 correspondence)
        dirs = os.listdir(self.train_PATH)

        faces = [] # can be list of numpy arrays
        labels = [] # must be numpy array of type int

        # mapping name to int, int to name
        self.name2int = {k: dirs.index(k) for k in dirs}
        self.int2name = {v: k for k, v in self.name2int.iteritems()}

        for d in dirs:
            path = self.train_PATH + d + '/'
            files = [(os.path.join(path, f), d) for f in os.listdir(path) if f.endswith('.png')]
        
            for path, label in files:
                image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)
                faceId = self.name2int[label]

                faces.append(image)
                labels.append(faceId)

        
        self.model.train(faces, np.array(labels))

    def saveModel(self):
        self.model.save(self.model_PATH)

    def predictFrame(self, frame):
        """
        Detects face from webcam, and spits out name
        """
        faces, gray = self.detectFace(frame)

        # can only play 1 music at a time, so checks
        if len(faces) == 1:
            (x, y, w, h) = faces[0]
            face = gray[y:y + w, x:x + h]

            # Distance = 0 means an exact match. Large values mean that there is almost no match between both.
            label, conf = self.model.predict(face)
            name = self.int2name[label]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, name + ', ' + str(conf), (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

            return frame, name, conf

        return frame, None, None


# test = FacialRecognitionMachine()
# test.addFace('ryancasey')
# test.trainModel()
# test.predictLive()