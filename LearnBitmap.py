# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:58:28 2022

@author: gurut
"""
# from PIL import Image
# import numpy as np
# im = Image.open('1.png').convert('1')
# im = im.resize((240,16), Image.ANTIALIAS)
# im2arr = np.array(im) # im2arr.shape: height x width x chanl
# arr2im = Image.fromarray(im2arr)


# import cv2

# # read the image file
# img = cv2.imread('BITMAP/a.jpg', 2)
# img = cv2.resize(img, (240,16))

# ret, bw_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# # converting to its binary form
# bw = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)



# cv2.imshow("Binary", bw_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

from PIL import Image
import numpy as np
im = Image.open('BITMAP/a.jpg').convert('1')
im = im.resize((240,16), Image.ANTIALIAS)
im2arr = np.array(im) # im2arr.shape: height x width x channel
arr2im = Image.fromarray(im2arr)


import seaborn as sns; sns.set_theme()


ax = sns.heatmap(im2arr)





imgA = "00-00-1C-00-78-00-88-00-F8-00-1C-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00"
imgAList = imgA.split("-")


# from PIL import Image
# import numpy as np
# im = Image.open('e.jpeg').convert('1')
# im = im.resize((240,16), Image.ANTIALIAS)


# array = np.array(im)
# np.savetxt("file.txt", array, fmt="%d")

# ax = sns.heatmap(array)




# array1 = np.array(imgAList)
# int_value = int(imgAList[2], base=16)
# binData = str(bin(int_value))[2:].zfill(8)

# for pixelData in range(0,len(imgAList)):
#     int_value = int(imgAList[pixelData], base=16)
#     binData = bin(int_value)
#     imgAList[pixelData] = binData
 
# array1 = np.array(imgAList)  
# ax = sns.heatmap(array1)   


temp=[]

for data in imgAList:
    print(data)
    my_hexdata = data
    
    scale = 16 ## equals to hexadecimal
    
    num_of_bits = 8
    
    bin(int(my_hexdata, scale))[2:].zfill(num_of_bits)
    
    temp.append(bin(int(my_hexdata, scale))[2:].zfill(num_of_bits))
    
    
import numpy as np


temp2 = []
temp3 = []


for data in temp:
    
    for data2 in data:
     temp2.append(int(data2))
     
    temp3.append(temp2)
    temp2 = []

array1 = np.array(temp3)  
ax = sns.heatmap(array1[:16])   


imgZ ="00-00-1C-00-78-00-88-00-F8-00-1C-00-00-00-00-00-FC-00-A4-00-A4-00-F8-00-00-00-78-00-CC-00-84-00-84-00-48-00-00-00-FC-00-84-00-84-00-CC-00-78-00-00-00-FC-00-A4-00-A4-00-00-00-00-00-FC-00-90-00-90-00-90-00-78-00-CC-00-94-00-94-00-DC-00-00-00-00-00-FC-00-20-00-20-00-20-00-FC-00-00-00-FC-00-00-00-04-00-FC-00-00-00-00-00-FC-00-20-00-50-00-48-00-84-00-FC-00-04-00-04-00-00-00-FC-00-C0-00-38-00-0C-00-38-00-C0-00-FC-00-00-00-00-00-FC-00-C0-00-30-00-0C-00-FC-00-00-00-78-00-C4-00-84-00-84-00-8C-00-78-00-00-00-00-00-FC-00-90-00-90-00-60-00-78-00-C4-00-84-00-84-00-8C-00-7E-00-02-00-00-00-FC-00-90-00-98-00-E4-00-00-00-64-00-A4-00-94-00-98-00-00-00-80-00-80-00-FC-00-80-00-80-00-00-00-F8-00-04-00-04-00-04-00-F8-00-00-00-00-00-E0-00-1C-00-04-00-1C-00-E0-00-00-00-F8-00-04-00-7C-00-C0-00-7C-00-04-00-F8-00-00-00-00-00-CC-00-30-00-CC-00-00-00-00-00-80-00-60-00-1C-00-60-00-80-00-8C-00-94-00-A4-00-C4-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00" 
imgZ = imgZ.split("-")

temp=[]

for data in imgZ:
    print(data)
    my_hexdata = data
    
    scale = 16 ## equals to hexadecimal
    
    num_of_bits = 8
    
    bin(int(my_hexdata, scale))[2:].zfill(num_of_bits)
    
    temp.append(bin(int(my_hexdata, scale))[2:].zfill(num_of_bits))
    
    
import numpy as np


temp2 = []
temp3 = []


for data in temp:
    
    for data2 in data:
     temp2.append(int(data2))
     
    temp3.append(temp2)
    temp2 = []
import seaborn as sns; sns.set_theme()
array1 = np.array(temp3)  
ax = sns.heatmap(array1[:100])   




#hex(int('010110', 2))





####### custom bitmaps

p = "00000000 00000000 01111110 01000010 01000010 01000010 01000010 01111110 01000000 01000000 01000000 01000000"

letterP = p.split(" ")


temp=[]

for data in letterP:
    print(data)
    my_hexdata = data
      
    temp.append(data)
    
    
import numpy as np


temp2 = []
temp3 = []


for data in temp:
    
    for data2 in data:
     temp2.append(int(data2))
     
    temp3.append(temp2)
    temp2 = []
    
    
import seaborn as sns; sns.set_theme()
array1 = np.array(temp3)  
ax = sns.heatmap(array1)   



#letter P test




imgP ="00-00-00-00-FC-00-90-00-90-00-60-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00" 
imgP = imgP.split("-")

temp=[]

for data in imgP:
    print(data)
    my_hexdata = data
    
    scale = 16 ## equals to hexadecimal
    
    num_of_bits = 8
    
    bin(int(my_hexdata, scale))[2:].zfill(num_of_bits)
    
    temp.append(bin(int(my_hexdata, scale))[2:].zfill(num_of_bits))
    
    
import numpy as np


temp2 = []
temp3 = []


for data in temp:
    
    for data2 in data:
     temp2.append(int(data2))
     
    temp3.append(temp2)
    temp2 = []
import seaborn as sns; sns.set_theme()
array1 = np.array(temp3)  
ax = sns.heatmap(array1[:90])   

"""
https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
https://stackoverflow.com/questions/56056346/how-to-convert-text-to-bitmap-of-text-not-binary
"""

from PIL import Image, ImageDraw, ImageFont

img = Image.new('L', (240, 16))
d = ImageDraw.Draw(img)
fnt = ImageFont.truetype("Arial.ttf", 15)
d.text((1,1), "P",255, font = fnt)
img.save('pil_text.png')


im = Image.open('pil_text.png').convert('1')
im2arr = np.array(im) # im2arr.shape: height x width x channel
arr2im = Image.fromarray(im2arr)

ax = sns.heatmap(im2arr)   

