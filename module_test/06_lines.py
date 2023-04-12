import cv2
import numpy as np

# Load the image
img = cv2.imread('module_test\\result\\template1_test\\image1_result_white.png')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Thresholding
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# Edge detection
edges = cv2.Canny(thresh, 50, 150, apertureSize=3)

# Hough Line Transform
lines = cv2.HoughLinesP(edges, rho=1, theta=1*np.pi/180, threshold=100, minLineLength=40, maxLineGap=10)

# Draw lines on the original image
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

cv2.imwrite('module_test\\result\\template1_test\\image1_crop_biliteral_lines.png', img)
