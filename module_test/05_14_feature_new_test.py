import cv2
import numpy as np
from sklearn.cluster import DBSCAN, MeanShift, estimate_bandwidth
import copy

MIN_MATCH_COUNT = 4
MATCH_DISTANCE = 0.7

# 0. read input image
file_name = "module_test\\result\\20230608_110853_bilateral"
image_name = file_name + ".png"

templateImage = cv2.imread(file_name + '_template'+'1.png')
backgroundImage = cv2.imread(image_name)

# 1. Feature Extraction: SIFT
sift = cv2.SIFT_create(
    nfeatures=0,        # Maximum number of keypoints to retain
    nOctaveLayers=3,     # Number of octave layers within each scale octave
    contrastThreshold=0.04,  # Threshold to filter out weak keypoints
    edgeThreshold=20,    # Threshold for edge rejection
    sigma=1.2            # Standard deviation of Gaussian blur applied to the input image
)

# 2. iteration of whole image/update image
iterationFlag = True  # when the image has no cluster which has more than 4 matched points, stop the iteration
while iterationFlag:
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(templateImage, None)
    kp2, des2 = sift.detectAndCompute(backgroundImage, None)

    # 2.1. Feature Matching
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=100)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    des1 = np.float32(des1)
    des2 = np.float32(des2)

    matches = flann.knnMatch(des1, des2, 2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < MATCH_DISTANCE * n.distance:
            good.append(m)

    if len(good) >= MIN_MATCH_COUNT:
        # 2.2. Clustering with DBSCAN with threshold of template size
        template_w, template_h = templateImage.shape[:2]
        dbscan = DBSCAN(eps=template_w, min_samples=5)  # Adjust the eps and min_samples parameters accordingly
        dbscan.fit(des2)
        labels = dbscan.labels_

        labels_unique, counts = np.unique(labels, return_counts=True)
        cluster_with_most_points = labels_unique[np.argmax(counts)]

        # 2.3. Get the most matched cluster which has the largest feature points
        d, = np.where(labels == cluster_with_most_points)

        # 2.4. Matching Homography (Masking)
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 2)

        if M is None:
            print("No Homography")
        else:
            matchesMask = mask.ravel().tolist()

            h, w, _ = templateImage.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            backgroundImage = cv2.fillPoly(backgroundImage, [np.int32(dst)], color=(255, 255, 255))
            # backgroundImage = cv2.polylines(backgroundImage, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

        # 2.5. Save image with the best match removed
        mask = mask.ravel()
        filtered_matches = [good[i] for i in range(len(good)) if mask[i]]
        matchesMask = [matchesMask[i] for i in range(len(matchesMask)) if mask[i]]  # Update matchesMask

        draw_params = dict(matchColor=(0, 255, 0), singlePointColor=None, matchesMask=matchesMask, flags=2)
        cv2.imwrite(file_name + "_result.png", backgroundImage)

        iterationFlag = False  # Stop the iteration
    else:
        iterationFlag = False  # Stop the iteration


