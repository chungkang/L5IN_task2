# http://janpalasek.com/fast-reflection-removal.html
# https://pypi.org/project/fast-reflection-removal/
# https://github.com/yyhz76/reflectSuppress

from frr import FastReflectionRemoval
import cv2
import numpy as np

img = cv2.imread("module_test\\glare_test3\\IMG_3753.JPG")
img_array = np.array(img)

# Normalize the pixel values to be between 0 and 1
# numpy array with values between 0 and 1 of shape (H, W, C)
image_array_norm = img_array/255.0

# instantiate the algoroithm class
alg = FastReflectionRemoval(h = 0.1)
# run the algorithm and get result of shape (H, W, C)
dereflected_img = alg.remove_reflection(image_array_norm)
cv2.imwrite("module_test\\glare_test3\\IMG_3753_glare.JPG", dereflected_img)

