# https://docs.opencv.org/3.4/dc/dc3/tutorial_py_matcher.html
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

file_name = "module_test\\result\\00_feature_match_01"
image_name = file_name + ".png"

img1 = cv.imread(image_name,cv.IMREAD_GRAYSCALE) # queryImage
img2 = cv.imread(file_name + '_template1.png',cv.IMREAD_GRAYSCALE) # trainImage

# Initiate SIFT detector
sift = cv.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# BFMatcher with default params
bf = cv.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)

# Apply ratio test to filter out false matches
good_matches = []

for m,n in matches:
    if m.distance < 0.75*n.distance:
        good_matches.append(m)

# Draw the matched keypoints and bounding box
img3 = cv.drawMatches(img1, kp1, img2, kp2, good_matches, None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)


# for match in good_matches:
#     pt1 = tuple(map(int, kp1[match.queryIdx].pt))
#     pt2 = tuple(map(int, kp2[match.trainIdx].pt))
#     cv.rectangle(img3, pt1, pt2, (0, 255, 0), thickness=2)


# Show the image with the bounding box
plt.imshow(img3), plt.show()