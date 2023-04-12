import cv2
import numpy as np

# Define the 4 points of the edges of the rotated rectangle
rect = np.array([[100, 100], [400, 200], [400, 300], [200, 300]], np.int32)

# Calculate the angle and center of the rectangle
center, size, angle = cv2.minAreaRect(rect)
center, size = tuple(map(int, center)), tuple(map(int, size))

# Get the rotation matrix
M = cv2.getRotationMatrix2D(center, angle, 1)

# Apply the rotation to the 4 points of the rectangle
rotated_rect = cv2.transform(np.array([rect]), M)[0]

img = np.zeros((500, 500), dtype=np.uint8)

# Draw the 4 lines of the rotated rectangle
cv2.line(img, tuple(rotated_rect[0]), tuple(rotated_rect[1]), (255, 255, 255), 2)
cv2.line(img, tuple(rotated_rect[1]), tuple(rotated_rect[2]), (255, 255, 255), 2)
cv2.line(img, tuple(rotated_rect[2]), tuple(rotated_rect[3]), (255, 255, 255), 2)
cv2.line(img, tuple(rotated_rect[3]), tuple(rotated_rect[0]), (255, 255, 255), 2)

# Show the image
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
