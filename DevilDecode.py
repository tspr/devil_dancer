# -*- coding: utf-8 -*-
"""
DeVil-Decoder
Decodes Data from Avenisense DeVil Viscosity sensors
Created on Sun May 11 22:01:02 2014

@author: tspr
"""
#import locale
#locale.setlocale(locale.LC_ALL, 'de_DE')
import binascii

demopayload=[0xfd, 0x07, 0x00, 0x00, 0x4e, 0xaf, 0xb4, 0x93, 0xa0, 0x18, 0x09, 0x00, 0x68, 0xc6, 0x77, 0x7f,
             0x50, 0x99, 0x31, 0x00, 0x9d, 0xe8, 0x10, 0x1b, 0xe5, 0x82, 0x7f, 0x00, 0xd0, 0xf1, 0x07, 0x7f,
             0xb6, 0x8f, 0x4d, 0x00, 0x16, 0xa3, 0x08, 0x22, 0x18, 0x50, 0x29, 0x80, 0x10, 0x3a, 0x6c, 0x03,
             0x8c, 0xa2, 0x89, 0x04, 0x07, 0xd1, 0x63, 0x04]
             
            
          
             
def valueraw4(rawdata):
        assert(len(rawdata)==4)
        rv=int(rawdata[0])+256*(int(rawdata[1])+256*(int(rawdata[2])+256*int(rawdata[3])))
        return rv

def get_Serial(rawdata):
    temp=int(rawdata[0])+256*int(rawdata[1])
    return temp

def get_Temp(data):
    temp=float(valueraw4(data[4:8]))/pow(2,23)
    return temp

def get_E1(data):
    temp=float(valueraw4(data[8:12]))/1
    return temp

def get_C1(data):
    temp=float(valueraw4(data[12:16]))/pow(2,31)
    return temp
    
def get_Q1(data):
    temp=float(valueraw4(data[16:20]))/pow(2,16)
    return temp

def get_F1(data):
    temp=float(valueraw4(data[20:24]))/pow(2,16)
    return temp

def get_E2(data):
    temp=float(valueraw4(data[24:28]))/1
    return temp

def get_C2(data):
    temp=float(valueraw4(data[28:32]))/pow(2,31)
    return temp
    
def get_Q2(data):
    temp=float(valueraw4(data[32:36]))/pow(2,16)
    return temp

def get_F2(data):
    temp=float(valueraw4(data[36:40]))/pow(2,16)
    return temp

def get_K(data):
    temp=float(valueraw4(data[40:44]))/pow(2,31)
    return temp

def get_D(data):
    temp=float(valueraw4(data[44:48]))/pow(2,16)
    return temp    

def get_V1(data):
    temp=float(valueraw4(data[48:52]))/pow(2,32)
    return temp    

def get_V2(data):
    temp=float(valueraw4(data[52:56]))/pow(2,32)
    return temp    


 
if __name__ == "__main__":   
    #print demopayload
    #print valueraw4(demopayload[5:9])
    #print get_Temp(demopayload)
    #print get_D(demopayload)
    #print "V1: ",get_V1(demopayload)    
    filehdl = open('./devillog.log','r')
    for line in filehdl:
        if len(line)>= 56:    
            print 'Line : ' , line
            hd=bytearray.fromhex(line.split('\r')[0])
            print ' Serial: ',  get_Serial(hd)
            print ' Temp: ', get_Temp(hd)
            print ' E1: ', get_E1(hd)
            print ' C1: ', get_C1(hd)
            print ' Q1: ', get_Q1(hd)
            print ' F1: ', get_F1(hd)
            print ' E2: ', get_E2(hd)
            print ' C2: ', get_C2(hd)
            print ' Q2: ', get_Q2(hd)
            print ' F2: ', get_F2(hd)
            print ' K: ', get_K(hd)
            print ' D: ', get_D(hd)
            print ' V1: ', get_V1(hd)
            print ' V2: ', get_V2(hd)
            print ''
            print '-------------'
            print''
    filehdl.close()
    
    print "ende"
    