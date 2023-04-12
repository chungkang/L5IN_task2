import cv2
import numpy as np

# Load the original image and template image
img = cv2.imread("module_test\\result\\image1_crop_biliteral.png")
template = cv2.imread('module_test\\result\\template_biliteral_1.png')

# Perform template matching using normalized cross-correlation
result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

# Obtain the location of the maximum correlation value
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# Create a mask image of the same size as the template and set all values to 1
mask = np.ones(template.shape[:2], dtype=np.uint8)

# Rotate the mask image to the same angle as the template
angle = -10 # example rotation angle
rows, cols = mask.shape[:2]
M = cv2.getRotationMatrix2D((cols/2,rows/2), angle, 1)
mask_rotated = cv2.warpAffine(mask, M, (cols,rows))

# Overlay the rotated mask image on the original image at the location of the maximum correlation value
overlay = np.zeros_like(img)
overlay[max_loc[1]:max_loc[1]+template.shape[0], max_loc[0]:max_loc[0]+template.shape[1]] = mask_rotated
result_no_overlap = cv2.bitwise_and(img, overlay)

# Repeat steps 1-5 for all templates and merge the resulting images to obtain the final image without any overlaps
# ...

# Display the result
cv2.imshow('Result without overlap', result_no_overlap)
cv2.waitKey(0)
cv2.destroyAllWindows()
