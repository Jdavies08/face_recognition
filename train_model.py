#! /usr/bin/python
'''
trains the model using data in the dat
'''

# import the necessary packages
import sys
import pickle
import os
import logging
import cv2
import face_recognition
from imutils import paths

# Logging levels affect many dependencies as well as current script.
# Change the verbosity of logs by changing the level to one of the following:
# CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
# Whatever level is set, that level and all levels more severe it will be logged.
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
SAVE_FILE = "encodings.pickle"
def train_model(window_name,progress_callback,frame, window_width):#pylint: disable = too-many-locals
    '''
    Takes the photos in the folders and uses them to train the model for later recognition.
    takes a callback for a progress bar progress callback must expect the following variables 
    progress_callback(frame,length,togo,loaded = 0,y = 0,thickness = 20) 
    window_name - the name of the window to display on
    frame - the frame that it will draw on
    length - the total length it should span
    togo - the total number of jobs to complete
    loaded - the number of these jobs done
    y - the y at which it starts at (the uppermost part of the bar)
    thickness- how far the bar should go downwards
    '''

    # our images are located in the dataset folder
    image_paths = list(paths.list_images("dataset"))
    if not os.path.exists(SAVE_FILE):
        data = {"encodings":[],"names":[]}
        logger.info("No encoding file exists running face detection only")
    else:
        with open(SAVE_FILE, "rb") as loadfile:
            data = pickle.load(loadfile)
    # initialize the list of known encodings and known names
    known_encodings = data["encodings"]
    known_names = data["names"]

    # loop over the image paths
    for (i, image_path) in enumerate(image_paths):
        # extract the person name from the image path

        frame = progress_callback(window_name,frame,window_width,len(image_paths),i + 1)
        #print(window_name,frame,window_width,len(image_paths),i + 1)
        name = image_path.split(os.path.sep)[-2]

        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(image_path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb,
            model="hog")

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            known_encodings.append(encoding)
            known_names.append(name)
    # dump the facial encodings + names to disk
    data = {"encodings": known_encodings, "names": known_names}
    with open(SAVE_FILE, "wb") as dumppicklefile:
        dumppicklefile.write(pickle.dumps(data))
        dumppicklefile.close()
    return frame

if __name__ == "__main__":
    print("This module is not intended to be run directly. Please see main_withdc.py")
    sys.exit(1)
