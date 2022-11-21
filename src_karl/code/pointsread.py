# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 15:07:12 2021

@author: kfl
"""

def read_points (datapath,imagename):
    
    ip_file = '%s/Passpunkte/%s_mp.txt' % (datapath,imagename)#create file path for image points
    cp_file = '%s/Passpunkte/%s_fp.txt' % (datapath,imagename)#create file path for control points
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