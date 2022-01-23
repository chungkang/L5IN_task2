# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 22:42:06 2021

@author: kfl
"""
import matplotlib.pyplot as plt

# import some needed methods
import winsound
import os
import pointsread as pr
import rectify as r
import binary as b
import neighbors as n
import vectorize as v
import kfilter as f
import secfilter as secf
#import filter01 as ff

# only for a singal, that the code is done
frequency = 1700  # Set Frequency To 2500 Hertz
duration = 300  # Set Duration To 1000 ms == 1 second

# path and name of the image
datapath = os.path.abspath("../data/")
imagename =  'IMG_3751_crop'#str(input('Name data image: ')) 2_Zuschnitt_HelligkeitFarbe#'IMG_20191015_181243'IMG_3751_crop


# rectify the image (only if it is needed)
e_image = r.rectify (datapath,imagename,1100,-2500)

# transforme to an binary image (False if no rectify is done, True when some rectify is done)
bin_image = b.binary(datapath,imagename,True)
plt.figure()
plt.imshow(bin_image)

# calculate the neighbor relationship
bildn8 = n.image_n8 (datapath,imagename)
plt.figure(1)
plt.imshow(bildn8)

# calculate all Lines
L,L0 = v.vectorize(datapath,imagename)

#both are variable applicable for the generated lines
#plot the lines
plt.figure(2)
plt.axis('equal') 
for i in range(len(L)):
    plt.plot([L[i,0],L[i,2]],[-L[i,1],-L[i,3]],'-b')
for i in range(len(L0)):
    plt.plot([L0[i,0],L0[i,2]],[-L0[i,1],-L0[i,3]],'-k')



# first Line filter
L_filter, L0_filter = f.kfilter(datapath,imagename)
#L_filter, L0_filter = ff.kfilter(datapath,imagename)

plt.figure(1)
plt.axis('equal')
for i in range(len(L_filter)):
    plt.plot([L_filter[i,0],L_filter[i,2]],[-L_filter[i,1],-L_filter[i,3]],'-b')

plt.figure(2)
plt.axis('equal')
for i in range(len(L_filter)):
    plt.plot([L_filter[i,0],L_filter[i,2]],[-L_filter[i,1],-L_filter[i,3]],'-b')
for i in range(len(L0_filter)):
    plt.plot([L0_filter[i,0],L0_filter[i,2]],[-L0_filter[i,1],-L0_filter[i,3]],'-k')

# second Line flter
L_new = secf.newfilter(datapath,imagename)




# make a sound
winsound.Beep(frequency, duration)
    
    


