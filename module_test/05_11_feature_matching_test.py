# https://www.kaggle.com/code/dataenergy/object-recognition-using-feature-matching

import cv2
import numpy as np
from sklearn.cluster import DBSCAN

# Function to match features and find the object
def match_feature_find_object(template_img, background_img, min_matches):
    # Create a SIFT object
    sift = cv2.SIFT_create()

    features1, des1 = sift.detectAndCompute(template_img, None)
    features2, des2 = sift.detectAndCompute(background_img, None)

    # # Create Brute-Force matcher object
    # bf = cv2.BFMatcher(cv2.NORM_L2)
    # matches = bf.knnMatch(des1, des2, k=2)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)

    # Nearest neighbour ratio test to find good matches
    matches_list = []
    filtered_matched_lists = []
    matches = [match for match in matches if len(match) == 2]
    for m, n in matches:
        if m.distance < 0.9 * n.distance:
            matches_list.append([m])
            filtered_matched_lists.append(m)

    if len(filtered_matched_lists) > 0:
        # Cluster the keypoints
        keypoints = np.float32([features2[m.trainIdx].pt for m in filtered_matched_lists])

        # Adjust the size of the rectangle based on the template image size
        template_w, template_h = template_img.shape[:2]
        # distance from template -> eps
        dbscan = DBSCAN(eps=template_w, min_samples=min_matches)  # Adjust eps and min_samples as needed
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
            pts = np.float32([[-7, -7], [-7, template_h + 7], [template_w + 7, template_h + 7], [template_w + 7, -7]]).reshape(-1, 1, 2)
            dst_pts = cv2.perspectiveTransform(pts, M)

            # Draw a rectangle around the cluster in the background image
            background_img = cv2.polylines(background_img, [dst_pts.astype(np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)
            # background_img = cv2.fillPoly(background_img, [dst_pts.astype(np.int32)], color=(255, 255, 255))
        
    else:
        print('Not enough good matches are found - {}/{}'.format(len(filtered_matched_lists), 0))

    result_img = cv2.drawMatchesKnn(template_img, features1, background_img, features2, matches_list, None, flags=2)
    cv2.imwrite(file_name + "_detect.png", result_img)
    cv2.imwrite(file_name + "_generated.png", background_img)


file_name = "module_test\\result\\IMG_3751_rect_crop_bilateral"
image_name = file_name + ".png"

backgroundImage = cv2.imread(image_name)
templateImage = cv2.imread(file_name + '_template1.png')

match_feature_find_object(templateImage, backgroundImage, 2)