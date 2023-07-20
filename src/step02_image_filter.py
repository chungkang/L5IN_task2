import cv2

file_name = "module_test\\result\\4OG_4"
image_name = file_name + ".jpg"

img = cv2.imread(image_name)

bilateral = cv2.bilateralFilter(img, 9, 75, 75)
cv2.imwrite(file_name + "_bilateral.png", bilateral)