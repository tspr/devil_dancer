# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 20:13:01 2014

@author: ts
"""

import argparse

DATA=1234
CARBON_SERVER='127.0.0.1'
ap=argparse.ArgumentParser(description='Logging-Deamon for Sengenuity Viscosity measurement device. Retrieves Data, writes to file and graphite/carbon server.')

ap.add_argument('-i',help='Interval: retrieve Data every I seconds', dest='INTERVAL',type=int,default=1)
args=ap.parse_args()

INTERVAL = args.INTERVAL
if __name__ == "__main__":
    print INTERVAL