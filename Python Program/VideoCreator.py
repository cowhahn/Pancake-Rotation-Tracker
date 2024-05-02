'''is used just basically does the reverse of video splitter and takes the outputted marked frames from the markedframes folders and turns
them into a video so you have videos with the rectangles marking each bearing and the COM marked.'''
import cv2 as cv
import glob


def CreateVideo(videoname):
    imgArray = []
    for filename in range(len(glob.glob('./MarkedFrames/'+videoname+'/*.jpg'))):
        img = cv.imread('./MarkedFrames/'+videoname+'/frame'+str(filename)+'.jpg')
        height, width, layers = img.shape #layers not used but if I remember .shape needs three variables to return to.
        size = (width, height)
        imgArray.append(img)

    out = cv.VideoWriter('./MarkedVideos/'+videoname,
                        cv.VideoWriter_fourcc(*'DIVX'), # this doesnt even matter its the wrong encoder for mp4s but cv2 just fixes it so i never changed it.
                        15,
                        size)
    for i in range(len(imgArray)):
        out.write(imgArray[i])
    out.release()
