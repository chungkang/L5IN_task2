import cv2

file_name = "module_test\\result\\label_test"
image_name = file_name + ".png"

src = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)

_, src_bin = cv2.threshold(src, 0, 255, cv2.THRESH_OTSU)

cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(src_bin)

dst = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)

# 1 is background
for i in range(1, cnt):
    (x, y, w, h, area) = stats[i]

    # remove noize
    if area < 20 or area > 1000:
        continue

    cv2.rectangle(dst, (x, y, w, h), (0, 255, 255))

cv2.imwrite(file_name + "_binary.png", src_bin)
cv2.imwrite(file_name + "_line.png", dst)

# cv2.imshow('src', src)
# cv2.imshow('src_bin', src_bin)
# cv2.imshow('dst', dst)
# cv2.waitKey()
# cv2.destroyAllWindows()