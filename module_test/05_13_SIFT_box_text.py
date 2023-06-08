# https://www.kaggle.com/code/dataenergy/object-recognition-using-feature-matching

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

file_name = "module_test\\result\\IMG_3751_rect_crop_bilateral"
image_name = file_name + ".png"

img1 = cv.imread(file_name + '_template1.png',cv.IMREAD_GRAYSCALE)
img2 = cv.imread(image_name,cv.IMREAD_GRAYSCALE)

sift = cv.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary
flann = cv.FlannBasedMatcher(index_params,search_params)
matches = flann.knnMatch(des1,des2,k=2)
# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in range(len(matches))]
# ratio test as per Lowe's paper
for i,(m,n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        matchesMask[i]=[1,0]
draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = cv.DrawMatchesFlags_DEFAULT)
img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

cv.imwrite(file_name + "_test.png", img3)

