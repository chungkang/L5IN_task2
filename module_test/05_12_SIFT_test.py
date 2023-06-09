# https://www.kaggle.com/code/dataenergy/object-recognition-using-feature-matching
# old code 2023.06.09
import cv2
import numpy as np
from sklearn.cluster import DBSCAN, MeanShift, estimate_bandwidth

MIN_MATCH_COUNT = 2

file_name = "module_test\\result\\IMG_3751_rect_crop_bilateral"
image_name = file_name + ".png"

backgroundImage = cv2.imread(image_name)
templateImage = cv2.imread(file_name + '_template1.png')

# 1. Feature Extraction: SIFT
sift = cv2.SIFT_create()

# find the keypoints and descriptors
features1, des1 = sift.detectAndCompute(templateImage, None)
features2, des2 = sift.detectAndCompute(backgroundImage, None)

# Feature Matching: FLANN
# bf = cv2.BFMatcher(cv2.NORM_L2)
# matches = bf.knnMatch(des1, des2, k=2)

FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary
flann = cv2.FlannBasedMatcher(index_params,search_params)
matches = flann.knnMatch(des1,des2,k=2)

# Nearest neighbour ratio test to find good matches
matches_list = []
filtered_matched_lists = []
matches = [match for match in matches if len(match) == 2]
# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in range(len(matches))]

# for m, n in matches:
for i,(m,n) in enumerate(matches):
    if m.distance < 0.8 * n.distance:
        matches_list.append([m])
        filtered_matched_lists.append(m)
        matchesMask[i]=[1,0]

if len(filtered_matched_lists) > 0:
    # Cluster the keypoints
    keypoints = np.float32([features2[m.trainIdx].pt for m in filtered_matched_lists])

    # Adjust the size of the rectangle based on the template image size
    template_w, template_h = templateImage.shape[:2]
    # distance from template -> eps
    dbscan = DBSCAN(eps=template_w, min_samples=MIN_MATCH_COUNT)  # Adjust eps and min_samples as needed
    labels = dbscan.fit_predict(keypoints)
    unique_labels = np.unique(labels)

    for label in unique_labels:
        # Draw a polygon around the recognized object
        # pixel coordinates of the keypoints from the que
        # src_pts = np.float32([features1[m.queryIdx].pt for m in filtered_matched_lists]).reshape(-1, 1, 2)
        src_pts = np.float32([features1[m.queryIdx].pt for m, lbl in zip(filtered_matched_lists, labels) if lbl == label]).reshape(-1, 1, 2)

        cluster_points = keypoints[labels == label].reshape(-1, 1, 2)
        
        # Skip clusters with fewer than 4 points
        if len(src_pts) < 4 or len(cluster_points) < 4:
            continue

        # Get the transformation matrix
        M, _ = cv2.findHomography(src_pts, cluster_points, cv2.RANSAC, 5.0)

        # Apply perspectiveTransform()
        pts = np.float32([[-5, -5], [-5, template_h + 5], [template_w + 5, template_h + 5], [template_w + 5, -5]]).reshape(-1, 1, 2)
        dst_pts = cv2.perspectiveTransform(pts, M)

        # Draw a rectangle around the cluster in the background image
        background_img = cv2.polylines(background_img, [dst_pts.astype(np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)
        # background_img = cv2.fillPoly(background_img, [dst_pts.astype(np.int32)], color=(255, 255, 255))
    
else:
    print('Not enough good matches are found - {}/{}'.format(len(filtered_matched_lists), 0))

result_img = cv2.drawMatchesKnn(templateImage, features1, background_img, features2, matches_list, None, flags=2)
cv2.imwrite(file_name + "_detect.png", result_img)
cv2.imwrite(file_name + "_generated.png", background_img)

draw_params = dict(matchColor = (0,255,0),
                singlePointColor = (255,0,0),
                matchesMask = matchesMask,
                flags = cv2.DrawMatchesFlags_DEFAULT)
img3 = cv2.drawMatchesKnn(templateImage,features1,background_img,features2,matches,None,**draw_params)
cv2.imwrite(file_name + "_points.png", img3)
