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
import threading
import logging
import os
logging.basicConfig(filename="Logs2.log", format='%(asctime)s %(message)s', filemode='w')

logger = logging.getLogger()

logger.setLevel(logging.ERROR)

logger.error("OverFlow Data Map Right")


class SignalBitmapDisplay:      
    
    def __init__(self, ip, port, fontSize, counter, stationName, sysFont , display = False, fontStyle= None, language = None, overFlowDisplay = False,   **kwargs):
        self.ip = ip
        self.port = port
        #self.text = text
        self.fontSize = fontSize
        self.display = display 
        self.sysFont = sysFont
        self.fontStyle = fontStyle
        self.language = language
        self.counter = counter
        self.stationName = stationName
        self.overFlowDisplay = overFlowDisplay
        
        
    def output(self):
        
        
        ip, port, fontSize, overFlowDisplay, fontStyle, language, counter, stationName, display, sysFont = self.ip, self.port,  self.fontSize, self.overFlowDisplay, self.fontStyle, self.language, self.counter, self.stationName , self.display, self.sysFont  
        

    
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
        
        
        
        # print("\nIP = ", ip, "\nPort = ", port, "\nText = ", stationName,  "Counter ", counter,"\nFont = ", fontPath[language][fontStyle], "\nFontSize = ", fontSize, "\n")
        
        
        if language == None and fontStyle == None:
            font = sysFont
        else:
            font = fontPath[language][fontStyle]
        
        
        
        img = Image.new('L', (200, 20))
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
        
        
        
        
        imgOverFlowDataString = Image.new('L', (480, 25))
        dx = ImageDraw.Draw(imgOverFlowDataString)
        fnt = ImageFont.truetype(font, fontSize) #max 12 fontsize
        
        text = stationName   
                
        dx.text((2,3), text , 1, font = fnt)
        
        #sns.heatmap(imgOverFlowDataString)
        #logger.error("OverFlow Data Map Right")
        
        imgOverFlowData = np.array(imgOverFlowDataString)
        
        setVariableRight = True
        
        for overFlow in imgOverFlowData[:, 162:]:
            for checkOverFlow in overFlow:
                if checkOverFlow == True:
                    print("\n\n Data is Overflowing \n\n")
                    setVariableRight = False
                    break 
            if setVariableRight == False and overFlowDisplay == True:
                j = Image.fromarray(imgOverFlowData[:, 162:])
                x = j.transpose(Image.FLIP_LEFT_RIGHT)
                x = j.transpose(Image.ROTATE_90)
                x = x.transpose(Image.ROTATE_90)
                x = x.transpose(Image.ROTATE_90)
                x = x.transpose(Image.ROTATE_90)
                y = np.array(x)
                sns.heatmap(y).set(title='OverFlow Data Map Right')
                plt.figure()
                #sg.Popup('Opps!', 'Data is OverFlowing')
                logger.error("OverFlow Data Map Right")
                break
        
        setVariableLower = True    
        for overFlow in imgOverFlowData[17:]:
            for checkOverFlow in overFlow:
                if checkOverFlow == True:
                    print("\n\n Data is Overflowing \n\n")
                    setVariableLower = False
                    break 
            if setVariableLower == False and overFlowDisplay == True:
                j = Image.fromarray(imgOverFlowData[17:])
                x = j.transpose(Image.FLIP_LEFT_RIGHT)
                x = j.transpose(Image.ROTATE_90)
                x = x.transpose(Image.ROTATE_90)
                x = x.transpose(Image.ROTATE_90)
                x = x.transpose(Image.ROTATE_90)
                y = np.array(x)
                sns.heatmap(y).set(title='OverFlow Data Map Lower')
                #plt.figure()
                #sg.Popup('Opps!', 'Data is OverFlowing')
                logger.error("OverFlow Data Map Lower")
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
        
        print("Ip  ", ip, "data")
        
        s.connect((ip, port))
        s.send(little_hex)
        s.close()
        print ("MESSAGE SENT SUCCESFULLY") #, data) 
            
    
    
class BitmapSignalingMultiSender:
    def __init__(self, ip, port, fontSize, counter, stationName, sysFont , display = False, fontStyle= None, language = None, overFlowDisplay = False, **kwargs):
        self.ip = ip
        self.port = port
        #self.text = text
        self.fontSize = fontSize
        self.display = display 
        self.sysFont = sysFont
        self.fontStyle = fontStyle
        self.language = language
        self.counter = counter
        self.stationName = stationName
        self.overFlowDisplay = overFlowDisplay
       
        
        
    def output(self):
        ip, port, fontSize, overFlowDisplay, fontStyle, language, counter, stationName, display, sysFont= self.ip, self.port,  self.fontSize, self.overFlowDisplay, self.fontStyle, self.language, self.counter, self.stationName , self.display, self.sysFont
     
        for ips in range(0, len(ip)):
            print(ips)
            x = SignalBitmapDisplay(ip = ip[ips], port = port, fontSize = fontSize, overFlowDisplay = overFlowDisplay, display = display, language = language, fontStyle = language , counter = counter[ips], stationName = stationName[ips], sysFont = sysFont)
            threading.Thread(target=x.output(), name=f'{ips}')
            print("Main thread name: {}".format(threading.current_thread().name))
            
    def getFontList():
        print( os.listdir("C://windows/fonts"))       
     
    
ip = "192.168.1.93";
port = 9999

fontSize = 12
overFlowDisplay = True
display = True
language = "English" 
fontStyle = "poppinsNormal"   

counter = ": 10"
stationName2 = "Jawaharlal Nehru Statdium"
stationName = "ABCDEFGHIJKLMNOPQRTSU"

stationName2 = "Amar Akbar Antony"



Iplist = ["192.168.1.93","192.168.1.94","192.168.1.95"]
datalist = ["Ahmad", "कभी लगता है इस जिन्दगी में खुशियां बेशुमार है,", stationName ,"Rochak"]
counter = [": 10", ": 50", ": 20"]
print(BitmapSignalingMultiSender.getFontList())

  
c = BitmapSignalingMultiSender(ip = Iplist, port = port, fontSize = fontSize, overFlowDisplay = False, display = False, language = None, fontStyle = None , counter = counter, stationName = datalist, sysFont = "NirmalaB")

c.output()

