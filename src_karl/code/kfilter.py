# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 22:40:28 2021

@author: kfl
"""

import numpy as np
import math as m

def kfilter(datapath,imagename): # method to filter the lines
    
    L_file = '%s/Lines/%s_L.txt' % (datapath,imagename) # load created lines
    L = np.loadtxt(L_file, delimiter=';')
    L0_file = '%s/Lines/%s_L0.txt' % (datapath,imagename)
    L0 = np.loadtxt(L0_file, delimiter=';')
    
    L_all = np.vstack([L,L0]) # matrix with all lines
    
    rows_L,cols_L = L.shape[:2] # get size of the matrices
    rows_L0,cols_L0 = L0.shape[:2]
    
    L_filter = list() # create new matrices for filtered and unfiltered lines 
    L0_filter = list()
    
    for i in range(0,rows_L,1): # for all lines in the filtered matrix
        
        line = False
        L_value = L[i,:] # get line
        
        if L_value[5] == 3: # if a horizontal line
            line = filter3(L_value,i,L_all,line) # check if the line will be filtered
        
        elif L_value[5] == 5: # if a diagonal right line
            line = filter5(L_value,i,L_all,line) # check if the line will be filtered
        
        elif L_value[5] == 4: # if a vertical line
            line = filter46(L_value,i,L_all,line) # check if the line will be filtered
        
        elif L_value[5] == 6: # if a diagonal left line
            line = filter46(L_value,i,L_all,line) # check if the line will be filtered
        
        if line == False: # if the line will be unfiltered
            L0_filter.append(L_value) # set in unfiltered matrix
        else: # if the line will be filtered
            L_filter.append(L_value) # set in filtered matrix
            
    L_filter = np.array(L_filter, dtype=np.float32) # transform list to array
    L0_filter = np.array(L0_filter, dtype=np.float32) # transform list to array
    
    L_filter0 = list() # create new matrices for filtered and unfiltered lines   
    L0_filter0 = list()
            
    for i in range(0,rows_L0,1): # for all lines in the unfiltered matrix
        
        line = False
        L_value = L0[i,:] # get line
        
        if L_value[5] == 3: # if a horizontal line
            line = filter3(L_value,i,L_filter,line) # check if the line will be filtered
        
        elif L_value[5] == 5: # if a diagonal right line
            line = filter5(L_value,i,L_filter,line) # check if the line will be filtered
        
        elif L_value[5] == 4: # if a vertical line
            line = filter46(L_value,i,L_filter,line) # check if the line will be filtered
        
        elif L_value[5] == 6: # if a diagonal left line
            line = filter46(L_value,i,L_filter,line) # check if the line will be filtered
        
        if line == False: # if the line will be unfiltered
            L0_filter0.append(L_value) # set in unfiltered matrix
        else: # if the line will be filtered
            L_filter0.append(L_value) # set in filtered matrix
            
    L_filter0 = np.array(L_filter0, dtype=np.float32) # transform list to array
    L0_filter0 = np.array(L0_filter0, dtype=np.float32) # transform list to array
    
    L_all_filter = np.vstack([L_filter,L_filter0]) # mixed the filtered matrices
    L0_all_filter = np.vstack([L0_filter,L0_filter0]) # mixed the unfiltered matrices
    
    Lfilter_file = '%s/Filtered/%s_L.txt' % (datapath,imagename) # save the matrices
    np.savetxt(Lfilter_file,L_all_filter, delimiter=';')
    L0filter_file = '%s/Filtered/%s_L0.txt' % (datapath,imagename)
    np.savetxt(L0filter_file,L0_all_filter, delimiter=';')
            
    return L_all_filter, L0_all_filter


def filter3(L_value,i,L_all,line): # methode to check if the line will be filtered
    
    if L_value[4] > 3: # check the length
        line = True # filter the line
        return line
    
    find_row,find_col = np.where(L_all == L_value[1]) # search for lines with same value
    
    rows = find_row.shape[0] # get size of matrix
    
    for j in range(0,rows,1): # for all lines in the found lines
        
        if find_row[j] != i: # if not self line
            
            if L_all [find_row[j],0] == L_value[0]: # if start point a other start point
                if L_all [find_row[j],1] == L_value[1]:
                    
                    if L_value[4] > 1: # if lenght bigger than 1 
                        line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                        return line
                        
                    else:
                        if L_all [find_row[j],5] == 3 or L_all [find_row[j],5] == 5: # if bordering line horizontal or vertical
                            if L_all [find_row[j],4] > 2:
                                line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                                return line
                        else:
                            if  L_all [find_row[j],4] > m.sqrt(18):
                                line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                                return line
            
            if L_all [find_row[j],2] == L_value[0]: # if start point a other end point
                if L_all [find_row[j],3] == L_value[1]:
                    
                    if L_value[4] > 1: # if lenght bigger than 1 
                        line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                        return line
                        
                    else:
                        if L_all [find_row[j],5] == 3 or L_all [find_row[j],5] == 5: # if bordering line horizontal or vertical
                            if L_all [find_row[j],4] > 2:
                                line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                                return line
                        
                        else:
                            if  L_all [find_row[j],4] > m.sqrt(18):
                                line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                                return line
    
    return line

def undefilter35(L_value,i,L_all,line,rows,find_row): # methode to check if endpoint is bordering
    
    for k in range(0,rows,1): # for all lines in the found lines
        
        if find_row[k] != i: # if not self line
            
            if L_all[find_row[k],0] == L_value[2]: # if end point a other start point
                if L_all[find_row[k],1] == L_value[3]:
                    
                    if L_value[4] > 1: # if lenght bigger than 1 
                        line = True # filter the line
                        return line
                        
                    else:
                        if L_all [find_row[k],5] == 3 or L_all [find_row[k],5] == 5: # if bordering line horizontal or vertical
                            if L_all [find_row[k],4] > 2:
                                line = True # filter the line
                                return line
                        else:
                            if  L_all [find_row[k],4] > m.sqrt(18):
                                line = True # filter the line
                                return line
                            
            if L_all[find_row[k],2] == L_value[2]:# if end point a other end point
                if L_all[find_row[k],3] == L_value[3]:
                    
                    if L_value[4] > 1: # if lenght bigger than 1 
                        line = True # filter the line
                        return line
                        
                    else:
                        if L_all [find_row[k],5] == 3 or L_all [find_row[k],5] == 5: # if bordering line horizontal or vertical
                            if L_all [find_row[k],4] > 2:
                                line = True # filter the line
                                return line
                        else:
                            if  L_all [find_row[k],4] > m.sqrt(18):
                                line = True # filter the line
                                return line
    
    return line

def filter5(L_value,i,L_all,line): # methode to check if the line will be filtered
    
    if L_value[4] > 3:
        line = True # filter the line
        return line
    
    find_row,find_col = np.where(L_all == L_value[0])  # search for lines with same value
    
    rows = find_row.shape[0] # get size of matrix
    
    for j in range(0,rows,1): # for all lines in the found lines
        
        if find_row[j] != i: # if not self line
            
            if L_all [find_row[j],0] == L_value[0]:# if start point a other start point
                if L_all [find_row[j],1] == L_value[1]:
                    
                    if L_value[4] > 1: # if lenght bigger than 1 
                        line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                        return line
                        
                    else:
                        if L_all [find_row[j],5] == 3 or L_all [find_row[j],5] == 5: # if bordering line horizontal or vertical
                            if L_all [find_row[j],4] > 2:
                                line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                                return line
                        else:
                            if  L_all [find_row[j],4] > m.sqrt(18):
                                line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                                return line
            
            if L_all [find_row[j],2] == L_value[0]: # if start point a other end point
                if L_all [find_row[j],3] == L_value[1]:
                    
                    if L_value[4] > 1: # if lenght bigger than 1 
                        line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                        return line
                        
                    else:
                        if L_all [find_row[j],5] == 3 or L_all [find_row[j],5] == 5: # if bordering line horizontal or vertical
                            if L_all [find_row[j],4] > 2:
                                line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                                return line
                        else:
                            if  L_all [find_row[j],4] > m.sqrt(18):
                                line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                                return line
    
    return line

def filter46(L_value,i,L_all,line): # methode to check if the line will be filtered
      
    find_row,find_col = np.where(L_all == L_value[0]) # search for lines with same value
    
    rows = find_row.shape[0] # get size of matrix
    
    for j in range(0,rows,1): # for all lines in the found lines
        
        if find_row[j] != i: # if not self line
            
            if L_all [find_row[j],0] == L_value[0]: # if start point a other start point
                if L_all [find_row[j],1] == L_value[1]:
                    
                    if L_value[4] <= m.sqrt(18):
                        
                        if L_all [find_row[j],5] == 3 or L_all [find_row[j],5] == 5: # if bordering line horizontal or vertical
                            if L_all [find_row[j],4] > 2:
                                n = 1
                                line = undefilter46(L_value,i,L_all,line,n) # check the endpoint
                                return line
                        else:
                            if  L_all [find_row[j],4] > m.sqrt(18):
                                n = 1
                                line = undefilter46(L_value,i,L_all,line,n) # check the endpoint
                                return line
                        
                    else:
                        n = 0
                        line = undefilter46(L_value,i,L_all,line,n) # check the endpoint
                        return line
            
            if L_all [find_row[j],2] == L_value[0]: # if start point a other end point
                if L_all [find_row[j],3] == L_value[1]:
                    
                    if L_value[4] <= m.sqrt(18):
                        
                        if L_all [find_row[j],5] == 3 or L_all [find_row[j],5] == 5: # if bordering line horizontal or vertical
                            if L_all [find_row[j],4] > 2:
                                n = 1
                                line = undefilter46(L_value,i,L_all,line,n) # check the endpoint
                                return line
                        else:
                            if  L_all [find_row[j],4] > m.sqrt(18):
                                n = 1
                                line = undefilter46(L_value,i,L_all,line,n) # check the endpoint
                                return line
                        
                    else:
                        n = 0
                        line = undefilter46(L_value,i,L_all,line,n) # check the endpoint
                        return line
    
    return line



def undefilter46(L_value,i,L_all,line,n): # methode to check if endpoint is bordering
    
    find_row,find_col = np.where(L_all == L_value[2]) # search for lines with same value
    
    rows = find_row.shape[0] # get size of matrix
    
    for k in range(0,rows,1): # for all lines in the found lines
        
        if find_row[k] != i: # if not self line
            
            if L_all[find_row[k],0] == L_value[2]: # if end point a other start point
                if L_all[find_row[k],1] == L_value[3]:
                    
                    if n == 0:
                        line = True # filter the line
                        return line
                    
                    else:
                        if L_all [find_row[k],5] == 3 or L_all [find_row[k],5] == 5: # if bordering line horizontal or vertical
                            if L_all [find_row[k],4] > 2:
                                line = True # filter the line
                                return line
                        else:
                            if  L_all [find_row[k],4] > m.sqrt(18):
                                line = True # filter the line
                                return line
                            
            if L_all[find_row[k],2] == L_value[2]: # if end point a other end point
                if L_all[find_row[k],3] == L_value[3]:
                    
                    if n == 0:
                        line = True # filter the line
                        return line
                    
                    else:
                        if L_all [find_row[k],5] == 3 or L_all [find_row[k],5] == 5: # if bordering line horizontal or vertical
                            if L_all [find_row[k],4] > 2:
                                line = True # filter the line
                                return line
                        else:
                            if  L_all [find_row[k],4] > m.sqrt(18):
                                line = True # filter the line
                                return line
    
    return line

