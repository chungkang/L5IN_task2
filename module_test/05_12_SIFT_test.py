import cv2
import matplotlib.pyplot as plt

file_name = "module_test\\result\\IMG_3751_rect_crop_bilateral_crop"
image_name = file_name + ".png"

# Load the images
image1 = cv2.imread(file_name + '_template1.png')
image2 = cv2.imread(image_name)

# image1 = cv2.imread(file_name + '_template1.png', cv2.IMREAD_GRAYSCALE)
# image2 = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)

# Create a SIFT object
sift = cv2.SIFT_create()

# Detect keypoints and compute descriptors
keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
keypoints2, descriptors2 = sift.detectAndCompute(image2, None)

# Create a BFMatcher object
bf = cv2.BFMatcher()

# Perform matching using KNN algorithm
matches = bf.knnMatch(descriptors1, descriptors2, k=2)

# Apply ratio test to filter good matches
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)

# Draw the matches
output_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.imwrite(file_name + "_output.png", output_image)
