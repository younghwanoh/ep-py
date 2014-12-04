#!/usr/bin/python

import sys
sys.dont_write_bytecode = True;

# library for ep.py
from parser import *
from tools import *
from plotter import *

# argument parser
import argparse

def parseCommandArgs():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-i", "--inFile", help='Specify the name of input data file')
    argparser.add_argument("-si", "--signature", help='Specify the signature')
    argparser.add_argument("-a", "--auxiliary", help='Auxiliary parameter')
    argparser.add_argument("-o","--outFile", help='Specify the name of output PDF file')
    argparser.add_argument("-s","--style", help='Specify the style of graphs')

    return argparser.parse_args()
