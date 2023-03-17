import cv2
import numpy as np
import matplotlib.pyplot as plt

# img = cv2.imread("module_test\\glare_test\\IMG_3753.JPG")
img = cv2.imread("module_test\\glare_test\\IMG_3753_glare.JPG")
# img = cv2.imread("module_test\\glare_test\\glare_test.png")
img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(img_HSV) # split into HSV components
cv2.imwrite('module_test\\glare_test\\IMG_3753_h_2.png', h)
cv2.imwrite('module_test\\glare_test\\IMG_3753_s_2.png', s)
cv2.imwrite('module_test\\glare_test\\IMG_3753_v_2.png', v)


nonSat = s < 60 # Find all pixels that are not very saturated
# Slightly decrease the area of the non-satuared pixels by a erosion operation.
# disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
disk = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
# disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
nonSat = cv2.erode(nonSat.astype(np.uint8), disk)
# Set all brightness values, where the pixels are still saturated to 0.
v2 = v.copy()
v2[nonSat == 0] = 0
# cv2.imwrite('module_test\\glare_test\\IMG_3753_nonSat_2.png', nonSat)
# cv2.imwrite('module_test\\glare_test\\IMG_3753_v2_2.png', v2) # v with nonSat


# plt.subplot(1, 3, 1)
# # plt.hist(nonSat.flatten(), bins=50)
# plt.imshow(nonSat)
# plt.xlabel("Brightness value")
# plt.ylabel("Frequency")
# plt.title("nonSat histogram")

# plt.subplot(1, 3, 2)
# # plt.hist(v.flatten(), bins=50)
# plt.imshow(v)
# plt.xlabel("Brightness value")
# plt.ylabel("Frequency")
# plt.title("V histogram")

# plt.subplot(1, 3, 3)
# # plt.hist(v2.flatten(), bins=50)
# plt.imshow(v2)
# plt.xlabel("Brightness value")
# plt.ylabel("Frequency")
# plt.title("V2 histogram")

# plt.show()

glare = v2 > 220 # filter out very bright pixels.
# Slightly increase the area for each pixel
glare = cv2.dilate(glare.astype(np.uint8), disk)

corrected = cv2.inpaint(img_HSV, glare, 5, cv2.INPAINT_NS)
corrected_RGB = cv2.cvtColor(corrected, cv2.COLOR_HSV2BGR)
cv2.imwrite('module_test\\glare_test\\IMG_3753_glare_2.png', glare)
cv2.imwrite('module_test\\glare_test\\IMG_3753_corrected.png', corrected_RGB)



