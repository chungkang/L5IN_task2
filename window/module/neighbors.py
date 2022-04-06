import numpy as np

def fn_image_n8 (datapath,imagename):
    
    bin_image_file = '%s\\%s' % (datapath,imagename)
    bin_image = np.loadtxt(bin_image_file, delimiter=';')

    rows, cols = bin_image.shape[:2]
    n8_image = np.zeros(shape=(rows,cols))#create new matrix with zeros
    
    for i in range(0,rows,1):#for all rows
        for j in range(0,cols,1):#for all collums
            if bin_image[i,j] == 0:#if color of the pixel is black
                if i == 0:#if the first row
                    if j == 0:#if the first collum
                        bild31 = bin_image[i:i+2,j:j+2]#cut out the neighbours
                        print(bild31,31)
                        k = n31(bild31)
                    elif j == cols-1:#if the last collum
                        bild32 = bin_image[i:i+2,j-1:j+1]#cut out the neighbours
                        print(bild32,32)
                        k = n32(bild32)
                    else:#if between the edges
                        bild51 = bin_image[i:i+2,j-1:j+2]#cut out the neighbours
                        print(bild51,51)
                        k = n51(bild51)
                elif i == rows-1:#if the last row
                    if j == 0:#if the first collum
                        bild34 = bin_image[i-1:i+1,j:j+2]#cut out the neighbours
                        print(bild34,34)
                        k = n34(bild34)
                    elif j == cols-1:#if the last collum
                        bild33 = bin_image[i-1:i+1,j-1:j+1]#cut out the neighbours
                        print(bild33,33)
                        k = n33(bild33)
                    else:#if between the edges
                        bild53 = bin_image[i-1:i+1,j-1:j+2]#cut out the neighbours
                        print(bild53,53)
                        k = n53(bild53)
                else:#if between the edges
                    if j == 0:#if the first collum
                        bild54 = bin_image[i-1:i+2,j:j+2]#cut out the neighbours
                        print(bild54,54)
                        k = n54(bild54)
                    elif j == cols-1:#if the last collum
                        bild52 = bin_image[i-1:i+2,j-1:j+1]#cut out the neighbours
                        print(bild52,52)
                        k = n52(bild52)
                    else:#if between the edges
                        bilda = bin_image[i-1:i+2,j-1:j+2]#cut out the neighbours
                        print(bilda,8)
                        k = n8a(bilda)
                        
                # k = n8(bilda, i, j, rows, cols)#get the color of the neighbors
                n8_image[i,j] = k#save the binary code of the neighbours 
            
    N8_file = '%s\\04_neighbors.txt' % (datapath)#save binary code
    np.savetxt(N8_file,n8_image, delimiter=';')
    
    return n8_image

def n8(bilda, i, j, rows, cols):
    if (np.sum(np.sum(bilda))) > 0:
        if i == 0:#if first row
            if j == 0:#if first collum
                k = n31(bilda)
            elif j == cols-1:#if last collum
                k = n32(bilda)
            else:#if between the edges
                k = n51(bilda)
    
        elif i == rows-1:#if the last row
            if j == 0:#if first collum
                k = n34(bilda)
            elif j == cols-1:#if last collum
                k = n33(bilda)
            else:#if between the edges
                k = n53(bilda)
    
        elif j == 0:#if first collum
            k = n52(bilda)
        elif j == cols-1:#if last collum
            k = n54(bilda)
        else:#if between the edges
            k = n8a(bilda)
    else:
        k = 0
    
    return k

def n8a(bilda):
    
    if (np.sum(np.sum(bilda))) > 0:
        
        k = 100000000#nine digit binary code
        
        if bilda[0,1] == 0:#Location 1
            k = k + 10000000
        if bilda[0,2] == 0:#Location 2
            k = k + 1000000
        if bilda[1,2] == 0:#Location 3
            k = k + 100000
        if bilda[2,2] == 0:#Location 4
            k = k + 10000
        if bilda[2,1] == 0:#Location 5
            k = k + 1000
        if bilda[2,0] == 0:#Location 6
            k = k + 100
        if bilda[1,0] == 0:#Location 7
            k = k + 10
        if bilda[0,0] == 0:#Location 8
            k = k + 1
    else:
        k = 0
        
    return k
    
def n31(bilda):
    
    if (np.sum(np.sum(bilda))) > 0:
    
        k = 100000000#nine digit binary code
        
        if bilda[0,1] == 0:#Location 3
            k = k + 100000
        if bilda[1,1] == 0:#Location 4
            k = k + 10000
        if bilda[1,0] == 0:#Location 5
            k = k + 1000
    else:
        k = 0
        
    return k

def n32(bilda):
    
    if (np.sum(np.sum(bilda))) > 0:
    
        k = 100000000#nine digit binary code
        
        if bilda[1,1] == 0:#Location 5
            k = k + 1000
        if bilda[0,1] == 0:#Location 6
            k = k + 100
        if bilda[0,1] == 0:#Location 7
            k = k + 10
        
    else:
        k = 0
    
    return k

def n33(bilda):
    
    if (np.sum(np.sum(bilda))) > 0:
    
        k = 100000000#nine digit binary code
        
        if bilda[0,1] == 0:#Location 1
            k = k + 10000000
        if bilda[1,0] == 0:#Location 7
            k = k + 10
        if bilda[0,0] == 0:#Location 8
            k = k + 1
    
    else:
        k = 0    
    
    return k

def n34(bilda):
    
    if (np.sum(np.sum(bilda))) > 0:
    
        k = 100000000#nine digit binary code
        
        if bilda[0,0] == 0:#Location 1
            k = k + 10000000
        if bilda[0,1] == 0:#Location 2
            k = k + 1000000
        if bilda[1,1] == 0:#Location 3
            k = k + 100000
        
    else:
        k = 0
    
    return k

def n51(bilda):
    
    if (np.sum(np.sum(bilda))) > 0:
    
        k = 100000000#nine digit binary code
        
        if bilda[0,2] == 0:#Location 3
            k = k + 100000
        if bilda[1,2] == 0:#Location 4
            k = k + 10000
        if bilda[1,1] == 0:#Location 5
            k = k + 1000
        if bilda[1,0] == 0:#Location 6
            k = k + 100
        if bilda[0,0] == 0:#Location 7
            k = k + 10
    
    else:
        k = 0    
    
    return k

def n52(bilda):
    
    if (np.sum(np.sum(bilda))) > 0:
    
        k = 100000000#nine digit binary code
        
        if bilda[0,1] == 0:#Location 1
            k = k + 10000000
        if bilda[2,1] == 0:#Location 5
            k = k + 1000
        if bilda[2,0] == 0:#Location 6
            k = k + 100
        if bilda[1,0] == 0:#Location 7
            k = k + 10
        if bilda[0,0] == 0:#Location 8
            k = k + 1
        
    else:
        k = 0
    
    return k

def n53(bilda):
    
    if (np.sum(np.sum(bilda))) > 0:
    
        k = 100000000#nine digit binary code
        
        if bilda[0,1] == 0:#Location 1
            k = k + 10000000
        if bilda[0,2] == 0:#Location 2
            k = k + 1000000
        if bilda[1,2] == 0:#Location 3
            k = k + 100000
        if bilda[1,0] == 0:#Location 7
            k = k + 10
        if bilda[0,0] == 0:#Location 8
            k = k + 1
        
    else:
        k = 0
    
    return k

def n54(bilda):
    
    if (np.sum(np.sum(bilda))) > 0:
    
        k = 100000000#nine digit binary code
        
        if bilda[0,0] == 0:#Location 1
            k = k + 10000000
        if bilda[0,1] == 0:#Location 2
            k = k + 1000000
        if bilda[1,1] == 0:#Location 3
            k = k + 100000
        if bilda[2,1] == 0:#Location 4
            k = k + 10000
        if bilda[2,0] == 0:#Location 5
            k = k + 1000
        
    else:
        k = 0
    
    return k