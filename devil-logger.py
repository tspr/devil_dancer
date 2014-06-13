# -*- coding: utf-8 -*-
"""
Created on Fri May 30 09:23:58 2014
Devil-Logger.py
Version 1.0

usage:  devil-logger -rrd FILENAME -c CARBONSERVER -v -p SERIALPORT
@author: T.Sprinzing
sprinzing@hdm-stuttgart.de
"""

from time import time, sleep
#from sys import argv
#import DevilDecode


INTERVAL = 1

SERIALPORT = '/dev/ttyUSB2'
CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003
WPATH=getcwd()

logging.basicConfig(filename=WPATH + '/devil_logger.log',
                            level=logging.DEBUG,
                            format='%(asctime)s:%(levelname)s:%(message)s',
                            datefmt='%d-%m-%Y %I:%M:%S %p')


class devil_log():
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
        csvfilepath= WPATH + '/' + datetime.datetime.today().strftime('%Y-%d-%m') + '_DeViL.csv'
        try:
            self.csvfile=open(csvfilepath,'a')
            self.csvwriter=csv.writer(self.csvfile,dialect='excel-tab')
            self.csvstatus=True
        except:
            logging.critical('could not open csv file for writing')
            self.csvstatus=False
            pass

        logging.debug('setting up carbon storage connection)
        self.sock = socket.socket()
        try:
            self.sock.connect( (CARBON_SERVER, CARBON_PORT) )
            self.carbonstatus=True
        except socket.error:
            logging.warning("Couldn't connect to %(server)s on port %(port)d, is carbon-cache.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT })
            self.carbonstatus=False
            pass
        
        
        def mainloop():
    


if __name__ == "__main__":
    vm=devil_log()    
    vm.setup()
    # run main loop
    try:
        vm.mainloop()
    except (KeyboardInterrupt, SystemExit):
        # exit gracefully
        vm.csvfile.flush()
        vm.csvfile.close()
        vm.ser.close()
        sys.stderr.write("\nDevil-Logger Exiting\n")
        sys.exit(0)