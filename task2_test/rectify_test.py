import os
import matplotlib.pyplot as plt
import cv2
import numpy as np

# path and name of the image
# datapath = os.path.abspath("")
datapath = os.path.dirname(os.path.realpath(__file__))
imagename =  'IMG_20191015_181243'

#str(input('Name data image: ')) 2_Zuschnitt_HelligkeitFarbe#'IMG_20191015_181243'IMG_3751_crop

def read_points (datapath,imagename):
    ip_file = '%s\\%s_mp.txt' % (datapath,imagename)#create file path for image points
    cp_file = '%s\\%s_fp.txt' % (datapath,imagename)#create file path for control points
    imagepoints_file = open (ip_file,'r') #open the data from file
    
    imagepoints = list()
    for line in imagepoints_file:#write image points
        line_sep = line.split(";")
        line_sep[0] = float(line_sep[0])
        line_sep[1] = float(line_sep[1].replace('\n', ''))
        imagepoints.append(line_sep)
    
    controlpoints_file = open (cp_file,'r') #open the data from file
    
    controlpoints = list()
    for line in controlpoints_file:#write control points
        line_sep = line.split(";")
        line_sep[0] = float(line_sep[0])
        line_sep[1] = float(line_sep[1].replace('\n', ''))
        controlpoints.append(line_sep)
        
    return     imagepoints,controlpoints


def rectify (datapath,imagename,plus_rows,plus_cols):
    
    image_file = '%s\\%s.jpg' % (datapath,imagename)
    print(image_file)
    image = plt.imread(image_file)#open the image file
    rows, cols = image.shape[:2]#get the size of the image
    
    [imagepoints,controlpoints] = read_points (datapath,imagename)#get the measured points    
    controlpoints = np.array(controlpoints, dtype=np.float32)#transform to an array
    imagepoints = np.array(imagepoints, dtype=np.float32)#transform to an array
    
    M = cv2.getPerspectiveTransform(imagepoints[0:4],controlpoints[0:4])#calculate the transformation matrix
    e_image = cv2.warpPerspective(image,M,(rows+plus_rows,cols+plus_cols))#calculate the new image
    
    e_image_file = '%s_adjusted.jpg' % (imagename)#save transformed image
    plt.imsave(e_image_file,e_image)
    
    return e_image




rectify (datapath,imagename,1100,-2500)