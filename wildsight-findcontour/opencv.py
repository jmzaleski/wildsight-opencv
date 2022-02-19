'''
Created on Feb. 16, 2022

@author: mzaleski
'''

#import numpy as np
import cv2 as cv
import os
import numpy as np
SHOW = False
DEBUG = True


if __name__ == '__main__':
    
    print("fool around with opencv opening a QGIS screensnap and looking for pink lines..")
    
    #FILE="smith.jpg"
    FILE="qgis-pink.jpg"
    im = cv.imread(FILE)
    if im is None:
        print("cannot open")
        os.system("/bin/pwd")
        exit(2)

    img = cv.imread(cv.samples.findFile(FILE))

    if SHOW:
        cv.imshow(FILE ,im)
        cv.waitKey(0)

    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        
    if SHOW:
        cv.imshow(FILE + "-gray",imgray)
        cv.waitKey(0)
    
    # Detect edges using Canny
    threshold = 100 #from https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html
    im_edges = cv.Canny(imgray, threshold, threshold * 2)        

    if SHOW:
        cv.imshow("canny output - edge detectin", im_edges)
        cv.waitKey(0)
        
    # from: https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/
    
    lines = cv.HoughLinesP(im_edges,1,np.pi/180,threshold=75,minLineLength=10,maxLineGap=5)
    for line in lines:
        x1,y1,x2,y2 = line[0]
        if abs(x1 - x2) < 0.5 or abs(y1 - y2) < 0.5 :
            if DEBUG: 
                print("draw (", x1,",",y1,") -> (",  x2,",",y2,") because horizontal or vertical" )
            cv.line(im,(x1,y1),(x2,y2),(255,0,0),2)  
        else:
            if DEBUG:
                print("skip (", x1,",",y1,") -> (",  x2,",",y2,") because not horizontal or vertical" )
            #cv.line(im,(x1,y1),(x2,y2),(0,255,0),2) #green for diagonals.. eyeball to make sure no green horizontals
                
    cv.imshow(FILE+'-linesP', im)
    cv.waitKey(0)    
    exit(0)
    
    