# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 20:36:46 2022

@author: gurut
"""


import numpy as np
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont
import socket
import matplotlib.pyplot as plt 
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate



class BitMapMaker:
    def __init__(self, ip, port, text, font, fontSize, language):
        self.ip = ip
        self.port = port
        self.text = text
        self.font = font
        self.fontSize = fontSize
        self.language = language
    
    def output(self):
        ip, port, text, font, fontSize, language= self.ip, self.port, self.text, self.font, self.fontSize, self.language
        
        
        print(ip, port, text, font, fontSize)
        
        img = Image.new('L', (240, 20))
        d = ImageDraw.Draw(img)

        fnt = ImageFont.truetype(font, fontSize) #max 12 fontsize
        
        languages = {"hindi" : sanscript.DEVANAGARI,
             "gujarati" : sanscript.GUJARATI,
             "kannad": sanscript.KANNADA,
             "telugu": sanscript.TELUGU
             }
        
        if language == "hindi":
            text = transliterate(text, sanscript.HK, languages[language])
            print("Hindi ", text)
        
        if language == "kannad":
            text = transliterate(text, sanscript.ITRANS, languages[language])
            print("kannad ", text)
        
        if language == "test":
             text = text
             print("test ", text)
        
        else:
            text = text
            
        
            
            
        
        d.text((2,1), text , 1, font = fnt)
        
        
        img2arrOriginal = np.array(img)
        
        
        imgFlip = img.transpose(Image.ROTATE_90)
        imgFlip = imgFlip.rotate(180)
        imgFlip = imgFlip.transpose(Image.FLIP_LEFT_RIGHT)
        im2arrFliped = np.array(imgFlip)
        
        
        im2arrFliped = np.delete(im2arrFliped, np.s_[0:5], axis=1)
        j = Image.fromarray(im2arrFliped)
        dst = Image.new('L', (16, 240))
        dst.paste(j, (0, 0))
        im2arrMerged = np.array(dst)

        fig, axes = plt.subplots(ncols=3, figsize=(10, 10))
 
        fig.suptitle(font + " " + text)
        
        imgFlip90 = img.transpose(Image.ROTATE_90)
        sns.heatmap(imgFlip90, ax=axes[0])
        
        sns.heatmap(im2arrFliped, ax=axes[1])
        
        sns.heatmap(im2arrMerged, ax=axes[2])


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
        
        import re
        mergedAllBinary8Bit = re.findall('........', mergeAllBinary)
        
        
        Storebin2Hex = []
        for data in mergedAllBinary8Bit:
            #print("Data = ", data, "Length of data ",len(data))
            bin2hex = hex(int(data, 2))
            if bin2hex=='0x0':
               # print("0x0 loop", bin2hex)
                bin2hex = bin2hex[2:]+'0'
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
        
        
        #Checksum
        
        splitDataOfFullData = AllDataOfProtocol.split("-")
        
        for r in range(0,len(splitDataOfFullData)):
            #g = g+bytes(splitData[r], 'Utf-8') 
            splitDataOfFullData[r] = bytes(splitDataOfFullData[r], 'Utf-8') 
        
            
        
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
            
            
        try:    
            little_hex = bytearray.fromhex(bufferString)
        except:
            little_hex = bytearray.fromhex(bufferString[:-1])
        #little_hex.reverse()
        print("Byte array format:", little_hex)
        
        
        
        #BUFFER_SIZE = 1024

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.send(little_hex)
        s.close()
        #data = s.recv(BUFFER_SIZE)
        print ("MESSAGE HAS BEEN SENT") #, data)        




        
eng_font, hindi_fnt, kannad_fnt = "Fonts/hindi/Poppins-Medium.ttf"  , "Fonts/hindi/Lohit-Devanagari.ttf" , "Fonts/kannad/Lohit-Kannada_TOP.ttf"   

 
# x = BitMapMaker("192.168.1.93", 9999, "Hello",kannad_fnt, 8, "kannad" ) #ip, port, text, font, fontSize, language
# x.output()        
        
        
# x = BitMapMaker("ip", 1234, "Hello",eng_font, 12,

# "english" ) #ip, port, text, font, fontSize, language
# x.output()           
        
        
        
# x = BitMapMaker("ip", 1234, "Hello",hindi_fnt, 12, "hindi" ) #ip, port, text, font, fontSize, language
# x.output()           
    
# import os

# ttf  = os.listdir("Fonts/kannad")


# for i in ttf:
        
#     hindi_fnt = "Fonts/kannad/" + i
           
#     y = "दिल्ली मेट्रो में आपका सुआगत हा "
#     y = "ದೆಹಲಿ ಮೆಟ್ರೋಗೆ ಸುಸ್ವಾಗತ"
#     x = BitMapMaker("ip", 1234, y, hindi_fnt, 12, "test" ) #ip, port, text, font, fontSize, language
#     x.output()  
    
y = "दिल्ली मेट्रो में आपका सुआगत हा "
y = "R O C H A K"
y = "A B C D E F G H I J K L M N O P"
x = BitMapMaker("192.168.1.94", 9999, y ,"Fonts/hindi/Poppins-Medium.ttf", 12, "test" ) #ip, port, text, font, fontSize, language
x.output()   