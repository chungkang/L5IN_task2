# https://www.kaggle.com/code/dataenergy/object-recognition-using-feature-matching

import cv2
import numpy as np

# Function to match features and find the object
def match_feature_find_object(template_img, background_img, min_matches): 
    # Create a SIFT object
    sift = cv2.SIFT_create()

    features1, des1 = sift.detectAndCompute(template_img, None)
    features2, des2 = sift.detectAndCompute(background_img, None)

    # Create Brute-Force matcher object
    bf = cv2.BFMatcher(cv2.NORM_L2)
    matches = bf.knnMatch(des1, des2, k = 2)

    # Nearest neighbour ratio test to find good matches
    good = []    
    good_without_lists = []    
    matches = [match for match in matches if len(match) == 2]
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append([m])
            good_without_lists.append(m)
            
    if len(good) >= min_matches:
        # Draw a polygon around the recognized object
        # pixel coordinates of the keypoints from the que
        src_pts = np.float32([features1[m.queryIdx].pt for m in good_without_lists]).reshape(-1, 1, 2)
        dst_pts = np.float32([features2[m.trainIdx].pt for m in good_without_lists]).reshape(-1, 1, 2)
        
        # Get the transformation matrix
        M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                
        # Find the perspective transformation to get the corresponding points
        h, w = template_img.shape[:2]
        pts = np.float32([[-7, -7], [-7, h + 7], [w + 7, h + 7], [w + 7, -7]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)

        # option 1 - only show green rectangle        
        # background_img = cv2.polylines(background_img, [np.int32(dst)], True, (0, 255, 0), 2, cv2.LINE_AA)
        
        # optioon 2 - cover the detected feature with white color
        # Mask the detected feature with white color
        mask = np.zeros_like(background_img, dtype=np.uint8)
        mask = cv2.fillPoly(mask, [np.int32(dst)], (255, 255, 255))
        
        # Apply the mask to remove the symbol from the image
        background_img = cv2.bitwise_or(background_img, mask)

    else:
        print('Not enough good matches are found - {}/{}'.format(len(good), min_matches))
            
    result_img = cv2.drawMatchesKnn(template_img, features1, background_img, features2, good, None, flags = 2)
    cv2.imwrite(file_name + "_detect.png", result_img)
    cv2.imwrite(file_name + "_generated.png", background_img)
    

file_name = "module_test\\result\\IMG_3751_rect_crop_bilateral_crop"
image_name = file_name + ".png"

backgroundImage = cv2.imread(image_name)
templateImage = cv2.imread(file_name + '_template1.png')
# templateImage = cv2.imread( "module_test\\result\\image2-2_crop_bilateral_template1.png")

match_feature_find_object(templateImage, backgroundImage, 2)