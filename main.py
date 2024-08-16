"""
detect faces and draw a box around them
"""
import os
import sys
import time
import logging
import pickle
import cv2
import face_recognition
import functions

# Logging levels affect many dependencies as well as current script.
# Change the verbosity of logs by changing the level to one of the following:
# CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
# Whatever level is set, that level and all levels more severe it will be logged.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CAMINDEX = 0
SAVE_FILE = "encodings.pickle"
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONTSCALE = 1
TEXTCOLOUR = (255, 0, 0)
TOLERANCE = 0.4

if not os.path.exists(SAVE_FILE):
    data = {"encodings":[],"names":[]}
    print("No encoding file exists running face detection only")
else:
    with open(SAVE_FILE, "rb") as f:
        data = pickle.load(f)

known_encodings = data["encodings"]
names = data["names"]

cap = functions.camera_connection(CAMINDEX)

logger.debug("Begin face detection...")
while True:
    q , frame = cap.read()
    boxes = face_recognition.face_locations(frame)
    encodings = face_recognition.face_encodings(frame, boxes)
    face_count = len(encodings)
    if face_count > 0:
        logger.debug("Faces detected: %s" , str(face_count))
    else:
        # No face detected, so save some CPU cycles
        time.sleep(0.01)

    matches = []
    foundnames = []
    for x,encoding in enumerate(encodings):
        matches = face_recognition.compare_faces(known_encodings,encoding, tolerance = TOLERANCE)
        print(matches)
        if not matches:
            for i in boxes:
                matches.append(False)
        for e,i in enumerate(matches):
            top,right,bottom,left = boxes[x]
            cv2.rectangle(frame, (left,top), (right,bottom) , (0,255,0), 4)

            if i:
                foundnames.append(names[e])
                image = cv2.putText(frame, names[e], (left-20,top-20), FONT, FONTSCALE,
                TEXTCOLOUR, 1, cv2.LINE_AA, False)
            elif True not in matches:
                image = cv2.putText(frame, "Unknown", (left-20,top-20), FONT, FONTSCALE,
                TEXTCOLOUR, 1, cv2.LINE_AA, False)

    print("Found:",foundnames)
    cv2.imshow("window",frame)
    if cv2.waitKey(1) == ord("q"):
        break
    time.sleep(0.1)

logger.debug("Q pressed. Exiting...")
cv2.destroyAllWindows()
sys.exit()
