import cv2

# Load input image
input_image = cv2.imread('module_test\\result\\20220112_162250_wrapped_crop.png')

# Convert image to grayscale
gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

# Threshold the grayscale image
thresholded_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)[1]

# Apply morphological transformation
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
morphed_image = cv2.erode(thresholded_image, kernel)
morphed_image = cv2.dilate(morphed_image, kernel)

# Remove reflection from grayscale image
output_image = cv2.subtract(gray_image, morphed_image)

# Save output image
cv2.imwrite('module_test\\result\\output_image.jpg', output_image)