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
