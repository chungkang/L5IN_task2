# https://www.kaggle.com/code/dataenergy/object-recognition-using-feature-matching

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Function to display an image using matplotlib
def show_image(img, title, colorspace):
    dpi = 96
    figsize = (img.shape[1] / dpi, img.shape[0] / dpi)
    fig, ax = plt.subplots(figsize = figsize, dpi = dpi)
    if colorspace == 'RGB':
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), interpolation = 'spline16')
    if colorspace == 'gray':
        plt.imshow(img, cmap = 'gray')
    plt.title(title, fontsize = 12)
    ax.axis('off')
    plt.show()


# Function to match features and find the object
def match_feature_find_object(query_img, train_img, min_matches): 
    # Create a SIFT object
    sift = cv2.SIFT_create()

    features1, des1 = sift.detectAndCompute(query_img, None)
    features2, des2 = sift.detectAndCompute(train_img, None)

    # Create Brute-Force matcher object
    bf = cv2.BFMatcher(cv2.NORM_L2)
    matches = bf.knnMatch(des1, des2, k = 2)

    # Nearest neighbour ratio test to find good matches
    good = []    
    good_without_lists = []    
    matches = [match for match in matches if len(match) == 2] 
    for m, n in matches:
        if m.distance < 0.8 * n.distance:
            good.append([m])
            good_without_lists.append(m)
            
    if len(good) >= min_matches:
        # Draw a polygon around the recognized object
        src_pts = np.float32([features1[m.queryIdx].pt for m in good_without_lists]).reshape(-1, 1, 2)
        dst_pts = np.float32([features2[m.trainIdx].pt for m in good_without_lists]).reshape(-1, 1, 2)
        
        # Get the transformation matrix
        M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                
        # Find the perspective transformation to get the corresponding points
        h, w = query_img.shape[:2]
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        
        train_img = cv2.polylines(train_img, [np.int32(dst)], True, (0, 255, 0), 2, cv2.LINE_AA)
        
        # Mask the detected feature with white color
        mask = np.zeros_like(train_img, dtype=np.uint8)
        mask = cv2.fillPoly(mask, [np.int32(dst)], (255, 255, 255))
        
        # Cover the detected feature with white color rectangle
        train_img = cv2.rectangle(train_img, (dst[0][0], dst[0][1]), (dst[2][0], dst[2][1]), (255, 255, 255), -1)

        # # Mask the detected feature with white color
        # mask = np.zeros_like(train_img, dtype=np.uint8)
        # mask = cv2.fillPoly(mask, [np.int32(dst)], (255, 255, 255))
        
        # # Combine the masked image with the original image
        # masked_img = cv2.bitwise_and(train_img, mask)
        
        # # Cover the detected feature with white color
        # train_img = cv2.addWeighted(masked_img, 1, train_img, 0, 0)


    else:
        print('Not enough good matches are found - {}/{}'.format(len(good), min_matches))
            
    result_img = cv2.drawMatchesKnn(query_img, features1, train_img, features2, good, None, flags = 2)
    cv2.imwrite(file_name + "_detect.png", result_img)

    # show_image(mask,'test','RGB')

    # show_image(result_img, 'Feature matching and object recognition', 'RGB')
    


file_name = "module_test\\result\\IMG_3751_rect_crop_bilateral_crop"
image_name = file_name + ".png"

trainImage = cv2.imread(image_name) # trainImage
queryImage = cv2.imread(file_name + '_template1.png') # queryImage
# queryImage = cv2.imread( "module_test\\result\\image2-2_crop_bilateral_template1.png")

match_feature_find_object(queryImage, trainImage, 10)