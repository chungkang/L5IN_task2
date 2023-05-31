# https://www.kaggle.com/code/dataenergy/object-recognition-using-feature-matching

import cv2
import numpy as np
from sklearn.cluster import DBSCAN
# Import the required libraries
from sklearn.cluster import DBSCAN
import numpy as np

# Function to match features and find the object
def match_feature_find_object(template_img, background_img, min_matches):
    # Create a SIFT object
    sift = cv2.SIFT_create()

    features1, des1 = sift.detectAndCompute(template_img, None)
    features2, des2 = sift.detectAndCompute(background_img, None)

    # Create Brute-Force matcher object
    bf = cv2.BFMatcher(cv2.NORM_L2)
    matches = bf.knnMatch(des1, des2, k=2)

    # Nearest neighbour ratio test to find good matches
    matches_list = []
    filtered_matched_lists = []
    matches = [match for match in matches if len(match) == 2]
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            matches_list.append([m])
            filtered_matched_lists.append(m)

    if len(matches_list) >= min_matches:
        # Cluster the keypoints
        keypoints = np.float32([features2[m.trainIdx].pt for m in filtered_matched_lists])

        # distance from template -> eps
        dbscan = DBSCAN(eps=13, min_samples=3)  # Adjust eps and min_samples as needed
        labels = dbscan.fit_predict(keypoints)

        unique_labels = np.unique(labels)
        for label in unique_labels:
            cluster_points = keypoints[labels == label]
            if len(cluster_points) > 2:
                for point in cluster_points:
                    x, y = np.int32(point)
                    w, h = template_img.shape[:2]
                    x -= w // 2
                    y -= h // 2
                    background_img = cv2.rectangle(background_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    else:
        print('Not enough good matches are found - {}/{}'.format(len(matches_list), min_matches))

    result_img = cv2.drawMatchesKnn(template_img, features1, background_img, features2, matches_list, None, flags=2)
    cv2.imwrite(file_name + "_detect.png", result_img)
    cv2.imwrite(file_name + "_generated.png", background_img)


file_name = "module_test\\result\\20220112_162232_rect_crop_bilateral_crop"
image_name = file_name + ".png"

backgroundImage = cv2.imread(image_name)
templateImage = cv2.imread(file_name + '_template1.png')
# templateImage = cv2.imread( "module_test\\result\\image2-2_crop_bilateral_template1.png")

match_feature_find_object(templateImage, backgroundImage, 2)