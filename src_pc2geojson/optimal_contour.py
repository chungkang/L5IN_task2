#Clean contour generator from optimal skeletonized image

import cv2
import numpy as np

# image path
fileName = "Repn3.png"

# Reading an image in default mode:
inputImage = cv2.imread("3_sb_morhps_dist_transform_thresh_crop.png")
inputImageCopy = inputImage.copy()

# Convert to grayscale:
grayscaleImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)

# Compute the skeleton:
skeleton = cv2.ximgproc.thinning(grayscaleImage, None, 1)

# Threshold the image so that white pixels get a value of 10 and
# black pixels a value of 0:
_, binaryImage = cv2.threshold(skeleton, 128, 10, cv2.THRESH_BINARY)

# Set the convolution kernel:
h = np.array([[1, 1, 1],
              [1, 10, 1],
              [1, 1, 1]])

# Convolve the image with the kernel:
imgFiltered = cv2.filter2D(binaryImage, -1, h)

cv2.imwrite('optimal_1.png', imgFiltered)

# Create list of thresholds:
thresh = [130, 110, 40]

# Prepare the final mask of points:
(height, width) = binaryImage.shape
pointsMask = np.zeros((height, width, 1), np.uint8)

# Perform convolution and create points mask:
for t in range(len(thresh)):
    # Get current threshold:
    currentThresh = thresh[t]
    # Locate the threshold in the filtered image:
    tempMat = np.where(imgFiltered == currentThresh, 255, 0)
    # Convert and shape the image to a uint8 height x width x channels
    # numpy array:
    tempMat = tempMat.astype(np.uint8)
    tempMat = tempMat.reshape(height,width,1)
    # Accumulate mask:
    pointsMask = cv2.bitwise_or(pointsMask, tempMat)
    
# Set kernel (structuring element) size:
kernelSize = 3
# Set operation iterations:
opIterations = 4
# Get the structuring element:
morphKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelSize, kernelSize))
# Perform Dilate:
pointsMask = cv2.morphologyEx(pointsMask, cv2.MORPH_DILATE, morphKernel, None, None, opIterations, cv2.BORDER_REFLECT101)

cv2.imwrite('optimal_2.png', pointsMask)

# Look for the outer contours (no children):
contours, _ = cv2.findContours(pointsMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Store the points here:
pointsList = []

# Loop through the contours:
for i, c in enumerate(contours):

    # Get the contours bounding rectangle:
    boundRect = cv2.boundingRect(c)

    # Get the centroid of the rectangle:
    cx = int(boundRect[0] + 0.5 * boundRect[2])
    cy = int(boundRect[1] + 0.5 * boundRect[3])

    # Store centroid into list:
    pointsList.append( (cx,cy) )

    # Set centroid circle and text:
    color = (0, 0, 255)
    cv2.circle(inputImageCopy, (cx, cy), 3, color, -1)
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(inputImageCopy, str(i), (cx, cy), font, 0.5, (0, 255, 0), 1)

cv2.imwrite('optimal_3.png', inputImageCopy)
