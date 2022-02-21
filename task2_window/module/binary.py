import matplotlib.pyplot as plt
import numpy as np

def fn_binary(datapath,imagename,rectify):
    image_file = '%s\\%s' % (datapath,imagename)
    image = plt.imread(image_file)#open transformed image

    rows, cols = image.shape[:2]#get size of the image
    bin_image = np.zeros(shape=(rows,cols))#create new matrix with zeros
    pixel = np.zeros(shape=(1,1,3))
    
    for i in range(0,rows,1):#for all rows in the image
        for j in range(0,cols,1):#for all collums in the image
        
            pixel[0,0,0:3] = image[i,j,0:3]#get the RGB-values for the pixel
            # print(np.max(image[i,j,:]))
            if (np.max(image[i,j,:]) - np.min(image[i,j,:])) > 15:#eliminate red green and blue (only for IMG_20191015_181243)
                pixel[0,0,0:3] = np.array([255, 255, 255], dtype=np.float32)
                # print(pixel)
            # print(np.sum(pixel)-sum(image[i,j,0:3]))  
            if np.sum(pixel) > 100:#transform to binary data (only for IMG_20191015_181243)
                bin_image[i,j] = 1#np.array([1, 1, 1], dtype=np.float32)
            else:
                bin_image[i,j] = 0#np.array([0, 0, 0], dtype=np.float32)
    
    # bin_image_file = '%s/Binaer/%s_binaer.jpg' % (datapath,imagename)#save binary image
    # plt.imsave(bin_image_file,bin_image)
    bin_image_file = '%s\\03_binary.txt' % (datapath)#save binary code
    np.savetxt(bin_image_file,bin_image, delimiter=';')
    
    return bin_image