#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sengenuity-logger.py
Version 1.0
Created on Wed Jun 11 20:07:28 2014

@author: T.Sprinzing
sprinzing@hdm-stuttgart.de
"""

import serial
import socket
import sys
import time
from time import sleep
import logging
import datetime
from os import getcwd
import csv


INTERVAL = 2
SERIALPORT = '/dev/sengenuity'
CARBON_SERVER = '141.62.68.180'
CARBON_PORT = 2003
WPATH=getcwd()
logfilename=WPATH + '/sengenuity_logger.log'
logging.basicConfig(filename=logfilename,
                            level=logging.INFO,
                            format='%(asctime)s: %(levelname)s: %(message)s',
                            datefmt='%d-%m-%Y %I:%M:%S %p')
                            
                        
class viscomess():
    def setup(self):
        logging.debug('setting up serial connection: ' + SERIALPORT)
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
        
        csvfilepath= WPATH + '/' + datetime.datetime.today().strftime('%Y-%m-%d') + '_Sengenuity.csv'
        logging.info('setting up csv file for writing: '+ csvfilepath)        
        try:
            self.csvfile=open(csvfilepath,'wa')
            self.csvwriter=csv.writer(self.csvfile,dialect='excel-tab')
            self.csvstatus=True
        except:
            logging.critical('could not open csv file for writing')
            self.csvstatus=False
            pass

        logging.info('setting up carbon storage connection to: '+ str(CARBON_SERVER) +':'+str(CARBON_PORT))
        self.sock = socket.socket()
        try:
            self.sock.connect( (CARBON_SERVER, CARBON_PORT) )
            self.carbonstatus=True
        except socket.error:
            logging.warning("Couldn't connect to %(server)s on port %(port)d, is carbon-cache.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT })
            self.carbonstatus=False
            pass
        
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
            sleep(0.5)
            raw= self.ser.readline(self.ser.inWaiting()).rstrip('\x00\r\n').lstrip('\x00')
            logging.info('read: ' + str(raw.split(',')))
            tnow=int(time.time())
            if self.csvstatus:
                logging.debug('writing to csv')
                row=[]
                row.append(time.asctime())
                row.append(tnow)
                for item in raw.split(','):
                    row.append(item)
                self.csvwriter.writerow(row)
            if self.rr == 10:
                self.csvfile.flush()
                self.rr = 0
            self.rr += 1
            carbonwrite=False            
            try:
                    temperature=raw.split(',')[1]
                    av=raw.split(',')[2]
                    err=raw.split(',')[3]
                    carbonwrite=True    
                    if (carbonwrite &
                        (raw.split(',')[0] == '10') &
                        (raw.split(',')[3] == '0') &
                        self.carbonstatus ):
                            logging.debug('sending data to carbonserver ' + CARBON_SERVER)
                            lines=[]
                            lines.append("HdM.Tiefdruck.Visko.Sengenuity.Temp %s %d" % (temperature, tnow))
                            lines.append("HdM.Tiefdruck.Visko.Sengenuity.AV %s %d" % (av, tnow))
                            message = '\n'.join(lines) + '\n' #all lines must end in a newline
                            self.sock.sendall(message)
            except:
                    logging.warning('received garbage:' + raw)
                    pass
                         
           
            

if __name__ == "__main__":
    logging.info('Starting up...')    
    vm=viscomess()    
    vm.setup()
    # run main loop
    try:
        vm.mainloop()
    except (KeyboardInterrupt, SystemExit):
        # exit gracefully
        vm.csvfile.flush()
        vm.csvfile.close()
        vm.ser.close()
        logging.info("Terminating on keyboardInt or SysExit")
        sys.stderr.write("Sengenuity-Logger terminated.")
        sys.exit(0)
