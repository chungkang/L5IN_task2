import cv2
import matplotlib.pyplot as plt

img = cv2.imread("IMG_3753.JPG")
# img = cv2.imread("EG2.PNG")
# img = cv2.resize(img, (1000,500))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_gau = cv2.GaussianBlur(gray, (7,7), 0)
ret, img2 = cv2.threshold(gray, 140, 100, cv2.THRESH_BINARY_INV)
img_canny = cv2.Canny(gray, 50, 150)


# plt.subplot(2,2,1)
# plt.imshow(img)

plt.subplot(2,2,1)
plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))

plt.subplot(2,2,2)
plt.imshow(cv2.cvtColor(gray_gau, cv2.COLOR_BGR2RGB))

plt.subplot(2,2,3)
plt.imshow(img2, cmap="gray")

plt.subplot(2,2,4)
plt.imshow(img_canny, cmap="gray")


plt.show()