# https://stackoverflow.com/questions/61693395/how-to-increase-the-size-of-the-line-to-be-searched-in-an-image-in-opencv-houghl
import cv2

file_name = "module_test\\result\\20230608_110853_bilateral_match_6_8"
image_name = file_name + ".png"

# Load the image
original = cv2.imread(image_name)

se=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
opening=cv2.dilate(original,se,iterations = 1)
opening=cv2.erode(opening,se,iterations = 1)

cv2.imwrite(file_name + "_opening.png", opening)