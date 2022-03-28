# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 20:36:46 2022

@author: Rochak Sharma
"""


import numpy as np
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont
import socket
import matplotlib.pyplot as plt
import re
import crc16
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

class BitMapMaker:      
    def __init__(self, ip, port, text, fontSize, display = False, fontStyle= None, language = None, **kwargs):
        self.ip = ip
        self.port = port
        self.text = text
        self.language = language
        self.fontSize = fontSize
        self.display = display    
        self.fontStyle = fontStyle
        
        
    def output(self):
        ip, port, text, fontSize, display, fontStyle, language= self.ip, self.port, self.text, self.fontSize, self.display, self.fontStyle, self.language    
        
        fontPath = {
        'English':{
            
                    'arial' : "Fonts/english/arial.ttf",
                    'poppinsBold': 'Fonts/english/Poppins-Bold.ttf',
                    'poppinsItalic': 'Fonts/english/Poppins-Italic.ttf',
                    'poppinsNormal': 'Fonts/english/Poppins-Medium.ttf',        
            },
        
        'Hindi':{
                    'poppinsBold': 'Fonts/english/Poppins-Bold.ttf',
                    'poppinsItalic': 'Fonts/english/Poppins-Italic.ttf',
                    'poppinsNormal': 'Fonts/english/Poppins-Medium.ttf',        
            },
        
        'Kannad':{
                    'maligeBold': 'Fonts/kannad/Malige-b.ttf',
                    'maligeItalic': 'Fonts/kannad/Malige-i.ttf',
                    'maligeNormal': 'Fonts/kannad/Malige-n.ttf',        
            },
        
        }
        
        
        
        print("\nIP = ", ip, "\nPort = ", port, "\nText = ", text, "\nFont = ", fontPath[language][fontStyle], "\nFontSize = ", fontSize, "\n")
        
        
        font = fontPath[language][fontStyle]
        
        
        img = Image.new('L', (240, 20))
        d = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(font, fontSize) #max 12 fontsize
        
        text = text
        
        d.text((2,3), text , 1, font = fnt)
        
        
        img2arrOriginal = np.array(img)
        imgFlip = img.transpose(Image.ROTATE_90)
        imgFlip = imgFlip.rotate(180)
        imgFlip = imgFlip.transpose(Image.FLIP_LEFT_RIGHT)
        im2arrFliped = np.array(imgFlip)
        im2arrFliped = np.delete(im2arrFliped, np.s_[0:2], axis=1)
        j = Image.fromarray(im2arrFliped)
        dst = Image.new('L', (16, 240))
        dst.paste(j, (0, 0))
        im2arrMerged = np.array(dst)
        if display == True:
            fig, axes = plt.subplots(ncols=2, figsize=(10, 10)) 
            fig.suptitle("1. BitmapData(Lt)" + "\n2. DisplayData(Rt)")        
            imgFlip90 = img.transpose(Image.ROTATE_90)
            sns.heatmap(imgFlip90, ax=axes[0])             
            sns.heatmap(im2arrMerged, ax=axes[1])
        
        tempStorage = ""
        Storebin2String = []        
        for ImgArrayData in im2arrMerged:
            for data in ImgArrayData:
                tempStorage = tempStorage + str(data)
                #print(data)
            Storebin2String.append(str(tempStorage))
            tempStorage = ""    
        mergeAllBinary = ""
        for dataB in Storebin2String:
            mergeAllBinary = mergeAllBinary + dataB    
        mergedAllBinary8Bit = re.findall('........', mergeAllBinary)    
        Storebin2Hex = []
        for data in mergedAllBinary8Bit:
            #print("Data = ", data, "Length of data ",len(data))
            bin2hex = hex(int(data, 2))        
            if len(bin2hex[2:]) ==1:    #bin2hex=='0x0' len(bin2hex[2:]) ==1
                #print("0x0 loop", bin2hex)
                bin2hex = '0' + bin2hex[2:]
                #print("loop 1", bin2hex)     
            else:
                bin2hex = bin2hex[2:]
                #print("loop3 ", bin2hex)        
            Storebin2Hex.append(bin2hex)        
        headerOfProtocol = "02-3A-51-48-57-52-47-00-00-A1-03-A0-00-00-00-00-14-00-00-00-03-D0-01-E0-"    
        fotterOfProtocol = "A3-C4-03-"    
        protocolDisplayData = ""    
        for hexData in Storebin2Hex:
            protocolDisplayData = protocolDisplayData + hexData+"-"   
        AllDataOfProtocol = headerOfProtocol + protocolDisplayData + fotterOfProtocol   
        splitDataOfFullData = AllDataOfProtocol.split("-")     
        for r in range(0,len(splitDataOfFullData)):
            splitDataOfFullData[r] = bytes(splitDataOfFullData[r], 'Utf-8') 
        arrayDataofProtocol = np.asarray(splitDataOfFullData) 
        checksumData = hex(crc16.crc16xmodem(arrayDataofProtocol[1:-2]))
        #print(checksumData)        
        checksumDataPart1 = checksumData[2:4]
        checksumDataPart2 = checksumData[4:]
        checksumDataModified = checksumDataPart1 +"-"+checksumDataPart2        
        AllDataOfProtocol = AllDataOfProtocol + checksumDataModified        
        splitData = AllDataOfProtocol.split("-")        
        bufferString = ""        
        for r in range(0,len(splitData)):
            bufferString = bufferString + splitData[r]
        try:    
            little_hex = bytearray.fromhex(bufferString)
        except:
            little_hex = bytearray.fromhex(bufferString[:-1])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.send(little_hex)
        s.close()
        print ("MESSAGE HAS BEEN SENT") #, data)        





fnt_hindi = "Fonts/hindi/Poppins-Medium.ttf" 
fnt_knd = "Fonts/kannad/Noodle-Regular.ttf"
yh = "पोथी पढ़ि पढ़ि जग मुवा, पंडित हुआ न कोय। "
yk = "ದೆಹಲಿ ಮೆಟ್ರೋಗೆ ಸುಸ್ವಾಗತ "
y = "WELCOMES TO DELHI METRO"

#ip, port, text, fontSize, display = False, fontStyle= None, language = None,
x = BitMapMaker(ip = "192.168.1.94", port = 9999, text = y , fontSize = 10, display = True, language = "English", fontStyle = "poppinsItalic") #ip, port, text, font, fontSize, language
x.output()   