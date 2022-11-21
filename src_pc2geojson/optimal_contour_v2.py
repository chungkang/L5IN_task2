import cv2
import numpy as np
import networkx as nx
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

#Ref: https://pyimagesearch.com/2016/03/21/ordering-coordinates-clockwise-with-python-and-opencv/
# https://stackoverflow.com/questions/37742358/sorting-points-to-form-a-continuous-line

def order_points(points, ind):
    points_new = [ points.pop(ind) ]  # initialize a new list of points with the known first point
    pcurr      = points_new[-1]       # initialize the current point (as the known point)
    while len(points)>0:
        d      = np.linalg.norm(np.array(points) - np.array(pcurr), axis=1)  # distances between pcurr and all other remaining points
        ind    = d.argmin()                   # index of the closest point
        points_new.append( points.pop(ind) )  # append the closest point to points_new
        pcurr  = points_new[-1]               # update the current point
    return points_new

    
    
# Load image, grayscale, Gaussian blur, Otsus threshold
image = cv2.imread('skeleton_5.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Find horizonal lines
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)

# Find vertical lines
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=1)

# Find joint intersections then the centroid of each joint
joints = cv2.bitwise_and(horizontal, vertical)
cnts = cv2.findContours(joints, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
final_points = []
for c in cnts:
    # Find centroid and draw center point
    x,y,w,h = cv2.boundingRect(c)
    centroid, coord, area = cv2.minAreaRect(c)
    cx, cy = int(centroid[0]), int(centroid[1])
    final_points.append([cx, cy])
    cv2.circle(image, (cx, cy), 5, (36,255,12), -1)


    
# Find endpoints
corners = cv2.goodFeaturesToTrack(thresh, 5, 0.5, 10)
corners = np.int0(corners)
for corner in corners:
    x, y = corner.ravel()
    cv2.circle(image, (x, y), 5, (255,100,0), -1)

#cv2.imshow('thresh', thresh)
#cv2.imshow('joints', joints)
#cv2.imshow('horizontal', horizontal)
#cv2.imshow('vertical', vertical)
#cv2.imshow('image', image)
#cv2.waitKey()    

cv2.imwrite('optimal_v2_1.png', image) 


final_points_np = np.array(final_points)


#print("Final points: ", final_points_np)
#final_points_np = np.where(final_points_np==0, 1, final_points_np) #use this to replace 0 value with 1

#Re-order points and generate polyline
img_polyline = np.zeros(image.shape)

ind    = final_points_np.argmin()
ordered_points = order_points(final_points, ind) #this causes an error - likely cause is a zero value
print("Final ordered points: ", ordered_points)

ordered_points_np = np.array(ordered_points)
ordered_points_np = ordered_points_np.reshape((-1, 1, 2))

# color, thickness and isClosed
color = (255, 0, 0)
thickness = 2
isClosed = False

# drawPolyline
img_polyline = cv2.polylines(img_polyline, [ordered_points_np], isClosed, color, thickness)

cv2.imwrite('optimal_v2_2.png', img_polyline) 

