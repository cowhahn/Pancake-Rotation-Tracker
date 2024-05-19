import argparse
import cv2
import time
import os

#print(cv2.__version__)
#takes a video and then iterates through it frame by frame until it cant writing each frame to the FrameExport folder created for that video.
def extractImages(pathIn, pathOut):
    count = 0
    vidcap = cv2.VideoCapture(pathIn)
    success,image = vidcap.read()
    success = True
    try:
        os.mkdir(pathOut)
    except Exception:
        print("Folder Already Exists")
    while success:
        cv2.imwrite("./" + pathOut + "/frame%d.jpg" % count, image)
        success,image = vidcap.read()        
        count +=1
    print("finished outputting video frames. Length:",str(count))
    time.sleep(5)

In = input("input path: ")
Out = input("output path: ")
extractImages(In, Out)



