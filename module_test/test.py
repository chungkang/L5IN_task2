import cv2

BINARY_THRESHOLD = 140

file_name = "module_test\\result\\2OG_1_result"
image_name = file_name + ".png"

img = cv2.imread(image_name)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold the image to create a binary image
# _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_OTSU)
_, thresh = cv2.threshold(gray, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)

cv2.imwrite(file_name + "_bin.png", thresh)
