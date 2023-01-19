import cv2
import numpy as np

# https://stackoverflow.com/questions/61121763/how-to-remove-glare-from-images-in-opencv

# read image
img = cv2.imread('module_test\\result\\20220112_162250_wrapped_crop.png')

# convert to gray
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# threshold grayscale image to extract glare
# mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)[1]
mask = cv2.threshold(gray, 205, 255, cv2.THRESH_BINARY)[1]

# Optionally add some morphology close and open, if desired
#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
#mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
#mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)


# use mask with input to do inpainting
# result = cv2.inpaint(img, mask, 21, cv2.INPAINT_TELEA) 
result = cv2.inpaint(img, mask, 20, cv2.INPAINT_TELEA) 

# write result to disk
cv2.imwrite("module_test\\result\\20220112_162250_mask.png", mask)
cv2.imwrite("module_test\\result\\20220112_162250_inpaint.png", result)

# display it
# cv2.imshow("IMAGE", img)
# cv2.imshow("GRAY", gray)
# cv2.imshow("MASK", mask)
# cv2.imshow("RESULT", result)
# cv2.waitKey(0)
