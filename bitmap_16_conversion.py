# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:58:28 2022

@author: gurut
"""


"""
File's workFlow 

Text > Bitmap > binary > hex > protocol conversion > checksum conversion > socket > send

"""


import numpy as np
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont
import socket
import PIL

img = Image.new('L', (16, 256))
d = ImageDraw.Draw(img)
#fnt = ImageFont.truetype("Arial.ttf", 15)
#d.text((1,1), "P",1,  align='center', font = fnt)

text1 = "A---\nA---"
text10 = "ABC\nZZZ"
text2 = "oZ\nk\na\ny\no\nk\na\ny"
text3 = "1\n2\n3\n4\n5\n6\n7\n7\n9\n1\n2\n3\n4\n5\n6\n7\n7\n9\n1\n2\n3\n4\n5\n6\n7\n7\n9"

d.text((1,3), text10,1) #, font = fnt)
img.save('pil_text.png')


im = Image.open('pil_text.png').convert('L')

# img = im.transpose(PIL.Image.FLIP_TRANSPOSE)
# img = im.rotate(PIL.Image.FLIP_TRANSPOSE)
# ax = sns.heatmap(img) 

# img = im.transpose(Image.FLIP_LEFT_RIGHT)
# ax1 = sns.heatmap(img) 

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
    print("Data = ", data, "Length of data ",len(data))
    bin2hex = hex(int(data, 2))
    if bin2hex=='0x0':
        bin2hex = bin2hex[2:]+'0'
        print("0x0 loop", bin2hex)
    else:
        bin2hex = bin2hex[2:]
        print("DAta(bin) conversion inti hex ", bin2hex)
    Storebin2Hex.append(bin2hex)    


# Protocol Conversion


headerOfProtocol = "02-3A-51-48-57-52-47-00-00-A1-03-A0-00-00-00-00-14-00-00-00-03-D0-01-E0-"

fotterOfProtocol = "A3-C4-03-"

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





# UDP FILE TRANSFER OF ALL DATA

splitData = AllDataOfProtocol.split("-")



bufferString = ""

for r in range(0,len(splitData)):
    bufferString = bufferString + splitData[r]
    
    
    
little_hex = bytearray.fromhex(bufferString)
#little_hex.reverse()
print("Byte array format:", little_hex)


TCP_IP = "192.168.1.95"
TCP_PORT = 9999
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(little_hex)
s.close()
#data = s.recv(BUFFER_SIZE)
print ("received data:") #, data)



    



