# https://stackoverflow.com/questions/53968218/how-to-scan-room-contour-data-from-a-floor-plan-using-opencv-or-deep-learning
import cv2
import numpy as np
from shapely.geometry import LineString
import random

file_name = "module_test\\result\\20230608_110853_bilateral_opening"
image_name = file_name + ".png"

# Load the image
img = cv2.imread(image_name)

gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

mor_img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (3, 3), iterations=3)

contours, hierarchy = cv2.findContours(mor_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # I addapted this part of the code. This is how my version works (2.4.16), but it could be different for OpenCV 3 

sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

for c in sorted_contours[1:]:
    area = cv2.contourArea(c)
    if area > 600:
        cv2.drawContours(img, [c], -1, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), 3)
        x, y, w, h = cv2.boundingRect(c) # the lines below are for getting the approximate center of the rooms
        cx = x + w / 2
        cy = y + h / 2

cv2.imwrite(file_name + "_mor_img.png", mor_img)
cv2.imwrite(file_name + "_img.png", img)
