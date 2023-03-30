# https://stackoverflow.com/questions/63933790/robust-algorithm-to-detect-uneven-illumination-in-images-detection-only-needed

import cv2
import numpy as np
import skimage.filters as filters

# read the image
img = cv2.imread("module_test\\glare_test2\\IMG_3754.JPG")

# convert to gray
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# blur
smooth = cv2.GaussianBlur(gray, (33,33), 0)

# divide gray by morphology image
division = cv2.divide(gray, smooth, scale=255)

# sharpen using unsharp masking
sharp = filters.unsharp_mask(division, radius=1.5, amount=2.5, multichannel=False, preserve_range=False)
sharp = (255*sharp).clip(0,255).astype(np.uint8)
sharp_RGB = cv2.cvtColor(sharp, cv2.COLOR_GRAY2RGB)


# save results
cv2.imwrite("module_test\\glare_test2\\IMG_3754_division.JPG",division)
cv2.imwrite("module_test\\glare_test2\\IMG_3754_division_sharp.JPG",sharp)
cv2.imwrite("module_test\\glare_test2\\IMG_3754_division_sharp_RGB.JPG",sharp_RGB)

