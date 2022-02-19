'''
Created on Feb. 16, 2022

@author: mzaleski
'''

#import numpy as np
import cv2 as cv
import os
import numpy as np

if __name__ == '__main__':
    
    #===========================================================================
    # tab = [["first","second"],["third", "fourth"]]
    # for pair in tab:
    #     left = pair[0]
    #     right = pair[1]
    #     print(left,right)
    # exit(0)
    #===========================================================================
    print("fool around with opencv opening a QGIS screensnap and looking for pink lines..")
    
    #FILE="smith.jpg"
    FILE="qgis-pink.jpg"
    im = cv.imread(FILE)
    if im is None:
        print("cannot open")
        os.system("/bin/pwd")
        exit(2)

    img = cv.imread(cv.samples.findFile(FILE))

    SHOW = True
    if SHOW:
        cv.imshow(FILE ,im)
        cv.waitKey(0)

    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        
    if SHOW:
        cv.imshow(FILE + "-gray",imgray)
        cv.waitKey(0)
    
    # Detect edges using Canny
    threshold = 100 #from https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html
    canny_output = cv.Canny(imgray, threshold, threshold * 2)        

    if SHOW:
        cv.imshow("canny output - edge detectin", canny_output)
        cv.waitKey(0)
        
    lines = cv.HoughLinesP(canny_output,1,np.pi/180,100,minLineLength=100,maxLineGap=10)
    for line in lines:
        x1,y1,x2,y2 = line[0]
        if abs(x1 - x2) < 100 or abs(y1 - y2) < 100 :
            print("skip (", x1,",",y1,") -> (",  x2,",",y2,")" )
            cv.line(im,(x1,y1),(x2,y2),(255,0,0),2)  
        else:
            print("draw (", x1,",",y1,") -> (",  x2,",",y2,")" )
            #cv.line(im,(x1,y1),(x2,y2),(0,255,0),2) #green for diagonals
                
    cv.imshow(FILE+'-linesP', im)
    cv.waitKey(0)    
    exit(0)
    
    