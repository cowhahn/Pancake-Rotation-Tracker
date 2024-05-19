'''
random debbuging code that I used to run only specific portions of the code for testing 
and also when I needed to fix prior data because I found a mistake or something failed
IDK random stuff like that. This isnt needed for the function of the program.'''

import OmegaT
import videoFrameSplitter
from os import listdir
import os
from os.path import isfile, join
import math
import VideoCreator
import ScriptManager

def filesInDirectory(my_dir: str):
    onlyfiles = [f for f in listdir(my_dir) if isfile(join(my_dir, f))]

list_of_videos = ['C0043.MP4','C0053.MP4']

#print(OmegaT.sumOfAngularVelocities('C0032.MP4'))
'''for i in listdir('./MarkedFrames'):
    if i not in listdir('./MarkedVideos'):
        VideoCreator.CreateVideo(i)'''
for i in listdir('./Data'):
    ClusterVelocity = OmegaT.sumOfAngularVelocities(i)
    f = open('./Data/'+i+'/ClusterAngularVelocity/Omega(t).txt', 'w')
    f.write(str(ClusterVelocity))
    f.close()
    #VideoCreator.CreateVideo(i)
#print(OmegaT.sumOfAngularVelocities('C0037.MP4'))

#ScriptManager.extractImagesFromFiles(None, './Videos')

'''for i in range(len(filesInDirectory('./Data.C0033.MP4'))):
    COM = OmegaT.findCOM(open('./Data/C0033.MP4/frame'+str(i)+'.jpg.txt','r'))
    arctanofpoints = OmegaT.findChangeInPos(COM.open('./Data/C0033.MP4/frame'+str(i)+'.jpg.txt','r'))
    f = open('./Data/C033.MP4/ArctanData/frame'+str(i)+'.jpg.txt','w')
    for i in arctanofpoints:
        f.write(str(i)+'\n')
    f.close()'''
'''for i in list_of_videos:
    ClusterVelocity = OmegaT.sumOfAngularVelocities(i)
    f = open('./Data/'+i+'/ClusterAngularVelocity/Omega(t).txt','w')
    f.write(str(ClusterVelocity))
    f.close()'''

'''def evaluate_equation(x1, y1, xCOM1, yCOM1, x2, y2, xCOM2, yCOM2):
    angle1 = math.atan2(y1 - yCOM1, x1 - xCOM1)
    angle2 = math.atan2(y2 - yCOM2, x2 - xCOM2)
    result = angle2 - angle1
    return result

x1, y1 = 1146.5, 285
x2, y2 = 1140.5, 286
xCOM1, yCOM1 = 1150.84, 625.04
xCOM2, yCOM2 = 1144.11, 624.35

# Evaluate the equation
result = evaluate_equation(x1, y1, xCOM1, yCOM1, x2, y2, xCOM2, yCOM2)

# Print the result
print(result)'''