import cv2
import os
import numpy as np

"""
This is the structure of the repository.

data
|------- train
|           |----- kaichang1.jpg
|           |----- kaichang2.jpg
|           |----- ...
|           |----- kaichangN.jpg
|------- test
|           |----- test1.jpg
|           |----- test2.jpg
|           |----- test3.jpg

"""
class Interface(object):
    def __init__(self):
        self.train_PATH = './data/train/'
        self.model_PATH = './model/LBPH_model.xml'
        self.cascadePath = "./model/haarcascade_frontalface_default.xml"

        self.FRM = FacialRecognitionMachine(self.cascade_PATH, model_PATH=self.model_PATH, train_PATH=self.train_PATH)



class FacialRecognitionMachine(object):
    def __init__(self, cascade_PATH, model_PATH, train_PATH=None):

        # For face detection we will use the Haar Cascade provided by OpenCV.
        self.faceCascade = cv2.CascadeClassifier(cascadePath)

        if model_PATH is None:
            # LBPH Face Recognizer 
            self.LBPH_recognizer = cv2.createLBPHFaceRecognizer()
        else:
            self.LBPH_recognizer = self.loadModel(model_PATH)

        self.train_PATH = train_PATH        

    def get_images_and_labels(self, path):
        """
        Appends all absolute image paths.

        Parameters
        -----------
        path : location to training or test dataset

        Note: filenames are of form: FIRST.LAST-#
        """
        image_paths = [(os.path.join(path, f), f) for f in os.listdir(path) if f.endswith('.jpg')]

        # face images
        faces = []
        # label that is assigned to the image
        labels = []

        for image_path, image_name in image_paths:
            # Read the image
            image = cv2.imread(image_path)

            # acquire label
            label = image_name.split('-')

            # detect face
            face, rect = detect_face(image)

            # ignore if no face detected
            if face is not None:
                faces.append(face)
                labels.append(label)

        return faces, labels

    def detect_face(self, image):
        """
        Determine and learn where the face is
        and the features that correspond to its label.
        Currently only 1 facial detection (will incorporate 
        multiple down the road).

        Parameters
        ------------
        image       : image containing face
        """
        # convert to greyscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # detect list of faces (for recursive playing)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        # if no faces are detected, return None
        if (len(faces) == 0):
            return None, None

        # assume only a single face (take first one)
        (x, y, w, h) = faces[0]

        # return only face part of image
        return gray_image[y:y + w, x:x + h], faces[0]


    def train_dataset(self):
        """
        Gather all the training data, and train the model.
        """
        face, labels = get_images_and_labels(self.train_PATH)

        self.LBPH_recognizer.train(faces, np.array(labels))


    def predict(self, image):
        """
        Predict based on image what person is.
        """
        img = image.copy()
        face, rect = detect_face(img)

        label, conf = self.LBPH_recognizer.predict(face)
        label_text = subjects[label]

        # self.draw_rectangle(img, rect)
        # self.draw_text(img, lable_text, rect[0], rect[1]-5)

        return label_text


    def loadModel(self model_PATH):
        """
        Load an old Face Recognition model.
        """
        return cv2.loadLBPHFaceRecognizer(model_PATH)

    def saveModel(self):
        """
        Saves the new Face Recognition model.
        """
        self.FRM.LBPH_recognizer.save(self.model_PATH)


    """_____________ Display Functions _____________"""
    def draw_rectangle(self, image, rect):
        """
        Draw rectangle around face in image.
        
        Parameters
        ------------
        image : image with face
        rect  : coordinate boundary containing face
        """
        (x, y, w, h) = rect
        cv2.rectangle(image, (x,y), (x + w, y + h), (0, 255, 0), 2)

    def draw_text(self, image, text, x, y):
        """
        Places the Label (name) on the image.
        """
        cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)