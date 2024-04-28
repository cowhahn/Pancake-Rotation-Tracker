from os import listdir
import os
from os.path import isfile, join, exists
import videoFrameSplitter
import time
import imageProcessor
import OmegaT
import VideoCreator
import random
import _thread
from multiprocessing import Process
import re

files = None
watchdir = "./Videos"
sortedFrames = []
threshold = .7
amountInFirstFrame = None
amountInFrame = None
looping = True
global colors
colors = []

#this is for assigning colors to the rectangles that we draw on images marking the bearings, 
#this will throw an error if a video contains more than 80 bearings.
for i in range(80):
    colors.append([random.randint(0,255),
                   random.randint(0,255),
                   random.randint(0,255)])
    
#returns all files in a directory so this excludes folders
def filesInDirectory(my_dir: str):
    onlyfiles = [f for f in listdir(my_dir) if isfile(join(my_dir, f))]
    return(onlyfiles)

#old function not used anymore
def dataAlreadyComputed(videoToCheck):
    #print(videoToCheck)
    if os.path.exists('./Data/'+videoToCheck):
        return True
    else:
        return False
    
#old function not used anymore   
def videoAlreadySplit(videoToSplit):
    alreadySplit = listdir('./FrameExport')
    #print(alreadySplit)
    if videoToSplit in alreadySplit:
        #print("we already split this video:", videoToSplit)
        return True
    else:
        return False
    
#also not used anymore after implementing multiproccesing
def extractImagesFromFiles(files, watchdir):
    while True:
        if files == None:
            files = filesInDirectory(watchdir)
            #print("we havent set variable")
        elif files == filesInDirectory(watchdir):
            files = filesInDirectory(watchdir)
            #print("no update")
            time.sleep(5) 
        else:
            videosToSplit = filesInDirectory('./Videos')
            if filesInDirectory('./Videos') == []:
                #print('File deleted remaking files list.')
                files = None
            else:
                for i in videosToSplit:
                    if not videoAlreadySplit(i):
                        if not os.path.exists('./FrameExport/'+i):
                            os.makedirs('./FrameExport/'+i)
                        videoFrameSplitter.extractImages('./Videos/'+i,'./FrameExport/'+i)
                    else:
                        files = None
                break

def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path)

def ProcessVideo(i,colors):
    threshold = .67 #starting threshold for videos only matters if not using code to calibrate using first frame and video title.
    createPath('./Data/'+i)
    createPath('./Data/'+i+'/COMData')
    createPath('./Data/'+i+'/RelativeYPositions')
    createPath('./Data/'+i+'/RelativeXPositions')
    createPath('./Data/'+i+'/ClusterAngularVelocity')
    createPath('./MarkedFrames/'+i)
    for z in range(len(filesInDirectory('./FrameExport/'+i))): # I had to do this because python returns filesInDirectory in not number order
        sortedFrames.append('frame'+str(z)+'.jpg')             # I think it was something like frame0,frame1, frame10, frame100. So had to fix that
    #print(sortedFrames)
    for foo in sortedFrames:
        while True:
            try:
                COM,relativex, relativey,amountInFrame = imageProcessor.checkImage(foo,i,threshold,colors) 
                amountInFrame = amountInFrame
                error = False
                if sortedFrames.index(foo) == 0:
                    amountInFirstFrame = amountInFrame
                    if "SB" in i:                      #I never attempted to run this code again on any LB files so i dont know if its broken for them but 
                        if amountInFirstFrame > int(re.search(r'\d+', i).group()): #it causes an int to be returned for COM and then somehow that doesnt raise an exception or escapes the loop and then causes an error because ints dont have indicies in line 169
                            print("The amount in first frame is larger then expected, expected",int(re.search(r'\d+', i).group()),'got', amountInFirstFrame)
                            threshold += .001
                            error = True
                        if amountInFirstFrame < int(re.search(r'\d+', i).group()):
                            print("The amount in first frame is smaller then expected, expected",int(re.search(r'\d+', i).group()),'got', amountInFirstFrame)
                            threshold -= .001
                            error = True
                elif amountInFrame < amountInFirstFrame:
                    raise Exception
                elif amountInFrame > amountInFirstFrame:
                    raise Exception 
            except Exception as e: #what this code was meant to do before potentially broken was check to make sure each frame had the correct number of bearings detected
                print('Error in '+str(i)+': Amount of bearings excpected',amountInFirstFrame,'recieved',amountInFrame,'adjusting threshold')#and if not adjust the threshold until it did.
                #print('Error we have a different amount in this frame then lastframe, adjusting threshold')
                #print("Amount:", amountInFrame)
                #print("Amount in first Frame:",amountInFirstFrame)
                if amountInFrame < amountInFirstFrame:
                    #print('Error we have less in this frame then lastframe, adjusting threshold')
                    threshold = threshold - .0005
                    #print("new threshold is:", threshold)
                elif amountInFrame > amountInFirstFrame:
                    #print('Error we have less in this frame then lastframe, adjusting threshold')
                    threshold = threshold + .0005 #these can probably be adjusted higher but really did not want videos to get stuck repeating a frame due to large an increment.
                    #print("new threshold is:", threshold)
                #print("new threshold is:", threshold)
                #print('Unexpected error: ', e)
                error = True
            if amountInFrame == amountInFirstFrame and not error:
                break
        for n in range(len(relativex)):
            if n == len(relativex)-1:
                f.write(str(relativex[n]))
            else:
                f.write(str(relativex[n])+'\n') #writes each frames relative positions to files
        f.close()
        f = open('./Data/'+i+'/RelativeYPositions/'+foo+'.txt', 'w') 
        for n in range(len(relativey)):
            if n == len(relativey)-1:
                f.write(str(relativey[n])) #writes each frames relative positions to files
            else:
                f.write(str(relativey[n])+'\n')
        f.close()
        f = (open('./Data/'+str(i)+'/COMData/'+foo+'.txt','w'))
        f.write(str(COM[0])+'\n')
        f.write(str(COM[1]))
        f.close()
        f = open('./Data/'+i+'/RelativeXPositions/'+foo+'.txt', 'w')
    try:    
        VideoCreator.CreateVideo(i) #surrouned these in try except to ensure it wouldnt break code because it was new but probably doesnt need it.
    except:
        print('error creating marked video.')
    ClusterVelocity = OmegaT.sumOfAngularVelocities(i)
    f = open('./Data/'+i+'/ClusterAngularVelocity/Omega(t).txt', 'w')
    f.write(str(ClusterVelocity))
    f.close()

if __name__ == '__main__':
    p = []
    videosToCompute = []
    videos = listdir('./Videos')
    for j in videos:#splits any videos in ./videos that doesnt exist in frameExport
        if j not in listdir('./FrameExport'):
            createPath('./FrameExport/'+j)
            videoFrameSplitter.extractImages('./Videos/'+j,'./FrameExport/'+j)
    videos = listdir('./FrameExport')
    print(videos)
    for i in videos: # starts a process for each video in ./FrameExport not already in ./Data
        alreadyComputed = listdir('./Data')
        if i not in alreadyComputed:
            print('Attempting to start thread for video:',i)                   
            p.append(Process(target=ProcessVideo, args=(i,colors, )))
    for processes in p:
        processes.start()
    
