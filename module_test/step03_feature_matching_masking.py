# https://stackoverflow.com/questions/42938149/opencv-feature-matching-multiple-objects?noredirect=1&lq=1

import cv2
import numpy as np
from sklearn.cluster import DBSCAN, MeanShift, estimate_bandwidth

MIN_MATCH_COUNT = 4
MATCH_DISTANCE = 0.7
NUMBER_OF_TEMPLATES = 7
PAD = 7 # padding of template

file_name = "module_test\\result\\2OG_1_result"
image_name = file_name + ".png"

backgroundImage = cv2.imread(image_name)

sift = cv2.SIFT_create(
    nfeatures=0,        # Maximum number of keypoints to retain
    nOctaveLayers=3,     # Number of octave layers within each scale octave
    contrastThreshold=0.04,  # Threshold to filter out weak keypoints
    edgeThreshold=20,    # Threshold for edge rejection
    sigma=1.2            # Standard deviation of Gaussian blur applied to the input image
)

# template
for template_num in range(1, NUMBER_OF_TEMPLATES + 1):
    # Load template image
    templateImage = cv2.imread(file_name + '\\' + str(template_num) + '.png')

    # 1. Feature Extraction: SIFT
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(templateImage, None)
    kp2, des2 = sift.detectAndCompute(backgroundImage, None)

    # 2. Clustering: MeanShift
    x = np.array([kp2[0].pt])

    for i in range(len(kp2)):
        x = np.append(x, [kp2[i].pt], axis=0)

    x = x[1:len(x)]

    bandwidth = estimate_bandwidth(x, quantile=0.05, n_samples=500)

    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, cluster_all=True)
    ms.fit(x)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)
    print("number of estimated clusters : %d" % n_clusters_)

    s = [None] * n_clusters_
    for i in range(n_clusters_):
        l = ms.labels_
        d, = np.where(l == i)
        print(d.__len__())
        s[i] = list(kp2[xx] for xx in d)

    des2_ = des2

    for i in range(n_clusters_):
        kp2 = s[i]
        l = ms.labels_
        d, = np.where(l == i)
        des2 = des2_[d, ]

        # 3. Feature Matching: FLANN
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 100)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        des1 = np.float32(des1)
        des2 = np.float32(des2)

        matches = flann.knnMatch(des1, des2, 2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m,n in matches:
            if m.distance < MATCH_DISTANCE * n.distance:
                good.append(m)

        if len(good) >= MIN_MATCH_COUNT:
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 2)

            if M is None:
                print ("No Homography")
            else:
                matchesMask = mask.ravel().tolist()

                h,w,_ = templateImage.shape
                pts = np.float32([ [-PAD,-PAD],[-PAD,h+PAD],[w+PAD,h+PAD],[w+PAD,-PAD] ]).reshape(-1,1,2)
                dst = cv2.perspectiveTransform(pts,M)

                # backgroundImage = cv2.polylines(backgroundImage,[np.int32(dst)],True,255,3, cv2.LINE_AA)
                backgroundImage = cv2.fillPoly(backgroundImage, [np.int32(dst)], color=(255, 255, 255))

                draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                                singlePointColor=None,
                                matchesMask=matchesMask,  # draw only inliers
                                flags=2)

                # img3 = cv2.drawMatches(templateImage, kp1, backgroundImage, kp2, good, None, **draw_params)
                # cv2.imwrite(file_name + "_" + str(i) + ".png", img3)
                cv2.imwrite(file_name + "\\match_" + str(template_num) + "_" + str(i) + ".png", backgroundImage)
                


        else:
            print ("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
            matchesMask = None


# # Need to draw only good matches, so create a mask
# matchesMask = [[0,0] for i in range(len(matches))]
# # ratio test as per Lowe's paper
# for i,(m,n) in enumerate(matches):
#     if m.distance < 0.7 * n.distance:
#         matchesMask[i]=[1,0]
# draw_params = dict(matchColor = (0,255,0),
#                 singlePointColor = (255,0,0),
#                 matchesMask = matchesMask,
#                 flags = cv2.DrawMatchesFlags_DEFAULT)
# img3 = cv2.drawMatchesKnn(templateImage,kp1,backgroundImage,kp2,matches,None,**draw_params)

# cv2.imwrite(file_name + "_test.png", img3)