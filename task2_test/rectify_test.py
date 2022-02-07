import os
import matplotlib.pyplot as plt
import cv2
import numpy as np

import pointsread as pr

# path and name of the image
datapath = os.path.abspath("../data/")
imagename =  'IMG_3751_crop'#str(input('Name data image: ')) 2_Zuschnitt_HelligkeitFarbe#'IMG_20191015_181243'IMG_3751_crop


# rectify the image (only if it is needed)
e_image = r.rectify (datapath,imagename,1100,-2500)



def rectify (datapath,imagename,plus_rows,plus_cols):
    
    image_file = '%s/Bilder/%s.jpg' % (datapath,imagename)#create file path for image
    image = plt.imread(image_file)#open the image file
    rows, cols = image.shape[:2]#get the size of the image
    
    [imagepoints,controlpoints] = pr.read_points (datapath,imagename)#get the measured points    
    controlpoints = np.array(controlpoints, dtype=np.float32)#transform to an array
    imagepoints = np.array(imagepoints, dtype=np.float32)#transform to an array
    
    M = cv2.getPerspectiveTransform(imagepoints[0:4],controlpoints[0:4])#calculate the transformation matrix
    e_image = cv2.warpPerspective(image,M,(rows+plus_rows,cols+plus_cols))#calculate the new image
    
    e_image_file = '%s/Entzerrt/%s_adjusted.jpg' % (datapath,imagename)#save transformed image
    plt.imsave(e_image_file,e_image)
    
    return e_image