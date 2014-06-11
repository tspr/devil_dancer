# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 20:13:01 2014

@author: ts
"""

import argparse

DATA=1234
CARBON_SERVER='127.0.0.1'
ap=argparse.ArgumentParser(description='testprogramm f. Argparse')
ap.add_argument('-d', help='Daten...', default=DATA)

if __name__ == "__main__":
    print DATA