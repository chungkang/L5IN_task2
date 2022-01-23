# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 23:27:02 2021

@author: kfl
"""

import os
from plantcv import plantcv as pcv
import numpy as np
import winsound
import cv2
import glob
import imutils

import non_max_suppression_fast as non


def binary_2(datapath,imagename,rectify):
    
    if rectify == True:
        image_file = '%s/Entzerrt/%s_adjusted.jpg' % (datapath,imagename)#create file path for transformed image
        image = plt.imread(image_file)#open transformed image
    else:
        image_file = '%s/Bilder/%s.jpg' % (datapath,imagename)#create file path for transformed image
        image = plt.imread(image_file)#open transformed image
    
    corrected_img = pcv.transform.nonuniform_illumination(img=image, ksize=31)
    
    rows, cols = corrected_img.shape[:2]#get size of the image
    bin_image = np.zeros(shape=(rows,cols))#create new matrix with zeros
    
    for i in range(0,rows,1):#for all rows in the image
        for j in range(0,cols,1):#for all collums in the image
            pixel= corrected_img[i,j]#get the RGB-values for the pixel 
            if np.sum(pixel) > 220:#transform to binary data (only for IMG_20191015_181243)
                bin_image[i,j] = 1
            else:
                bin_image[i,j] = 0
                
    bin_image_file = '%s/Binaer/%s_binaer.txt' % (datapath,imagename)#save binary code
    np.savetxt(bin_image_file,bin_image, delimiter=';')
    
    return bin_image




































winsound.Beep(frequency, duration)