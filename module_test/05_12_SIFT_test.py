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
        if m.distance < 0.75 * n.distance:
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
            cluster_points = keypoints[labels == label]

            # Calculate the bounding rectangle for the cluster
            x, y, w, h = cv2.boundingRect(cluster_points)
            
            x -= template_w // 2
            y -= template_h // 2
            w += template_w
            h += template_h

            # Apply scale and rotation based on template and background feature points
            template_center = (template_w // 2, template_h // 2)
            background_center = (x + w // 2, y + h // 2)
            scale_factor = np.sqrt((template_w * template_w + template_h * template_h) / (w * w + h * h))
            rotation_angle = np.arctan2(template_center[1] - background_center[1], template_center[0] - background_center[0])

            # Rotate the rectangle
            M = cv2.getRotationMatrix2D(background_center, np.degrees(rotation_angle), scale_factor)
            rect_points = np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], dtype=np.float32)
            rect_points = np.hstack((rect_points, np.ones((4, 1))))
            rect_points = np.dot(M, rect_points.T).T[:, :2].astype(np.int32)

            # Draw a rectangle around the cluster in the background image
            background_img = cv2.polylines(background_img, [rect_points], isClosed=True, color=(0, 255, 0), thickness=2)
            # background_img = cv2.fillPoly(background_img, [rect_points], color=(255, 255, 255))
        


    else:
        print('Not enough good matches are found - {}/{}'.format(len(filtered_matched_lists), 0))

    result_img = cv2.drawMatchesKnn(template_img, features1, background_img, features2, matches_list, None, flags=2)
    cv2.imwrite(file_name + "_detect.png", result_img)
    cv2.imwrite(file_name + "_generated.png", background_img)


file_name = "module_test\\result\\20220112_162232_rect_crop_bilateral_crop"
image_name = file_name + ".png"

backgroundImage = cv2.imread(image_name)
templateImage = cv2.imread(file_name + '_template2.png')

match_feature_find_object(templateImage, backgroundImage, 2)