#!/usr/bin/python
# Club de Robótica y Mecatrónica de la Universidad Autónoma de Madrid

# Fast reading from the raspberry camera with Python, Numpy, and OpenCV
# Allows to process grayscale video up to 124 FPS (tested in Raspberry Zero Wifi with V2.1 camera)
#
# Made by @CarlosGS in May 2017
# Club de Robotica - Universidad Autonoma de Madrid
# http://crm.ii.uam.es/
# License: Public Domain, attribution appreciated

import cv2
import numpy as np
import subprocess as sp
import datetime
import time
import atexit
import face_recognition
import pickle
import threading

#encodingsP = "encodings.pickle"
#data = pickle.loads(open(encodingsP, "rb").read())


frames = [] # stores the video sequence for the demo
max_frames = 300

N_frames = 0

HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())



# Video capture parameters
# Resolution spelar roll
(w,h) = (640, 340)
bytesPerFrame = w * h
fps = 250 # setting to 250 will request the maximum framerate possible

# "raspividyuv" is the command that provides camera frames in YUV format
#  "--output -" specifies stdout as the output
#  "--timeout 0" specifies continuous video
#  "--luma" discards chroma channels, only luminance is sent through the pipeline
# see "raspividyuv --help" for more information on the parameters
videoCmd = "raspividyuv -w "+str(w)+" -h "+str(h)+" --output - --timeout 0 --framerate "+str(fps)+" --nopreview"
videoCmd = videoCmd.split() # Popen requires that each parameter is a separate string

cameraProcess = sp.Popen(videoCmd, stdout=sp.PIPE, bufsize=w*h) # start the camera
atexit.register(cameraProcess.terminate) # this closes the camera process in case the python scripts exits unexpectedly

frame = None
boxes = []

def find_human():
    global frame
    global boxes
    while True:
        if frame is None:
            continue
        boxes, _ =  HOGCV.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03)
    
    
        if len(boxes) > 0:
            print("People in frame: ", len(boxes)) 


def find_face():
    global frame
    global boxes
    while True:
        if frame is None:
            continue
        boxes = face_recognition.face_locations(frame)

        if len(boxes) > 0:
            print("Faces in frame: ", len(boxes))
        
        
t=threading.Thread(target=find_face, daemon=True)
t.start()

emptyline = b'\0'*w
while True:
    
    buffer = [emptyline for i in range(h)]
    while emptyline in buffer:
        line = cameraProcess.stdout.read(w)
        buffer.pop(-1)
        buffer.insert(0, line)
    f= b''
    for i in buffer:
        f += i

    for (top, right, bottom, left) in boxes:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)


    frame = np.frombuffer(f, dtype=np.uint8 )     
    frame.shape = (h,w) # set the correct dimensions for the numpy array

   
    cv2.imshow("Slow Motion", frame) 
    key = cv2.waitKey(1) & 0xFF
    if key == 'q':
        break

cameraProcess.terminate() # stop the camera
cv2.destroyAllWindows()
