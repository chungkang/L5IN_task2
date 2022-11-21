40# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 23:01:24 2021

@author: kfl
"""
import numpy as np


def newfilter(datapath,imagename): # method to filter the lines
    
    L_file = '%s/Lines/%s_L.txt' % (datapath,imagename) # load filtered lines
    L_filter = np.loadtxt(L_file, delimiter=';')
    L0_file = '%s/Lines/%s_L0.txt' % (datapath,imagename)
    L0_filter = np.loadtxt(L0_file, delimiter=';')    
    
    L_new = list() # create new matrices for filtered and unfiltered lines 
    
    rows = L0_filter.shape[0] # get size of the matrices
    
    for i in range(0,rows): # for all lines in the unfiltered matrix
    
        L0_value = L0_filter[i,:] # get line
        
        line = L0filter(L0_value,L_filter,i) # check if the line will be filtered
        
        if line == True: # if the line will be filtered
            L_new.append(L0_value) # set in filtered matrix
            
    L_all = np.vstack([L_filter,L_new]) # join the filtered lines to the input lines
    
    Lall_file = '%s/Filtered/%s_L_all.txt' % (datapath,imagename) # save the matrix
    np.savetxt(Lall_file,L_all, delimiter=';')
        
    return L_all

def thirdfilter(datapath,imagename): # method to filter the lines
    
    L_all_file = '%s/Filtered/%s_L_all.txt' % (datapath,imagename) # load filtered lines
    L_all = np.loadtxt(L_all_file, delimiter=';')    
    
    L_new = list() # create new matrices for filtered and unfiltered lines 
    rows = L_all.shape[0] # get size of the matrices
    
    for i in range(0,rows): # for all lines in the unfiltered matrix
    
        L_all_value = L_all[i,:] # get line
        
        line = L0filter(L_all_value,L_all,i) # check if the line will be filtered
        
        if line == True: # if the line will be filtered
            L_new.append(L_all_value)   # set in filtered matrix
    
    L_third_file = '%s/Filtered/%s_L_thr.txt' % (datapath,imagename) # save the matrix
    np.savetxt(L_third_file,L_new, delimiter=';')
        
    return L_new

def L0filter(L0_value,L_filter,i): # methode to check if the line will be filtered
    
    line = False # value that indicates whether the line is filtered or not
    
    find_row,find_col = np.where(L_filter == L0_value[1]) # search for lines with same value
    
    rows = find_row.shape[0] # get size of matrix
    
    for j in range(0,rows,1): # for all lines in the found lines
        
        if find_row[j] != i: # if not self line
            
            if L_filter [find_row[j],0] == L0_value[0]: # if start point a other start point
                if L_filter [find_row[j],1] == L0_value[1]:
                    
                    line = L0underfilter(L0_value,i,L_filter) # check the endpoint
                
                if line == True: # filter the line
                    return line
                
            if L_filter [find_row[j],2] == L0_value[0]: # if start point a other end point
                if L_filter [find_row[j],3] == L0_value[1]:
                    
                    line = L0underfilter(L0_value,i,L_filter) # check the endpoint
                
                if line == True: # filter the line
                    return line
                
    return line

def L0underfilter(L0_value,i,L_filter): # methode to check if endpoint is bordering
    
    line = False # value that indicates whether the line is filtered or not
    
    find_row,find_col = np.where(L_filter == L0_value[3]) # search for lines with same value
    
    rows = find_row.shape[0] # get size of matrix
    
    for j in range(0,rows,1): # for all lines in the found lines
        
        if find_row[j] != i: # if not self line
            
            if L_filter [find_row[j],0] == L0_value[2]: # if end point a other start point
                if L_filter [find_row[j],1] == L0_value[3]:
                    
                    line = True # filter the line
                    return line
                
            if L_filter [find_row[j],2] == L0_value[2]: # if end point a other end point
                if L_filter [find_row[j],3] == L0_value[3]:
                    
                    line = True # filter the line
                    return line
                
    return line
    
    