# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 18:26:05 2022

@author: gurut
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
import PySimpleGUI as sg



class SignalBitmapDisplay:      
    
    def __init__(self, ip, port, fontSize, counter, stationName, display = False, fontStyle= None, language = None, overFlowDisplay = False,   **kwargs):
        self.ip = ip
        self.port = port
        #self.text = text
        self.fontSize = fontSize
        self.display = display    
        self.fontStyle = fontStyle
        self.language = language
        self.counter = counter
        self.stationName = stationName
        self.overFlowDisplay = overFlowDisplay
        
        
    def output(self):
        
        
        ip, port, fontSize, overFlowDisplay, fontStyle, language, counter, stationName, display = self.ip, self.port,  self.fontSize, self.overFlowDisplay, self.fontStyle, self.language, self.counter, self.stationName , self.display  
        

    
    # ip, port, text, fontSize, display, fontStyle, language= ip, port, text, fontSize, display, fontStyle, language    
    

    
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
        
        
        
        print("\nIP = ", ip, "\nPort = ", port, "\nText = ", stationName,  "Counter ", counter,"\nFont = ", fontPath[language][fontStyle], "\nFontSize = ", fontSize, "\n")
        
        
        font = fontPath[language][fontStyle]
        
        
        img = Image.new('L', (180, 20))
        d = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(font, fontSize) #max 12 fontsize
        
        text = stationName 
                
        d.text((2,3), text , 1, font = fnt)
        #sns.heatmap(img)
        
        #create img for Time
        
        imgCounter = Image.new('L', (60, 20))
        dimgCounter = ImageDraw.Draw(imgCounter)
        fnt = ImageFont.truetype(font, fontSize) #max 12 fontsize
        
        text = counter   
                
        dimgCounter.text((2,3), text , 1, font = fnt)
        
        # sns.heatmap(imgCounter)
        
        newImageDataCounter = Image.new('L', (img.width+imgCounter.width, img.height))
        
        newImageDataCounter.paste(img, (0,0))
        
        newImageDataCounter.paste(imgCounter, (img.width, 0))
        
        
        #sns.heatmap(newImageDataCounter)
               
        
        imgOverflow = Image.new('L', (480, 20))
        e = ImageDraw.Draw(imgOverflow)
        fnt = ImageFont.truetype(font, fontSize) #max 12 fontsize    
        e.text((2,3), text , 1, font = fnt)
        OverFlowImage = np.array(imgOverflow)
        
        
        img = newImageDataCounter
        
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
        
        #overFlow of data
        
        
        
        
        imgOverFlowDataString = Image.new('L', (480, 20))
        dx = ImageDraw.Draw(imgOverFlowDataString)
        fnt = ImageFont.truetype(font, fontSize) #max 12 fontsize
        
        text = stationName   
                
        dx.text((2,3), text , 1, font = fnt)
        
        #sns.heatmap(imgOverFlowDataString)
        
        
        imgOverFlowData = np.array(imgOverFlowDataString)
        
        setVariable = True
        
        for overFlow in imgOverFlowData[:, 162:]:
            for checkOverFlow in overFlow:
                if checkOverFlow == True:
                    print("\n\n Data is Overflowing \n\n")
                    setVariable = False
                    break
            if setVariable == False and overFlowDisplay == True:
                j = Image.fromarray(imgOverFlowData[:, 162:])
                x = j.transpose(Image.FLIP_LEFT_RIGHT)
                x = j.transpose(Image.ROTATE_90)
                x = x.transpose(Image.ROTATE_90)
                x = x.transpose(Image.ROTATE_90)
                x = x.transpose(Image.ROTATE_90)
                y = np.array(x)
                sns.heatmap(y).set(title='OverFlow Data Map')
                sg.Popup('Opps!', 'Data is OverFlowing')
                break
                    
            
        
        
        
        
        if display == True:
            fig, axes = plt.subplots(ncols=2, figsize=(10, 10)) 
            fig.suptitle("1. BitmapData(Lt)" + "\n2. DisplayData(Rt)")        
            imgFlip90 = img.transpose(Image.ROTATE_90)
            sns.heatmap(imgFlip90, ax=axes[0])             
            sns.heatmap(im2arrMerged, ax=axes[1]) #, annot = True)
        
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
        print ("MESSAGE SENT SUCCESFULLY") #, data) 
            
    
    
    
    
     
    
# ip = "192.168.1.93";
# port = 9999

# fontSize = 10
# overFlowDisplay = True
# display = True
# language = "English" 
# fontStyle = "poppinsNormal"   

# counter = ": 02"
# stationName = "Jawaharlal Nehru Statdium"
# stationName2 = "Mandi House"

    
# #ip, port, fontSize, display = False, fontStyle= None, language = None,counter, stationName, overFlowDisplay = False,         

# jnlHindi = "नेहरु स्टेडियम"
# mndHouseHindi = ""

# stationList = ["Jawaharlal Nehru Statdium ghjuhgfghjikjuhgfghjiuhguytgfgyhut", jnlHindi , "Mandi House", mndHouseHindi]

# lineIp = ["192.168.1.93", "192.168.1.94"]


# for data in range(0, 2):
#     stName = stationList[data]
    
#     for counter in range(1,6):
        
#         counterDataM = ": 0{}".format(counter)
        
#         x = SignalBitmapDisplay(ip = lineIp[0], port = port, fontSize = 10, overFlowDisplay = False, display = False, language = "English", fontStyle = "poppinsNormal" , counter = counterDataM, stationName = stationList[0])
#         x.output()
        
#     for counter in range(1,6):
        
#         counterData = ": 0{}".format(counter)
        
        
#         y = SignalBitmapDisplay(ip = lineIp[0], port = port, fontSize = 10, overFlowDisplay = False, display = False, language = "Hindi", fontStyle = "poppinsNormal" , counter = counterData, stationName = stationList[1])
#         y.output()
        
         
        
        


          
# # x = SignalBitmapDisplay(ip = ip, port = port, fontSize = 10, overFlowDisplay = True, display = True, language = "Hindi", fontStyle = "poppinsNormal" , counter = counter, stationName = stationName2)    


    
    
    
    
    
    
    
    
    
    
