# https://stackoverflow.com/questions/42938149/opencv-feature-matching-multiple-objects?noredirect=1&lq=1

import cv2
import numpy as np
from sklearn.cluster import DBSCAN, MeanShift, estimate_bandwidth

MIN_MATCH_COUNT = 4

file_name = "module_test\\result\\20230608_110853_bilateral"
image_name = file_name + ".png"

templateImage = cv2.imread(file_name + '_template1.png')
backgroundImage = cv2.imread(image_name)

# # 1.1. Feature Extraction: ORB
# orb = cv2.ORB_create(10000, 1.2, nlevels=8, edgeThreshold = 5)

# # find the keypoints and descriptors with ORB
# kp1, des1 = orb.detectAndCompute(templateImage, None)
# kp2, des2 = orb.detectAndCompute(backgroundImage, None)
# # 1.1.

# 1.2. Feature Extraction: SIFT
sift = cv2.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(templateImage, None)
kp2, des2 = sift.detectAndCompute(backgroundImage, None)
# 1.2.

# 2.1. Clustering: MeanShift
x = np.array([kp2[0].pt])

for i in range(len(kp2)):
    x = np.append(x, [kp2[i].pt], axis=0)

x = x[1:len(x)]

bandwidth = estimate_bandwidth(x, quantile=0.05, n_samples=500)

ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, cluster_all=True)
ms.fit(x)
labels = ms.labels_
cluster_centers = ms.cluster_centers_
# 2.1.

# # 2.2. Clustering: DBSCAN
# # Adjust the size of the rectangle based on the template image size
# template_w, template_h = templateImage.shape[:2]
# dbscan = DBSCAN(eps=template_w, min_samples=5)  # Adjust the eps and min_samples parameters accordingly
# dbscan.fit(des2)
# labels = dbscan.labels_
# # 2.2.

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)
print("number of estimated clusters : %d" % n_clusters_)

s = [None] * n_clusters_
for i in range(n_clusters_):
    # 2.1. Clustering: MeanShift
    l = ms.labels_
    d, = np.where(l == i)
    # 2.1.

    # # 2.2. Clustering: DBSCAN
    # d, = np.where(labels == i)
    # # 2.2.

    print(d.__len__())
    s[i] = list(kp2[xx] for xx in d)

des2_ = des2

for i in range(n_clusters_):
    kp2 = s[i]
    # 2.1. Clustering: MeanShift
    l = ms.labels_
    d, = np.where(l == i)
    # 2.1.

    # # 2.2. Clustering: DBSCAN
    # d, = np.where(labels == i)
    # # 2.2.

    des2 = des2_[d, ]

    # 3. Feature Matching: FLANN
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    des1 = np.float32(des1)
    des2 = np.float32(des2)

    matches = flann.knnMatch(des1, des2, 2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good)>3:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 2)

        if M is None:
            print ("No Homography")
        else:
            matchesMask = mask.ravel().tolist()

            h,w,_ = templateImage.shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,M)

            backgroundImage = cv2.polylines(backgroundImage,[np.int32(dst)],True,255,3, cv2.LINE_AA)
            # backgroundImage = cv2.fillPoly(backgroundImage, [np.int32(dst)], color=(255, 255, 255))


            draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                               singlePointColor=None,
                               matchesMask=matchesMask,  # draw only inliers
                               flags=2)

            img3 = cv2.drawMatches(templateImage, kp1, backgroundImage, kp2, good, None, **draw_params)

            cv2.imwrite(file_name + "_gray_" + str(i) + ".png", img3)

    else:
        print ("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
        matchesMask = None