import cv2
import numpy as np

img = cv2.imread("module_test\\result\\image_wraped.png")
blur = cv2.GaussianBlur(img, (5, 5), 0)
# cv2.imwrite("module_test\\result_2\\image1_wraped_blur.png", blur)

# median = cv2.medianBlur(img, 5)
# cv2.imwrite("module_test\\result_2\\image1_wraped_median.png", median)

bilateral = cv2.bilateralFilter(img, 9, 75, 75)
cv2.imwrite("module_test\\result\\image_map_bilateral.png", bilateral)

# averaging = cv2.blur(img, (5, 5))
# blur_averaging = cv2.medianBlur(averaging, 5)
# cv2.imwrite("module_test\\result_2\\image1_wraped_blur_averaging.png", blur_averaging)
