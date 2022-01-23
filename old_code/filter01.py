# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 22:40:28 2021

@author: kfl
"""

import numpy as np
import math as m

def kfilter(datapath,imagename): # method to filter the lines
    
    L_file = '%s/Lines/%s_L_all.csv' % (datapath,imagename) # load created lines
    L_all = np.loadtxt(L_file, delimiter=';')
    # L0_file = '%s/Lines/%s_L0.csv' % (datapath,imagename)
    # L0 = np.loadtxt(L0_file, delimiter=';')
    
    # L_all = np.vstack([L,L0]) # matrix with all lines
    
    rows_L,cols_L = L_all.shape[:2] # get size of the matrix
    
    L_filter = list() # create new matrices for filtered and unfiltered lines 
    L0_filter = list()
    L_wkt = list()
    L0_wkt = list()
    
    for i in range(0,rows_L,1): # for all lines in the filtered matrix
        
        line = False
        L_value = L_all[i,:] # get line
        
        if L_value[5] == 3: # if a horizontal line
            line = filter35(L_value,i,L_all,line) # check if the line will be filtered
        
        elif L_value[5] == 5: # if a diagonal right line
            line = filter35(L_value,i,L_all,line) # check if the line will be filtered
        
        elif L_value[5] == 4: # if a vertical line
            line = filter46(L_value,i,L_all,line) # check if the line will be filtered
        
        elif L_value[5] == 6: # if a diagonal left line
            line = filter46(L_value,i,L_all,line) # check if the line will be filtered
        
        if line == False: # if the line will be unfiltered
            L0_filter.append(L_value) # set in unfiltered matrix
            L0_wkt.append(f'LINESTRING({L_value[0]} {L_value[1]}, {L_value[2]} {L_value[3]})')
        else: # if the line will be filtered
            L_filter.append(L_value) # set in filtered matrix
            L_wkt.append(f'LINESTRING({L_value[0]} {L_value[1]}, {L_value[2]} {L_value[3]})')
            
    L_filter = np.array(L_filter, dtype=np.float32) # transform list to array
    L0_filter = np.array(L0_filter, dtype=np.float32) # transform list to array
    
        
    # Lfilter_file = '%s/Filtered/%s_L_01.csv' % (datapath,imagename) # save the matrices
    # np.savetxt(Lfilter_file,L_filter, delimiter=';')
    # L0filter_file = '%s/Filtered/%s_L0_01.csv' % (datapath,imagename)
    # np.savetxt(L0filter_file,L0_filter, delimiter=';')
    Lfilter_file = '%s/Filtered/%s_L_01.wkt' % (datapath,imagename) # save the arrays
    with open(Lfilter_file, 'w') as output:
        for row in L_wkt:
            output.write(str(row) + '\n')
    L0filter_file = '%s/Filtered/%s_L0_01.wkt' % (datapath,imagename) # save the arrays
    with open(L0filter_file, 'w') as output:
        for row in L0_wkt:
            output.write(str(row) + '\n')
    
            
    return L_filter, L0_filter


def filter35(L_value,i,L_all,line): # methode to check if the line will be filtered
    
    if L_value[4] > 5: # check the length
        line = True # filter the line
        return line
    
    find_row,find_col = np.where(L_all == L_value[1]) # search for lines and collums with same y-value as value
    
    rows = find_row.shape[0] # get size of matrix
    
    for j in range(0,rows,1): # for all lines in the found lines
        
        if find_row[j] != i: # if not self line
            
            if L_all [find_row[j],0] == L_value[0]: # if start point a other start point
                if L_all [find_row[j],1] == L_value[1]:
                    
                    if L_value[4] > 1: # if lenght bigger than 1 
                        # line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                        line = True # filter the line
                        return line
                        
                    else:
                        if L_all [find_row[j],5] == 3 or L_all [find_row[j],5] == 5: # if bordering line horizontal or vertical
                            if L_all [find_row[j],4] > 1:
                            # line = True
                                line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                            # return line
                        else:
                            if  L_all [find_row[j],4] > m.sqrt(2):
                                line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                            # return line
            
            if L_all [find_row[j],2] == L_value[0]: # if start point a other end point
                if L_all [find_row[j],3] == L_value[1]:
                    
                    if L_value[4] > 1: # if lenght bigger than 1 
                        line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                        # line = True # filter the line
                        # return line
                        
                    else:
                        if L_all [find_row[j],5] == 3 or L_all [find_row[j],5] == 5: # if bordering line horizontal or vertical
                            if L_all [find_row[j],4] > 1:
                            # line = True
                                line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                            # return line
                        
                        else:
                            if  L_all [find_row[j],4] > m.sqrt(2):
                                line = undefilter35(L_value,i,L_all,line,rows,find_row) # check the endpoint
                            # return line
    
    return line

def undefilter35(L_value,i,L_all,line,rows,find_row): # methode to check if endpoint is bordering
    
    for k in range(0,rows,1): # for all lines in the found lines
        
        if find_row[k] != i: # if not self line
            
            if L_all[find_row[k],0] == L_value[2]: # if end point a other start point
                if L_all[find_row[k],1] == L_value[3]:
                    
                    if L_all [find_row[k],5] == 3 or L_all [find_row[k],5] == 5: # if bordering line horizontal or vertical
                        # if L_all [find_row[k],4] > 1:
                        line = True # filter the line
                        return line
                    else:
                        if  L_all [find_row[k],4] > m.sqrt(2):
                            line = True # filter the line
                        return line
                            
            if L_all[find_row[k],2] == L_value[2]:# if end point a other end point
                if L_all[find_row[k],3] == L_value[3]:
                   
                    if L_all [find_row[k],5] == 3 or L_all [find_row[k],5] == 5: # if bordering line horizontal or vertical
                        # if L_all [find_row[k],4] > 1:
                        line = True # filter the line
                        return line
                    else:
                        if  L_all [find_row[k],4] > m.sqrt(2):
                            line = True # filter the line
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
                                # return line
                        else:
                            if  L_all [find_row[j],4] > m.sqrt(18):
                                n = 1
                                line = undefilter46(L_value,i,L_all,line,n) # check the endpoint
                                # return line
                        
                    else:
                        n = 0
                        line = undefilter46(L_value,i,L_all,line,n) # check the endpoint
                        # return line
            
            if L_all [find_row[j],2] == L_value[0]: # if start point a other end point
                if L_all [find_row[j],3] == L_value[1]:
                    
                    if L_value[4] <= m.sqrt(18):
                        
                        if L_all [find_row[j],5] == 3 or L_all [find_row[j],5] == 5: # if bordering line horizontal or vertical
                            if L_all [find_row[j],4] > 2:
                                n = 1
                                line = undefilter46(L_value,i,L_all,line,n) # check the endpoint
                                # return line
                        else:
                            if  L_all [find_row[j],4] > m.sqrt(18):
                                n = 1
                                line = undefilter46(L_value,i,L_all,line,n) # check the endpoint
                                # return line
                        
                    else:
                        n = 0
                        line = undefilter46(L_value,i,L_all,line,n) # check the endpoint
                        # return line
    
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
                                # return line
                        else:
                            if  L_all [find_row[k],4] > m.sqrt(18):
                                line = True # filter the line
                                # return line
                            
            if L_all[find_row[k],2] == L_value[2]: # if end point a other end point
                if L_all[find_row[k],3] == L_value[3]:
                    
                    if n == 0:
                        line = True # filter the line
                        return line
                    
                    else:
                        if L_all [find_row[k],5] == 3 or L_all [find_row[k],5] == 5: # if bordering line horizontal or vertical
                            if L_all [find_row[k],4] > 2:
                                line = True # filter the line
                                # return line
                        else:
                            if  L_all [find_row[k],4] > m.sqrt(18):
                                line = True # filter the line
                                # return line
    
    return line

