import os
import matplotlib.pyplot as plt
import cv2
import numpy as np

# path and name of the image
# datapath = os.path.abspath("")
datapath = os.path.dirname(os.path.realpath(__file__))
imagename =  'IMG_20191015_181243'

#str(input('Name data image: ')) 2_Zuschnitt_HelligkeitFarbe#'IMG_20191015_181243'IMG_3751_crop

def fn_read_points (image_points,control_points):
    imagepoints = list()
    controlpoints = list()
    raw_image_list = image_points.split('\n')
    raw_control_list = control_points.split('\n')

    for line in raw_image_list:
        line_sep = line.split(";")
        line_sep[0] = float(line_sep[0])
        line_sep[1] = float(line_sep[1])
        imagepoints.append(line_sep)

    for line in raw_control_list:
        line_sep = line.split(";")
        line_sep[0] = float(line_sep[0])
        line_sep[1] = float(line_sep[1])
        controlpoints.append(line_sep)
        
    return     imagepoints,controlpoints


def fn_rectify (datapath,imagename,image_points,control_points,plus_rows,plus_cols):
    # image_file = '%s\\%s' % (datapath,imagename)
    image_file = imagename
    print(image_file)
    image = plt.imread(image_file)#open the image file
    rows, cols = image.shape[:2]#get the size of the image
    
    [imagepoints,controlpoints] = fn_read_points(image_points,control_points)#get the measured points    
    controlpoints = np.array(controlpoints, dtype=np.float32)#transform to an array
    imagepoints = np.array(imagepoints, dtype=np.float32)#transform to an array
    
    M = cv2.getPerspectiveTransform(imagepoints[0:4],controlpoints[0:4])#calculate the transformation matrix
    e_image = cv2.warpPerspective(image,M,(rows+int(plus_rows),cols+int(plus_cols)))#calculate the new image
    
    # e_image_file = '%s\\02_rectify.png' % (datapath)#save transformed image
    e_image_file = '02_rectify.png'
    plt.imsave(e_image_file,e_image)
    
    return e_image