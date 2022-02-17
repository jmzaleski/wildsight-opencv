'''
Created on Feb. 16, 2022

@author: mzaleski
'''

#import numpy as np
import cv2 as cv
import os
import numpy as np
import random as rng
from pickle import FALSE

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
    #gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    #edges = cv.Canny(gray,50,150,apertureSize = 3)


    SHOW = False
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    
    
    if SHOW:
        cv.imshow("gray",imgray)
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
                
    cv.imshow('linesP', im)
    cv.waitKey(0)    
    exit(0)
    
    # Find lines
    #from https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/
    lines = cv.HoughLines(canny_output,1,np.pi/180, 200)
    #print(lines[0])
    # The below for loop runs till r and theta values 
# are in the range of the 2d array
    for pair in lines:
        print(pair)
        r = pair[0][0]
        theta = pair[0][1] #now do this in python..
        #print(r,theta)
        
        #HACK keep the line only if theta is vertical or horizontal. 
        #that's 0 or pi or pi/2 
        
        # Stores the value of cos(theta) in a
        a = np.cos(theta)
      
        # Stores the value of sin(theta) in b
        b = np.sin(theta)
          
        # x0 stores the value rcos(theta)
        x0 = a*r
          
        # y0 stores the value rsin(theta)
        y0 = b*r
          
        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
        x1 = int(x0 + 1000*(-b))
          
        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
        y1 = int(y0 + 1000*(a))
      
        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
        x2 = int(x0 - 1000*(-b))
          
        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
        y2 = int(y0 - 1000*(a))
          
        # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
        # (0,0,255) denotes the colour of the line to be 
        #drawn. In this case, it is red. 
        delta_x = x1-x0
        print("x1-x0", delta_x)
        delta_y = y1-y0
        print("y1-y0", delta_y)
        if abs(delta_x) < 10.0 or abs(delta_y) <10.0:
            print("draw", delta_x, delta_y)
            cv.line(im,(x1,y1), (x2,y2), (0,0,255),2)
        else:
            print("skip", delta_x, delta_y)


    cv.imshow('lines', im)
    cv.waitKey(0)    
    exit(0)

    
    contours, hierarchy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    
    # Draw contours
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    for i in range(len(contours)):
        color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        cv.drawContours(drawing, contours, i, color, 2, cv.LINE_8, hierarchy, 0)

    # Show in a window
    cv.imshow('Contours', drawing)
    cv.waitKey(0)    
    exit(0)
    
    
    #turn into grayscale (i'm not sure why)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)
    _, contours1, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnt = contours1[4]
    im_copy = im.copy()
    cv.drawContours(im_copy, [cnt], 0, (0,255,0), 3)
    
    cv.imshow('None approximation', im_copy)
    cv.waitKey(0)
    #cv.imwrite('contours_none_image1.jpg', image_copy)
    cv.destroyAllWindows()
    #img2 = im.copy()

    def thresh_callback(val):
        threshold = val
    
        # Detect edges using Canny https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html
        canny_output = cv.Canny(src_gray, threshold, threshold * 2)
    
        # Find contours
        _, contours, hierarchy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
        # Draw contours
        drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
        for i in range(len(contours)):
            color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
            cv.drawContours(drawing, contours, i, color, 2, cv.LINE_8, hierarchy, 0)
    
        # Show in a window
        cv.imshow('Contours', drawing)
