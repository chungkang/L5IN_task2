# https://redketchup.io/color-picker

import cv2
import numpy as np


def convert_standard_hsv_to_opencv_hsv(hsv_standard):
    hsv_opencv = np.array(hsv_standard, dtype=np.float32)
    hsv_opencv[0] /= 2  # Convert hue value
    hsv_opencv[1] *= 255 / 100  # Convert saturation value
    hsv_opencv[2] *= 255 / 100  # Convert value/brightness value
    return hsv_opencv

file_name = "module_test\\result\\4OG_full"
image_name = file_name + ".png"

# Read the image
img = cv2.imread(image_name)

# Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define the light green color range in HSV
lower_green = np.array(convert_standard_hsv_to_opencv_hsv([50, 5, 40]))
upper_green = np.array(convert_standard_hsv_to_opencv_hsv([150, 20, 70]))

# Create a mask that selects only the pixels within the color range
mask = cv2.inRange(hsv, lower_green, upper_green)

# Increase the value component (V)
hsv[..., 2][mask == 255] = 255

# Convert the image back to the BGR color space
result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

cv2.imwrite(file_name + "_color.png", result)