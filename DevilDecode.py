# -*- coding: utf-8 -*-
"""
DeVil-Decoder
Decodes Data from Avenisense DeVil Viscosity sensors
Created on Sun May 11 22:01:02 2014

@author: tspr
"""
import locale
locale.setlocale(locale.LC_ALL, 'de_DE')
import binascii

demopayload=[0xfd, 0x07, 0x00, 0x00, 0x4e, 0xaf, 0xb4, 0x93, 0xa0, 0x18, 0x09, 0x00, 0x68, 0xc6, 0x77, 0x7f,
             0x50, 0x99, 0x31, 0x00, 0x9d, 0xe8, 0x10, 0x1b, 0xe5, 0x82, 0x7f, 0x00, 0xd0, 0xf1, 0x07, 0x7f,
             0xb6, 0x8f, 0x4d, 0x00, 0x16, 0xa3, 0x08, 0x22, 0x18, 0x50, 0x29, 0x80, 0x10, 0x3a, 0x6c, 0x03,
             0x8c, 0xa2, 0x89, 0x04, 0x07, 0xd1, 0x63, 0x04]
             
def valueraw4(rawdata):
        assert(len(rawdata)==4)
        rv=int(rawdata[0])+256*(int(rawdata[1])+256*(int(rawdata[2])+256*int(rawdata[3])))
        return rv

def serialfromraw(rawdata):
    assert(len(rawdata)==2)
    rv=int(rawdata[0])+256*int(rawdata[1])
    return rv

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


    
#print demopayload
#print valueraw4(demopayload[5:9])
#print get_Temp(demopayload)
#print get_D(demopayload)
#print "V1: ",get_V1(demopayload)

filehdl = open('./DV data stream.txt','r')
for line in filehdl:
    print 'Line : ' , line
    hexdata=binascii.hexlify(line)
    print ' Serial : ',  serialfromraw(hexdata[0:2])
filehdl.close()

print "ende"
    