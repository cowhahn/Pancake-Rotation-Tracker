import math
import os
from os.path import isfile, join
from os import listdir


pi = math.pi

def filesInDirectory(my_dir: str):
    onlyfiles = [f for f in listdir(my_dir) if isfile(join(my_dir, f))]
    return(onlyfiles)

def getPoints(pointsfile):#reads the points from the text files in the weird format I have them.
    points = []
    pointsx = []
    pointsy = []
    for line in pointsfile:
        points.append(float(line))
    for i in range(len(points)):
        if i<= len(points)/2-1:
            pointsx.append(points[i])
        else:
            pointsy.append(points[i])
    pointsfile.close()
    return pointsx,pointsy

def findCOM(f):#works as long as all the bearings are the same mass.
    pointsx, pointsy = getPoints(f)
    ycm = 0
    xcm = 0   
    xcm = sum(pointsx)/len(pointsx)
    ycm = sum(pointsy)/len(pointsy)
    return(xcm,ycm)

def findChangeInPos(COM,points): #returns relative positions
    arctanOfI = []
    foox = []
    fooy = []
    pointsx,pointsy = getPoints(points)
    for x in pointsx:
        foox.append(x-COM[0])
    for y in pointsy:
        fooy.append(y-COM[1])
    return foox, fooy

def angularVelocityOfI(frame0RelativeX,frame0RelativeY,frame1RelativeX,frame1RelativeY):
    angle1 = math.atan2(float(frame0RelativeY), float(frame0RelativeX))
    angle2 = math.atan2(float(frame1RelativeY), float(frame1RelativeX))

    if angle1 < 0 and angle2 > 0:
        angle = (math.pi - angle1) + angle2
    elif angle1 > 0 and angle2 < 0:        #not 100 percent sure this is all right but without it I was getting delta thetas close to pi. 
        angle = -(math.pi - angle2) - angle1 #So i think that this works to fix whena bearing moves across quadrants of the unit circle.
    else:                                      #I think these weird values were because python returns negative angles for anything above pi radians.
        angle = angle2 - angle1
    while angle < -pi:
        angle += pi
    while angle > pi:
        angle -= pi

    angular_velocity = angle * 240 #specific to 240 fps
    #print(angular_velocity)
    return angular_velocity

def sumOfAngularVelocities(videoname):
    print(videoname)
    angularVelocityData = []
    framedata = []
    videodataX = []
    videodataY = []
    relativeXs = []
    relativeYs = []
    foo = []
    frameAngularVelocities = []
    videoAngularVelocities = []
    f = open('newfile.txt', 'w')
    pointsx = getPoints(open('./Data/'+videoname+'/frame0.jpg.txt','r'))
    n = len(pointsx[0])
    #print(n)
    runTime = len(filesInDirectory('./Data/'+videoname+'/COMData'))/240 #I wanted to implement some way to detect the framerate of a input video but never did.
    runTime = runTime - (1/240)
    #print(runTime)
    #creates a list of lists where the columns are each bearing and the rows represent each frame and the data is angular velocities.
    for  i in range(len(filesInDirectory('./Data/'+videoname+'/RelativeXPositions'))):
        for lines in open('./Data/'+videoname+'/RelativeXPositions/frame'+str(i)+'.jpg.txt','r'):
            relativeXs.append(lines)
        for lines in open('Data/'+videoname+'/RelativeYPositions/frame'+str(i)+'.jpg.txt','r'):
            relativeYs.append(lines)
        videodataX.append(relativeXs)
        videodataY.append(relativeYs)
        relativeYs = []
        relativeXs = []
    for frame in range(len(videodataX)-1):
        for data in range(len(videodataX[frame])):
            angularVelocityOfParticle = angularVelocityOfI(videodataX[frame][data],
                                                           videodataY[frame][data],
                                                           videodataX[frame+1][data],
                                                           videodataY[frame+1][data])
            #f.write(str(angularVelocityOfParticle)+'\n')
            frameAngularVelocities.append(angularVelocityOfParticle/(n*(959)))# 959 being specific to our camera T-1, we always had 960 frames in a video.
        videoAngularVelocities.append(frameAngularVelocities)
        frameAngularVelocities = []
    for i in videoAngularVelocities: #calculates the sigma notation for i=1 to n number of bearings.
        foo2 = sum(i)
        foo.append(foo2)
    foo3 = sum(foo) #same thing but for t=delta t to total frames.
    print(foo3)
    return foo3
    #print(videoAngularVelocities)
    #old but didnt want to delete for fear of needing again.
    '''for i in range(len(filesInDirectory('./Data/'+videoname+'/ArctanData'))):
        for lines in open('./Data/'+videoname+'/ArctanData/'+'frame'+str(i)+'.jpg.txt','r'):
            framedata.append(float(lines))
        #print(i)
        videodata.append(framedata)
        #print(videodata)
        framedata = []
    #print(videodata[0][0])
    #print(videodata)
    for frame in range(len(videodata)-1):
        for arctanData in range(len(videodata[frame])):
            angularVelocityOfParticle = angularVelocityOfI(videodata[frame][arctanData],videodata[frame+1][arctanData])
            #print(angularVelocityOfParticle)                                                                                    
            frameAngularVelocities.append(angularVelocityOfParticle)
        angularVelocityData.append(sum(frameAngularVelocities))
        frameAngularVelocities = []
    #print(angularVelocityData)
    for i in angularVelocityData:
        f.write(str(i)+'\n')
    f.close()
    ClusterAngularVelocity = sum(angularVelocityData)
    ClusterAngularVelocity = ClusterAngularVelocity/n
    ClusterAngularVelocity = ClusterAngularVelocity/(runTime - (1/240))
    return ClusterAngularVelocity'''

if __name__ == "__main__":
    print("script was run")