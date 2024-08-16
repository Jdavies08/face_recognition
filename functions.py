'''
Holds all functions for the code
'''
import sys
import logging
import cv2
import numpy as np

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONTSCALE = 0.5
TEXTCOLOUR = (255, 255, 255)
# Log level should be set in the main script
logger = logging.getLogger(__name__)

def camera_connection(camindex = 0):
    '''
    handles all connections to the camera and errors 
    camindex is the index of the camera as according to the OS
    returns a cv2 videocapture device
    '''
    try:
        cap = cv2.VideoCapture(camindex)
        ret= cap.read()[0]
        #check if an image can be formed
        if not ret:
            raise ValueError("camera not responding")

        # If we reach this point the camera has connected successfully
        logger.debug("Camera connected at index: %s", str(camindex))
    except ValueError:
        logger.warning("Camera is not valid, are you sure its plugged in or in use?")
        sys.exit(1)
    return cap

def load_and_show(window_name,frame,length,togo,loaded = 0,bar_y = 0,thickness = 60):#pylint: disable= too-many-arguments
    ''' 
    displays a loadingbar across the specified length and height and immediately displays it.
    this should be called for every frame you want it used
    window_name - the name of the window to display to
    frame - the frame that it will draw on
    length - the total length it should span
    togo - the total number of jobs to complete
    loaded - the number of these jobs done
    y - the y at which it starts at (the uppermost part of the bar)
    thickness- how far the bar should go downwards
    returns the frame with the bar drawn
    '''
    frame = np.zeros((500,640,3),np.uint8)
    frame = loading_bar(frame,length,togo,loaded,bar_y,thickness)
    frame = cv2.putText(frame, "Building your biometric profile. Please wait...",
    (10,100), FONT, FONTSCALE, TEXTCOLOUR, 1, cv2.LINE_AA, False )
    cv2.imshow(window_name, frame)
    cv2.waitKey(1)
    return frame

def loading_bar(frame,length,togo,loaded = 0,bar_y = 0,thickness = 20):#pylint: disable=too-many-arguments
    ''' 
    displays a loadingbar across the specified length and height,
    this should be called every frame you want it used
    frame - the frame that it will draw on
    length - the total length it should span
    togo - the total number of jobs to complete
    loaded - the number of these jobs done
    y - the y at which it starts at (the uppermost part of the bar)
    thickness- how far the bar should go downwards
    returns the frame with the bar drawn
    '''
    loaded = min(loaded, togo)
    processed = int((length/togo)*loaded)
    frame = cv2.rectangle(frame,(0,bar_y),(length,thickness),(255,255,255),5)
    frame = cv2.rectangle(frame,(5,bar_y+5),(processed-5,thickness -5),(0,255,0),-1)

    return frame

if __name__ == "__main__":
    print("This module is not intended to be run directly. Please see main.py")
    sys.exit(1)

def removevalue(array,value = "Unknown"):
    ''' removes the stated value from the passed array'''
    for i in array:
        if i == value:
            array.remove(i)
    return array
