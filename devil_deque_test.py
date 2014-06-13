# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 22:08:52 2014

@author: ts
"""

import collections
import serial
import DevilDecode


SERIALPORT = '/dev/ttyUSB2'
ser=serial.Serial(
            port=SERIALPORT,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE)



dq =collections.deque(maxlen=10)
print dq

if not ser.isOpen():
    ser.open()

ser.flush()
while True:
    

        dq.append(int(ser.read(1)))
        print list(dq)

