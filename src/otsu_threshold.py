import cv2
import numpy as np
import matplotlib.pyplot as plt 


# image = cv2.imread('test_image\\photo\\20221115_115018.jpg', 0)

image = cv2.imread('test_image\\photo\\20221115_115049.jpg', 0)


thresh = 0
maxValue = 255

otsu_threshold, image_result = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print(otsu_threshold)

th, dst = cv2.threshold(image, otsu_threshold, maxValue, cv2.THRESH_BINARY)

plt.figure(figsize=(14,5))
plt.subplot(121),plt.imshow(image, cmap='gray'),plt.title('original image',fontsize=15)
plt.xticks([]), plt.yticks([])

plt.subplot(122),plt.imshow(dst,cmap='gray'),plt.title('filtered image',fontsize=15)
plt.xticks([]), plt.yticks([])

plt.show()