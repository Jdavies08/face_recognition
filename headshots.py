#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This code takes pictures of the user its recommended to take multiple per person
'''
import os
import logging
import shutil
import cv2
import functions
import train_model
# Logging levels affect many dependencies as well as current script.
# Change the verbosity of logs by changing the level to one of the following:
# CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
# Whatever level is set, that level and all levels more severe it will be logged.
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

MIN = 5
DATASET_FOLDER = "dataset"
CAMINDEX = 0
WINDOW_WIDTH=640
WINDOW_HEIGHT=1080
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONTSCALE = 0.5
TEXTCOLOUR = (255, 255, 255)
WINDOW_NAME = "press space to take a photo"

cam = functions.camera_connection(CAMINDEX)
name = input("Please enter the name you are booking in with, and then press Enter: ")

cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_FULLSCREEN)
#cv2.resizeWindow("press space to take a photo", WINDOW_WIDTH, WINDOW_HEIGHT)
if os.path.exists(DATASET_FOLDER):
    logger.debug("deleteing dataset folder at %s", DATASET_FOLDER)
    shutil.rmtree(DATASET_FOLDER)

if not os.path.exists(DATASET_FOLDER):
    logger.debug("Creating dataset folder at %s", DATASET_FOLDER)
    os.makedirs(DATASET_FOLDER)
if not os.path.exists(DATASET_FOLDER +"/"+ name):
    logger.debug("Creating new folder for %s", DATASET_FOLDER +"/"+ name)
    os.makedirs(DATASET_FOLDER +"/"+ name)
img_counter = 0# pylint: disable=invalid-name

while True:
    ret, frame = cam.read()
    if not ret:
        logger.error("Failed to grab frame. Please check camera connection.")
        break
    frame = cv2.putText(frame, "Position your face central and unobscured in front of the camera.",
    (10,int(20*FONTSCALE+400)), FONT, FONTSCALE,
            TEXTCOLOUR, 1, cv2.LINE_AA, False)
    frame = cv2.putText(frame, "Press space to take photo, we recommend take at least 5.",
    (10,int(50*FONTSCALE+400)), FONT, FONTSCALE,
            TEXTCOLOUR, 1, cv2.LINE_AA, False)
    frame = cv2.putText(frame, "Once you are finished press Esc.",
    (10,int(80*FONTSCALE+400)), FONT, FONTSCALE,
            TEXTCOLOUR, 1, cv2.LINE_AA, False)

    functions.loading_bar(frame,WINDOW_WIDTH,5,img_counter,0)
    cv2.imshow(WINDOW_NAME, frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        frame = train_model.train_model(WINDOW_NAME,functions.load_and_show,frame,WINDOW_WIDTH)
        frame = cv2.putText(frame, "Biometric profile generation completed",
        (10,int(50*FONTSCALE+100)), FONT, FONTSCALE,
            TEXTCOLOUR, 1, cv2.LINE_AA, False)
        frame = cv2.putText(frame, "You can now be recognised at the door",
        (10,int(80*FONTSCALE+100)), FONT, FONTSCALE,
            TEXTCOLOUR, 1, cv2.LINE_AA, False)
        frame = cv2.putText(frame, "Press any key to close",
        (10,int(110*FONTSCALE+100)), FONT, FONTSCALE,
            TEXTCOLOUR, 1, cv2.LINE_AA, False)
        cv2.imshow(WINDOW_NAME, frame)
        cv2.waitKey(0)
        logger.info("Escape hit, closing...")
        break
    if k%256 == 32:
        # SPACE pressed
        img_name = f"{DATASET_FOLDER}/{name}/image_{img_counter}.jpg"
        cv2.imwrite(img_name, frame)
        print(f"{img_name} written!")
        img_counter += 1

cam.release()
cv2.destroyAllWindows()
