import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('test_image\\photo\\20220112_162239.jpg')

thresh = 0
maxValue = 255 

th, dst = cv2.threshold(image, thresh, maxValue, cv2.THRESH_BINARY)

# plt.imshow(image)

plt.figure(figsize=(10,5))
plt.subplot(121),plt.imshow(image, cmap='gray'),plt.title('original image',fontsize=15)
plt.xticks([]), plt.yticks([])

plt.subplot(122),plt.imshow(dst,cmap='gray'),plt.title('filtered image',fontsize=15)
plt.xticks([]), plt.yticks([])