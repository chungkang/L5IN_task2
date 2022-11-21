# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 22:13:47 2021

@author: kfl
"""

import os
from plantcv import plantcv as pcv
import numpy as np
import cv2

import non_max_suppression_fast as non


def symbolfinder(img,template_fa):# to find the templates
    pcv.params.debug = "print"
    imageGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# transform picturer into gray
    templateGray = cv2.cvtColor(template_fa, cv2.COLOR_BGR2GRAY)# transform template into gray 
    templateGray = pcv.transform.nonuniform_illumination(img=templateGray, ksize=31)
    (tH, tW) = templateGray.shape[:2]
    method = cv2.TM_CCOEFF_NORMED
    rects = list()
    result = cv2.matchTemplate(imageGray, templateGray,	method) # find the spots where the template in the picture
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)# get some Values out of the result
    (startX, startY) = np.where(result >= maxVal-(maxVal+minVal))# set the spots where the result value is above a threshold 
    for (x, y) in zip(startX, startY):
        rects.append((x, y, x + tW, y + tH))# find the koordinates of the found templates
    return rects,result

def symbolseraser(img,template_fa,img0):# turn the found tamplates into white
    rects,result = symbolfinder(img,template_fa)
    pick = non.non_max_suppression(np.array(rects))
    for (startX, startY, endX, endY) in pick:
        cv2.rectangle(img0, (startY, startX), (endY, endX),(255, 255, 255), -1)    
    return img0,result

def symbolremoveall(datapath,imagename):
    image_file = '%s/Entzerrt/%s_adjusted.jpg' % (datapath,imagename)
    img = cv2.imread(image_file)
    img0 = cv2.imread(image_file)
    template_names = ['rescue_man','fire_alarm','rescue_arrow']
# remove all symbols like the templates
    for i in range(0,3):
        template_file_fa = './Template/%s.jpg'% (template_names[i])
        template_fa = cv2.imread(template_file_fa)
        img0,result = symbolseraser(img,template_fa,img0)    
    return img0,result

