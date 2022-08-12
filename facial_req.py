#! /usr/bin/python

"""
MIT License

Copyright (c) 2021 Caroline Dunn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# import the necessary packages
from threading import Timer
import face_recognition
import cv2
import numpy as np

import pickle
import socket
import time
import datetime
import struct


def dump_buffer(s):
  while True:
    seg, addr = s.recvfrom(MAX_DGRAM)
    print(seg[0])
    # 49 = ASCII '1'
    # Räknar ner till sissta segmentet (1)
    seg_n = struct.unpack('B', seg[0:1])[0]
    if seg_n == 1 or seg_n == 49:
      print('finish emptying buffer')
      break

#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())
time.sleep(2.0)
MAX_DGRAM = 2**16
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 1337))
dat = b''
dump_buffer(s)




# start the FPS counter
#fps = FPS().start()


# loop over frames from the video file stream
while True:
    
    # grab the frame from the threaded video stream and resize it
    # to 500px (to speedup processing)
    b = datetime.datetime.now()

    frame = 0
    
    while(True):
        
        
        seg, addr = s.recvfrom(MAX_DGRAM)
        print('recv')
        if struct.unpack('B', seg[0:1])[0] > 1:
            dat += seg[1:]
        else:
            dat += seg[1:]
            frame = cv2.imdecode(np.frombuffer(dat, dtype=np.uint8), 1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            dat = b'' # cap.§release()
            break
        
    print("Frame: ", (datetime.datetime.now() - b).microseconds)
    #frame = imutils.resize(frame, width=500)
    # Detect the fce boxes
    b = datetime.datetime.now()
    if(isinstance(frame,np.ndarray)):
        if(frame.any()):
            boxes = face_recognition.face_locations(frame)
            print("Face: ", (datetime.datetime.now() - b).microseconds)
    
            encodings = face_recognition.face_encodings(frame, boxes)
            names = []
            matches = []
            matchedIdxs = []
            # 
            # # loop over the facial embeddings
            for encoding in encodings:
            # # attempt to match each face in the input image to our known
            # # encodings
                matches = face_recognition.compare_faces(data["encodings"], encoding, 0.5)
                name = "Unknown" #if face is not recognized, then print Unknown

               
                # # check to see if we have found a match
                if True in matches:
                # # find the indexes of all matched faces then initialize a
                # # dictionary to count the total number of times each face
                # # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
                # 
                # # loop over the matched indexes and maintain a count for
                # # each recognized face face
                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1
                    # 
                    # # determine the recognized face with the largest number
                    # # of votes (note: in the event of an unlikely tie Python
                    # # will select first entry in the dictionary)
                    name = max(counts, key=counts.get)
                    # 
                    # #If someone in your dataset is identified, print their name on the screen
                    if currentname != name:
                        currentname = name
                    # print(currentname)
                    # 
                    # # update the list of names
                    names.append(name)


                # loop over the recognized faces
                for (top, right, bottom, left) in boxes:
                # draw the predicted face name on the image - color is in BGR
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
                    y = top - 15 if top - 15 > 15 else top + 15
                    cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 255), 2)

            # display the image to our screen
            
            cv2.imshow("Facial Recognition is Running", frame)
            key = cv2.waitKey(1) & 0xFF

            # quit when 'q' key is pressed
            if key == ord("q"):
                break
    # update the FPS counter
 #   fps.update()
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
