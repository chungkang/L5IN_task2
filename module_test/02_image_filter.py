import cv2
import numpy as np

file_name = "module_test\\result\\IMG_3751_rect_crop"
image_name = file_name + ".png"

img = cv2.imread(image_name)
blur = cv2.GaussianBlur(img, (5, 5), 0)
# cv2.imwrite("module_test\\result_2\\image1_wraped_blur.png", blur)

# median = cv2.medianBlur(img, 5)
# cv2.imwrite("module_test\\result_2\\image1_wraped_median.png", median)

bilateral = cv2.bilateralFilter(img, 9, 75, 75)
cv2.imwrite(file_name + "_bilateral.png", bilateral)

# averaging = cv2.blur(img, (5, 5))
# blur_averaging = cv2.medianBlur(averaging, 5)
# cv2.imwrite("module_test\\result_2\\image1_wraped_blur_averaging.png", blur_averaging)

# img_gray = cv2.cvtColor(bilateral, cv2.COLOR_BGR2GRAY)
# _, src_bin = cv2.threshold(img_gray, 0, 255, cv2.THRESH_OTSU)
# cv2.imwrite(file_name + "_bin.png", src_bin)

# cv2.imwrite(file_name + "_gray.png", img_gray)

# normalized = cv2.normalize(img_gray, None, 0, 255, cv2.NORM_MINMAX)
# cv2.imwrite(file_name + "_normalize.png", normalized)


# CLAHE https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv
# converting to LAB color space
lab= cv2.cvtColor(bilateral, cv2.COLOR_BGR2LAB)
l_channel, a, b = cv2.split(lab)

# Applying CLAHE to L-channel
# feel free to try different values for the limit and grid size:
clahe = cv2.createCLAHE(clipLimit=1, tileGridSize=(75,75))
cl = clahe.apply(l_channel)

# merge the CLAHE enhanced L-channel with the a and b channel
limg = cv2.merge((cl,a,b))

# Converting image from LAB Color model to BGR color spcae
enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

# Stacking the original image with the enhanced image
cv2.imwrite(file_name + "_clahe.png", enhanced_img)


