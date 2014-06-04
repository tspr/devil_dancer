# -*- coding: utf-8 -*-
"""
Created on Fri May 30 09:23:58 2014
Devil-Logger


usage:  devil-logger -rrd FILENAME -c CARBONSERVER -v -p SERIALPORT
@author: tspr
"""

from time import time, sleep
#from sys import argv
#import DevilDecode


INTERVAL = 1

def mainloop():
    print INTERVAL    
    readtime = time() - INTERVAL
    timeintegral = 0
    corr = 0
    while 1:    
        lasttime=readtime
        readtime=time()    
        timediff=readtime-lasttime-INTERVAL
        timeintegral = timeintegral + timediff
        print readtime, ' ' , lasttime, ' ', timediff, ' ',timeintegral, corr
        corr = (0.3 * timediff) + (0.75 * timeintegral)
        #if corr > (2 * INTERVAL):
        #    corr = 2 * INTERVAL
        #if corr < (-2* INTERVAL):
        #    corr = -2 * INTERVAL
        remainingtime = readtime + INTERVAL - time() - corr
        if remainingtime > 0:
            sleep(remainingtime)


if __name__ == "__main__":
    #setup()
    # run main loop
    while 1:
        
        mainloop()
