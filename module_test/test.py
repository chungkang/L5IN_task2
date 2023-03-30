
import cv2
image = cv2.imread("module_test\glare_test2\IMG_3754_division_sharp.JPG")
image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

cv2.imwrite("module_test\glare_test2\IMG_3754_division_sharp_RGB.JPG", image_RGB)