# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:58:28 2022

@author: gurut
"""


"""
File's workFlow 

Text > Bitmap > binary > hex > protocol conversion > checksum conversion > socket > send

"""

# text to bitmap

import numpy as np
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont

img = Image.new('L', (8, 240))
d = ImageDraw.Draw(img)
fnt = ImageFont.truetype("Arial.ttf", 15)
d.text((1,1), "ROC",1,  align='center', font = fnt)
img.save('pil_text.png')


im = Image.open('pil_text.png').convert('1')
im2arr = np.array(img) # im2arr.shape: height x width x channel
arr2im = Image.fromarray(im2arr)



ax = sns.heatmap(im2arr)   



# bitmap to binary to hex

tempStorage = ""
Storebin2String = []

for ImgArrayData in im2arr:
    for data in ImgArrayData:
        tempStorage = tempStorage + str(data)
        #print(data)
    Storebin2String.append(str(tempStorage))
    tempStorage = ""

Storebin2Hex = []
for data in Storebin2String:
    bin2hex = hex(int(data, 2))
    print(bin2hex)
    if bin2hex=='0x0':
        bin2hex = bin2hex[2:]+'0'   
    else:
        bin2hex = bin2hex[2:]
    Storebin2Hex.append(bin2hex)    


# Protocol Conversion


headerOfProtocol = "02-3A-51-48-57-52-47-00-00-A1-03-A0-00-00-00-00-14-00-00-00-03-D0-01-E0-"

fotterOfProtocol = "A3-C4-03-2A"

protocolDisplayData = ""

for hexData in Storebin2Hex:
    protocolDisplayData = protocolDisplayData + hexData+"-"

AllDataOfProtocol = headerOfProtocol + protocolDisplayData + fotterOfProtocol


#Checksum

splitDataOfFullData = AllDataOfProtocol.split("-")

for r in range(0,len(splitDataOfFullData)):
    #g = g+bytes(splitData[r], 'Utf-8') 
    splitDataOfFullData[r] = bytes(splitDataOfFullData[r], 'Utf-8') 

    
import numpy as np
arrayDataofProtocol = np.asarray(splitDataOfFullData) 

import crc16
checksumData = hex(crc16.crc16xmodem(arrayDataofProtocol[1:-2]))
print(checksumData)


# Merging of protocol with checksum

checksumDataPart1 = checksumData[2:4]
checksumDataPart2 = checksumData[4:]
checksumDataModified = checksumDataPart1 +"-"+checksumDataPart2

AllDataOfProtocol = AllDataOfProtocol + checksumDataModified


