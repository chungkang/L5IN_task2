# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 23:37:44 2021

@author: kfl
"""

import numpy as np
import math as m

def vectorize(datapath,imagename): # method to transform the neighbor relationship to lines
    
    N8_file = '%s/N8/%s_n8.txt' % (datapath,imagename) # load neighbor relationship
    n8_image = np.loadtxt(N8_file, delimiter=';')
    
    
    rows, cols = n8_image.shape[:2] # get size of matrix
    
    L = list() # new matrix for first filtered lines
    L0 = list() # new matrix for outfiltered lines
    
    for k in range (0,rows-1,1): # in range of the matrix size
        for l in range(0,cols-1,1):
            
            n8_value = int(n8_image[k,l]) # get the value of the neighbor relationship
            
            if n8_value > 0: # if there is a relationship
                
                n8_num = [int(i) for i in str(n8_value)] # split binary code into seperate numbers
                
                if n8_num[3] == 1: # if neighbor three is true
                    
                    ay = k # get starting point
                    ax = l
                    
                    ex,ey,n8_image = line3(ay,ax,n8_image,cols) # search end point
                    
                    dx = ex - ax # calculate the length
                    f = 3 # direction of the line
                    
                    if dx > 1:
                        L.append([ax,ay,ex,ey,dx,f]) # set in filtered matrix
                    else:
                        L0.append([ax,ay,ex,ey,dx,f]) # set in outfiltered matrix
                
                if n8_num[4] == 1: # if neighbor four is true
                    
                    ay = k# get starting point
                    ax = l
                    
                    ex,ey,n8_image = line4(ay,ax,n8_image,cols,rows) # search end point
                    
                    dx = ex - ax
                    dy = ey - ay
                    
                    c = m.sqrt(dx**2 + dy**2) # calculate the length
                    f = 4 # direction of the line
                    
                    if c > m.sqrt(2):
                        L.append([ax,ay,ex,ey,c,f]) # set in filtered matrix
                    else:
                        L0.append([ax,ay,ex,ey,c,f]) # set in outfiltered matrix
                
                if n8_num[5] == 1: # if neighbor five is true
                    
                    ay = k# get starting point
                    ax = l
                    
                    ex,ey,n8_image = line5(ay,ax,n8_image,rows) # search end point
                    
                    dy = ey - ay # calculate the length
                    f = 5 # direction of the line
                    
                    if dy > 1:
                        L.append([ax,ay,ex,ey,dy,f]) # set in filtered matrix
                    else:
                        L0.append([ax,ay,ex,ey,dy,f]) # set in outfiltered matrix
                
                if n8_num[6] == 1: # if neighbor six is true
                    
                    ay = k# get starting point
                    ax = l
                    
                    ex,ey,n8_image = line6(ay,ax,n8_image,rows) # search end point
                    
                    dx = ex - ax
                    dy = ey - ay
                    
                    c = m.sqrt(dx**2 + dy**2) # calculate the length
                    f = 6 # direction of the line
                    
                    if c > m.sqrt(2):
                        L.append([ax,ay,ex,ey,c,f]) # set in filtered matrix
                    else:
                        L0.append([ax,ay,ex,ey,c,f]) # set in outfiltered matrix
    
    L = np.array(L, dtype=np.float32) # transform list to array
    L0 = np.array(L0, dtype=np.float32) # transform list to array
    
    L_file = '%s/Lines/%s_L.csv' % (datapath,imagename) # save the arrays
    np.savetxt(L_file,L, delimiter=';')
    L0_file = '%s/Lines/%s_L0.csv' % (datapath,imagename)
    np.savetxt(L0_file,L0, delimiter=';')
                        
    return  L,L0

def line3(ay,ax,n8_image,cols): # method to calculate the endpoint for horizontal lines
    
    if ax < cols-1: # if not right side
        
        wx = ax + 1 # possible endpoint
        wy = ay
        
        n8_value = int(n8_image[wy,wx]) # get the value of the neighbor relationship
        
        if n8_value > 0: # if there is a relationship
            
            n8_num = [int(i) for i in str(n8_value)] # split binary code into seperate numbers
            
            if n8_num[3] == 1: # only if neighbor three is true
                
                ex,ey,n8_image = line3(wy,wx,n8_image,cols) # search next possible end point
                
                n8_image[wy,wx] = n8_image[wy,wx] - 100000 # change binary code to avoid overwriting
            else:
                ex = wx # set endpoint
                ey = wy
        else:
            ex = ax # set endpoint
            ey = ay
    else:
        ex = ax # set endpoint
        ey = ay 
    
    return ex,ey,n8_image

def line4(ay,ax,n8_image,cols,rows): # method to calculate the endpoint for diagonal right lines
    
    if ax < cols-1 and ay < rows-1: # if not right or down side
        
        wx = ax + 1 # possible endpoint
        wy = ay + 1
        
        n8_value = int(n8_image[wy,wx]) # get the value of the neighbor relationship
        
        if n8_value > 0: # if there is a relationship
            
            n8_num = [int(i) for i in str(n8_value)] # split binary code into seperate numbers
            
            if n8_num[4] == 1: # only if neighbor four is true
                
                ex,ey,n8_image = line4(wy,wx,n8_image,cols,rows) # search next possible end point
                
                n8_image[wy,wx] = n8_image[wy,wx] - 10000 # change binary code to avoid overwriting
            else:
                ex = wx # set endpoint
                ey = wy
        else:
            ex = ax # set endpoint
            ey = ay
    else:
        ex = ax # set endpoint
        ey = ay 
    
    return ex,ey,n8_image

def line5(ay,ax,n8_image,rows): # method to calculate the endpoint for vertical lines 
    
    if ay < rows - 1: # if not  left side
        
        wx = ax # possible endpoint
        wy = ay + 1
        
        n8_value = int(n8_image[wy,wx]) # get the value of the neighbor relationship
        
        if n8_value > 0: # if there is a relationship
            
            n8_num = [int(i) for i in str(n8_value)] # split binary code into seperate numbers
            
            if n8_num[5] == 1: # only if neighbor five is true
                
                ex,ey,n8_image = line5(wy,wx,n8_image,rows) # search next possible end point
                
                n8_image[wy,wx] = n8_image[wy,wx] - 1000 # change binary code to avoid overwriting
            else:
                ex = wx # set endpoint
                ey = wy
        else:
            ex = ax # set endpoint
            ey = ay
    else:
        ex = ax # set endpoint
        ey = ay 
    
    return ex,ey,n8_image

def line6(ay,ax,n8_image,rows): # method to calculate the endpoint for diagonal left lines
    
    if ax != 0 and ay < rows-1: # if not left or down side
        
        wx = ax - 1 # possible endpoint
        wy = ay + 1
        
        n8_value = int(n8_image[wy,wx]) # get the value of the neighbor relationship
        
        if n8_value > 0: # if there is a relationship
            
            n8_num = [int(i) for i in str(n8_value)] # split binary code into seperate numbers
            
            if n8_num[6] == 1: # only if neighbor six is true
                
                ex,ey,n8_image = line6(wy,wx,n8_image,rows) # search next possible end point
                
                n8_image[wy,wx] = n8_image[wy,wx] - 100 # change binary code to avoid overwriting
            else:
                ex = wx # set endpoint
                ey = wy
        else:
            ex = ax # set endpoint
            ey = ay
    else:
        ex = ax # set endpoint
        ey = ay 
    
    return ex,ey,n8_image


