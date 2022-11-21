# Import the necessary libraries
import cv2
import math
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt #for visual debugging

total_lines = []

def distance(x0, x1, y0, y1):
  return math.sqrt((x0-x1)**2 + (y0-y1)**2)

def FLD(image, name):

  total_lines.clear() #Always reset total lines

  # Create default Fast Line Detector class
  length_threshold = 2 #default 10
  distance_threshold = 10 #default: 1.41421356 or 50
  
  #These are not really important for us
  canny_th1 = 100.0 #not important
  canny_th2 = 200.0 #not important
  canny_aperture_size =0 # we don't need to apply the canny filter
  do_merge = False

  #Detect lines here
  fld = cv2.ximgproc.createFastLineDetector(length_threshold, distance_threshold, canny_th1, canny_th2, canny_aperture_size, do_merge)

  # Get line vectors from the image
  lines = fld.detect(image)

  for line in lines:
    total_lines.append(line)

  print("Generating final image skeleton")
  # Draw lines on the image
  line_on_image = fld.drawSegments(image, lines)

  cv2.imwrite(name, line_on_image)

def WriteWallCoords(lines):
  print("Generating wall coords...")

  with open('walls_v3.txt', 'a') as f:
    for line in lines:
      length = 0
      coordinates = str(line[0][0]) + ' ' + str(line[0][1]) + ' ' + str(line[0][2]) + ' ' + str(line[0][3]) +  ' ' + str(length) +'\n'
      f.write(coordinates)
      
    f.close()

def RemoveSmallLines(line_length_threshold): #default line_length_threshold = 20
  for index, lines in enumerate(total_lines):
    current_line_length = distance(lines[0][0], lines[0][2], lines[0][1], lines[0][3])

    if(current_line_length <= line_length_threshold):
      print("Found line segment smaller than line length threshold, removing")
      total_lines.pop(index)

def SnapToNearestPoint(snap_dist_threshold): # default snap_dist_threshold = 15.0
  l = len(total_lines)

  print("Total number of line segments: ", l)

  for index, current_line in enumerate(total_lines):

    #Compare current line to next line
    if index < (l - 1):
      next_line = total_lines[index + 1]

      if(math.isclose(current_line[0][0], next_line[0][0], abs_tol = snap_dist_threshold) and math.isclose(current_line[0][1], next_line[0][1], abs_tol = snap_dist_threshold)):
        print("Found snapping candidate points between cl(0, 1) and nl(0, 1)...snapping")
        current_line[0][0] = next_line[0][0]
        current_line[0][1] = next_line[0][1]
        
      if(math.isclose(current_line[0][2], next_line[0][2], abs_tol = snap_dist_threshold) and math.isclose(current_line[0][3], next_line[0][3], abs_tol = snap_dist_threshold)):
        print("Found snapping candidate points between cl(2,3) and nl(2, 3)...snapping")
        current_line[0][2] = next_line[0][2]
        current_line[0][3] = next_line[0][3]

      if(math.isclose(current_line[0][0], next_line[0][2], abs_tol = snap_dist_threshold) and math.isclose(current_line[0][1], next_line[0][3], abs_tol = snap_dist_threshold)):
        print("Found snapping candidate points between cl(0,1) and nl(2, 3)...snapping")
        current_line[0][0] = next_line[0][2]
        current_line[0][1] = next_line[0][3]

      if(math.isclose(current_line[0][2], next_line[0][0], abs_tol = snap_dist_threshold) and math.isclose(current_line[0][3], next_line[0][1], abs_tol = snap_dist_threshold)):
        print("Found snapping candidate points between cl(2,3) and nl(0, 1)...snapping")
        current_line[0][2] = next_line[0][0]
        current_line[0][3] = next_line[0][1]

      total_lines[index] = current_line

def zhang_suen_skeleton(img):
  # use zhang_suen algorithm
  skel = cv2.ximgproc.thinning(img)
  
  return skel

def check_connectivity(block_img):
  block_img[1][1] = 0
  (rows, cols) = np.nonzero(block_img)
  rows = sorted(rows)
  cols = sorted(cols)

  # condition 1
  for i in range(len(rows)-1):
      if rows[i+1] - rows[i] > 1:
          return False
  for j in range(len(cols)-1):
      if cols[j+1] - cols[j] > 1:
          return False
  
  # condition 2: check 4 corners
  if block_img[0][0] > 0:
      if block_img[0][1] == 0 and block_img[1][0] == 0:
          return False
  if block_img[2][0] > 0:
      if block_img[2][1] == 0 and block_img[1][0] == 0:
          return False
  if block_img[2][2] > 0:
      if block_img[2][1] == 0 and block_img[1][2] == 0:
          return False
  if block_img[0][2] > 0:
      if block_img[0][1] == 0 and block_img[1][2] == 0:
          return False

  return True

def single_pixelated(img):
  (rows, cols) = np.nonzero(img)
  result = img.copy()
  removed_pixels = []
  for (r, c) in zip(rows, cols):
      if (r, c) not in removed_pixels:
          block_img = result[r-1: r+2, c-1: c+2].copy()
          if np.sum(block_img) >=3*255:
              if check_connectivity(block_img):
                  result[r][c] = 0
                  removed_pixels.append((r, c))
  return result

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

#Check this out as a possible solution: https://gis.stackexchange.com/questions/6728/joining-lines-when-direction-is-not-known

# Read the image as a grayscale image
img = cv2.imread('3_sb_morhps_dist_transform_thresh_crop.png', 0) 

#Thinning 
thinned_v1 = cv2.ximgproc.thinning(img)

#FLD pass 
FLD(thinned_v1, "skeleton_1.png")

#Cleaning an snapping

#Pass 1 - Remove small line segments
RemoveSmallLines(20)

#Pass 2 - snap to nearest line point
SnapToNearestPoint(15)

#Output clean floorplan image 
snapped_lines_img = np.zeros(img.shape)

for line in total_lines:
  print(line[0])
  cv2.line(snapped_lines_img,(int(line[0][0]), int(line[0][1])),(int(line[0][2]), int(line[0][3])),(255,0,0),1)

cv2.imwrite("skeleton_2.png", snapped_lines_img)

#Dilate image again to connect missing segments
dialte_v2 = cv2.imread('skeleton_2.png', 0)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
dilation_result = cv2.morphologyEx(dialte_v2, cv2.MORPH_CLOSE, kernel, iterations=10) #default iterations 1
cv2.imwrite("skeleton_3.png", dilation_result)

#Thinning - optional
#thinned_v2 = cv2.ximgproc.thinning(img_skel_2)

#FLD pass 
img_skel_2 = cv2.imread('skeleton_3.png', 0) 
FLD(img_skel_2, "skeleton_4.png")

#Dilation pass
dialte_v3 = cv2.imread('skeleton_4.png', 0)

kernel_v2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
dilation_result_v2 = cv2.morphologyEx(dialte_v3, cv2.MORPH_CLOSE, kernel_v2, iterations=10) #default iterations 1
cv2.imwrite("skeleton_5.png", dilation_result_v2)

#FLD pass 
FLD(dilation_result_v2, "skeleton_6.png")

#Dilation pass
dialte_v4 = cv2.imread('skeleton_6.png', 0)

kernel_v3 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
dilation_result_v3 = cv2.morphologyEx(dialte_v3, cv2.MORPH_CLOSE, kernel_v3, iterations=10) #default iterations 1
cv2.imwrite("skeleton_7.png", dilation_result_v3)

img = cv2.imread('skeleton_7.png', 0)

# Set threshold and maxValue
thresh = 0
maxValue = 255 
th, dst = cv2.threshold(img, thresh, maxValue, cv2.THRESH_BINARY);

cv2.imwrite('skeleton_7_thresh.png', dst)

img = cv2.imread('skeleton_7_thresh.png', 0)

skel = zhang_suen_skeleton(img)
single_skel = single_pixelated(skel)

cv2.imwrite('skeleton_8.png',single_skel)


img = cv2.imread('skeleton_8.png', 0)

#Contour detection
result_fill = np.ones(img.shape, np.uint8) * 255
result_borders = np.zeros(img.shape, np.uint8)

# the '[:-1]' is used to skip the contour at the outer border of the image
contours = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0][:-1] #Note: Use to get disconnected edges cv2.RETR_CCOMP

# fill spaces between contours by setting thickness to -1
cv2.drawContours(result_fill, contours, -1, 255, -1)
cv2.drawContours(result_borders, contours, -1, 255, 1)

# xor the filled result and the borders to recreate the original image
result = result_fill ^ result_borders

# prints True: the result is now exactly the same as the original
print(np.array_equal(result, img))

#TODO IMPORTANT: Merge all contours into one continous shape

cv2.imwrite('skeleton_9_contours.png', result)


#Apply DP filter
img_contours_final_dp = np.zeros(img.shape) 
img_contours_final = np.zeros(img.shape)
  
for cnt in contours:
    #DP Filtering
    epsilon = 0.03*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)
    cv2.drawContours(img_contours_final_dp, [approx], -1, 255, 1) 

print("Writting final contouring results to files...")
cv2.imwrite("skeleton_10_dp.png", img_contours_final_dp)
print("Done!")

#Morph ops
dialte_v4 = cv2.imread('skeleton_10_dp.png', 0)

kernel_v3 = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
dilation_result_v3 = cv2.morphologyEx(dialte_v4, cv2.MORPH_CLOSE, kernel_v3, iterations=10) #default iterations 1
cv2.imwrite("skeleton_11_morphs.png", dilation_result_v3)

img = cv2.imread('skeleton_11_morphs.png', 0)

thresh = 0
maxValue = 255 
th, dst = cv2.threshold(img, thresh, maxValue, cv2.THRESH_BINARY);

cv2.imwrite('skeleton_12_thresh.png', dst)

img = cv2.imread('skeleton_12_thresh.png', 0)

skel = zhang_suen_skeleton(img)
single_skel = single_pixelated(skel)

cv2.imwrite('skeleton_13_skel.png',single_skel)


FLD(single_skel, "skeleton_14_fld.png")

#WriteWallCoords(total_lines)