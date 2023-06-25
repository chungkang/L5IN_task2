# https://stackoverflow.com/questions/53968218/how-to-scan-room-contour-data-from-a-floor-plan-using-opencv-or-deep-learning
import cv2
import numpy as np
import random
import json
from shapely.geometry import LineString

MIN_AREA = 3000

file_name = "module_test\\result\\20230608_110853_bilateral_match_6_8"
image_name = file_name + ".png"

img = cv2.imread(image_name)

gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# Threshold the image to create a binary image
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
# _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

mor_img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (3, 3), iterations=3)

contours, hierarchy = cv2.findContours(mor_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

for c in contours[1:]:
    area = cv2.contourArea(c)
    if area > MIN_AREA:
        cv2.drawContours(img, [c], -1, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), 3)
        x, y, w, h = cv2.boundingRect(c) # the lines below are for getting the approximate center of the rooms
        cx = x + w / 2
        cy = y + h / 2

cv2.imwrite(file_name + "_img_bin.png", mor_img)
cv2.imwrite(file_name + "_img.png", img)
