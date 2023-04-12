import cv2
import numpy as np
# Create a black image
img = np.zeros((512, 512, 3), np.uint8)

# Define the rectangle parameters
center = (256, 256)
size = (200, 100)
angle = 30

# Calculate the rectangle vertices
rect = cv2.boxPoints((center, size, angle))
rect = np.int0(rect)

# Draw the rectangle on the image
cv2.drawContours(img, [rect], 0, (0, 255, 0), 3)

# Show the image
cv2.imshow('Rotated Rectangle', img)
cv2.waitKey(0)
cv2.destroyAllWindows()