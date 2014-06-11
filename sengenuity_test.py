# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/ts/.spyder2/.temp.py
"""

import serial
import time
import logging
import datetime
from os import getcwd

INTERVAL = 1
SERIALPORT = '/dev/ttyUSB0'

WPATH=getcwd()

logging.basicConfig(filename=WPATH + '/sengenuity_deamon.log',
                            level=logging.DEBUG,
                            format='%(asctime)s:%(levelname)s:%(message)s',
                            datefmt='%d-%m-%Y %I:%M:%S %p')
                            
                        
class viscomess():
    def setup(self):
        logging.debug('setting up serial connection')
        self.ser=serial.Serial(
            port=SERIALPORT,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE)
    
        if self.ser.isOpen():
            logging.info('serial port already open. Hope this works')
        else:
            logging.info('opening serial port')            
            try:
                self.ser.open()
            except:
                logging.critical('cannot open serial ' + SERIALPORT)
                raise
        logging.debug('setting up csv file for writing')
        csvfilepath= WPATH + '/' + datetime.datetime.today().strftime('%Y-%d-%m') + '.csv'
        try:
            self.csvfile=open(csvfilepath,'a')
            self.csvwriter=csv.writer(self.csvfile,dialect='excel-tab')
            self.csvstatus=True
        except:
            logging.critical('could not open csv file for writing')
            self.csvstatus=False

    def mainloop(self):
        #initialize timing control loop values
        readtime = time.time() - INTERVAL
        timeintegral = 0
        corr = 0
        self.rr=0
        #start main loop
        while 1:    
            #(re-)set timing variables            
            lasttime=readtime
            readtime=time.time()    
            # repetition timing control loop
            timediff=readtime-lasttime-INTERVAL
            timeintegral = timeintegral + timediff
            corr = (0.3 * timediff) + (0.75 * timeintegral) + 0.001
            logging.debug( str(readtime) + ' ' + str(lasttime)+ ' ' + str(timediff+INTERVAL) + ' ' + str(timeintegral) + ' ' + str(corr))
            # call worker process()
            self.worker()
            # calculate time to next call, wait
            remainingtime = readtime + INTERVAL - time.time() - corr
            if remainingtime > 0:
                time.sleep(remainingtime)
        
    
    def worker(self):
        if self.ser.isOpen():
            self.ser.flush()
            self.ser.write(':10,A\r\n')
            raw= self.ser.readline(self.ser.inWaiting()).rstrip('\x00\r\n').lstrip('\x00')
            logging.info('read: ' + str(raw.split(',')))
            if self.csvstatus:
                logging.info('writing to csv')
                row=[]
                row.append(asctime())
                row.append(time.time())
                for item in raw.split(','):
                    row.append(item)
                self.csvwriter.writerow(row)
            if self.rr == 10:
                self.csvfile.flush()
                self.rr = 0
            self.rr += 1
            
            
    

if __name__ == "__main__":
    vm=viscomess()    
    vm.setup()
    # run main loop
    vm.mainloop()