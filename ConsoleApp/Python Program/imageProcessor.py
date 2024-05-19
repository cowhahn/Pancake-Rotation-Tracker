import cv2 as cv
import numpy as np
import math 
import OmegaT
import traceback
import random

beta = -50 #i found that by adjusting the contrast and brightness of each frame templatematching worked better
alpha = 1.2
global templates
templates = cv.imread('./ImageTemplates/BallBearing2.png',cv.IMREAD_GRAYSCALE)
assert templates is not None, "file could not be read, check with os.path.exists()"
centers = [] #stores a frames position
deleted = []
n=0
radius = 50

#this draws the multicolored rectangles over the bearing on each frame 
def drawRectangles(centers,img_rgb,h,w,colors):
    for points in centers:
        #print(points)
        start_point = (int(points[0] + w/2), int(points[1] + h/2))
        end_point = (int(points[0] - w/2), int(points[1]-h/2))
        cv.rectangle(img_rgb, start_point, end_point, (colors[centers.index(points)][0],
                                                       colors[centers.index(points)][1],
                                                       colors[centers.index(points)][2]),
                                                         2)

def writeToFile(f,centers): #This is definitely not the best way to store positions but it was quick and made sense at the time.
    for y in range(2):
        for i in centers:
            if centers.index(i)+1 == len(centers) and y == 1: 
                f.write(str(i[y])) 
            else:
                f.write(str(i[y])+'\n')
    f.close()

def sortPoints(framename,videoname,points,sens): # this is called for every frame after frame0. So I realized that I had to ensure that a bearing is in the same index 
    sortedFrameData = [] #in the lists over the course of the videos so this takes the position of a bearing in the current frame finds the distance to each bearing in the 
    print('Processing frame:',framename,'in video:', videoname) #previous frame and then finds the closest and moves the position data to that index in the current frame.
    framenamenew = int(''.join(x for x in framename if x.isdigit())) #and does this for each bearing in the current frame, was able to verify it working by watching the marked videos
    #print(framename)                                                and seeing that none of the colors ever switched bearings.
    lastframe = framenamenew-1
    lastframedata = open('./Data/'+videoname+'/Frame'+str(lastframe)+'.jpg.txt','r')
    lastframex, lastframey = OmegaT.getPoints(lastframedata)
    #print(lastframex,lastframey)
    distances = []
    sortedDistances = []
    for z in range(len(points)):
        sortedFrameData.append('')
    for i in points:
        for y in range(len(lastframex)):
            foo = (i[0]-lastframex[y],i[1]-lastframey[y])
            foo = (foo[0]**2,foo[1]**2)
            foo = (math.sqrt(foo[0]+foo[1]))
            distances.append(foo)
        for g in distances:
            sortedDistances.append(g)
        sortedDistances.sort()
        sortedFrameData[distances.index(sortedDistances[0])] = i
        sortedDistances.clear()
        distances.clear()
    return sortedFrameData

def checkImage(framename,videoname,sens,colors):
    if 'C0' in videoname:                        #specific to our naming format
        templates = cv.imread('./ImageTemplates/BallBearing2.png',cv.IMREAD_GRAYSCALE)
        radius = 50 #a number that I found nicely pruned out repetitive marks for each bearing size.
    if 'SB' in videoname:
        templates = cv.imread('./ImageTemplates/SmallBearing.png',cv.IMREAD_GRAYSCALE)
        radius = 25
    img_rgb = cv.imread('./FrameExport/'+videoname+'/'+framename)
    assert img_rgb is not None, "file could not be read, check with os.path.exists()"
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    img_gray = cv.convertScaleAbs(img_gray, alpha=alpha, beta=beta)
    #templates_adjusted = cv.convertScaleAbs(templates,alpha=alpha,beta=beta)
    templates_adjusted = templates
    w, h = templates_adjusted.shape[::-1]
    centers = []
    deleted = []
    n=0
    res = cv.matchTemplate(img_gray,templates_adjusted,cv.TM_CCOEFF_NORMED) #I tested all the opencv2 algorithms and this worked best.
    threshold = sens
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        temp = (pt[0]+w,pt[1]+h)
        temp = (temp[0]+pt[0],temp[1]+pt[1])
        temp = (temp[0]/2,temp[1]/2)
        #print(temp)
        centers.append(temp)
    count = len(centers)
    new_centers = []
    for i in range(len(centers)): #prunes all repetitive points inside the radius of a bearing in pixels.
        keep_point = True         #it tests if any marked points are within a radius of it if there is it deletes that point.
        for j in range(i+1, len(centers)):
            dist = math.sqrt((centers[i][0]-centers[j][0])**2 + (centers[i][1]-centers[j][1])**2)
            if dist < radius:
                deleted.append(centers[j])
                keep_point = False
        if keep_point:
            new_centers.append(centers[i])
    centers = new_centers
    #print("We have detected",len(centers),"Bearings. Their positions are: ")
    #print(centers)
    #print("The Original Length was",count)
    #cv.imwrite('adjusted.png', img_gray)
    #cv.imwrite('res.jpg',img_rgb)
    try:    
        if framename != 'frame0.jpg': #only difference between these is that here we call the sortpoints function.
            #print("we need to fix points")
            centers = sortPoints(framename,videoname,centers,sens)
            #print(centers)
            writeToFile(open('./Data/'+videoname+'/'+framename+".txt", 'w'),centers)
            COM = OmegaT.findCOM(open('./Data/'+videoname+'/'+framename+".txt", 'r'))
            relativex,relativey = OmegaT.findChangeInPos(COM,open('./Data/'+videoname+'/'+framename+".txt",'r'))
            #print("arctans:",relativex,relativey)
            #print("COM:",COM)
            drawRectangles(centers,img_rgb,h,w,colors)
            cv.circle(img_rgb,(int(COM[0]),int(COM[1])),20,(0,0,0),-1)
            cv.imwrite('./MarkedFrames/'+videoname+'/'+framename,img_rgb)
            return(COM,relativex,relativey,len(centers))
        else:
            writeToFile(open('./Data/'+videoname+'/'+framename+".txt", 'w'),centers)
            COM = OmegaT.findCOM(open('./Data/'+videoname+'/'+framename+".txt", 'r'))    
            relativex,relativey = OmegaT.findChangeInPos(COM,open('./Data/'+videoname+'/'+framename+".txt",'r'))
            #print("arctans:",relativex,relativey)
            print("COM:",COM)
            drawRectangles(centers,img_rgb,h,w,colors)
            cv.circle(img_rgb,(int(COM[0]),int(COM[1])),20,(0,0,0),-1)
            cv.imwrite('./MarkedFrames/'+videoname+'/'+framename,img_rgb)
            print("detected", str(len(centers)), "bearings")
            return(COM,relativex,relativey,len(centers))
    except Exception:
        #print(traceback.format_exc())
        #print(e)
        return(0,0,0,len(centers)) # this is were that int is returned i dont know how it escapes the loop because it never did before i implemented the first frame checking.
    
if __name__ == '__main__':
    print('this doesnt do anything')