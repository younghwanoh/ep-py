#!/usr/bin/python

import sys
import re
import csv
from sys import stdout

sys.dont_write_bytecode = True;

# library for ep.py
from parser import PatternParser
from tools import *
from plotter import *

# argument parser
import argparse
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--inFile", help='Specify the name of input data file')
argparser.add_argument("-si", "--signature", help='Specify the signature')
argparser.add_argument("-o","--outFile", help='Specify the name of output PDF file')
argparser.add_argument("-s","--style", help='Specify the style of graphs')
args = argparser.parse_args()

# color macro dictionary
mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292", "blue":"#4455D2",
        "white":"#FFFFFF", "dwhite":"#DFDFDF", "gray":"#888888", "dgray":"#4F4F4F", "black":"#000000"}

# output file name
output = "output.pdf"
if bool(args.outFile) == True:
    output = args.outFile

if bool(args.inFile) == True:
    text = tRead(args.inFile)

if bool(args.style) == True:
    style = args.style


# benchmarks = ["atax", "syrk", "gemm"]
benchmarks = ["syrk", "gemm"]
# benchmarks = ["syrk"]


key = ['GPU memcp', 'GPU comm0', 'GPU comm1', 'GPU comm2',
       'GPU schdl', 'GPU exe', 'GPU merge',
       'CPU memcp', 'CPU comm0', 'CPU comm1', 'CPU comm2',
       'CPU schdl', 'CPU exe', 'CPU merge']

S_GPUresult = []
NS_GPUresult = []
S_CPUresult = []
NS_CPUresult = []

# Reproduce data (Normalization, ...)
for i in range(len(benchmarks)):
    txt_share = tRead("dat/jaws-merge/%s.share.log" % benchmarks[i])
    txt_noshare = tRead("dat/jaws-merge/%s.noshare.log" % benchmarks[i])
    
    # Parse text
    PP1 = PatternParser(txt_share)
    PP1.PickKeyWith(": ")
    PP1.ParseWith(",")
    PP2 = PatternParser(txt_noshare)
    PP2.PickKeyWith(": ")
    PP2.ParseWith(",")

    S_GPUresult.append(PP1.datList[:6])
    S_CPUresult.append(PP1.datList[6:])
    NS_GPUresult.append(PP2.datList[:6])
    NS_CPUresult.append(PP2.datList[6:])

for i in range(len(benchmarks)):
    GPUOverhead = reduce(np.add, NS_GPUresult[i])
    CPUOverhead = reduce(np.add, NS_CPUresult[i])

    # Normalized to total sum of data(NS_CPUresult)
    S_GPUresult[i] = [ j[0]/GPUOverhead for j in S_GPUresult[i] ]
    NS_GPUresult[i] = [ j[0]/GPUOverhead for j in NS_GPUresult[i] ]
    S_CPUresult[i] = [ j[0]/CPUOverhead for j in S_CPUresult[i] ]
    NS_CPUresult[i] = [ j[0]/CPUOverhead for j in NS_CPUresult[i] ]

## Tag lists that will parse
tag_cpu = ["memcp", "comm0", "comm1", "comm2", "schdl", "merge"]
tag_gpu = ["memcp", "comm0", "comm1", "comm2", "schdl", "merge"]
leg = ["memcpy", "init", "task_begin", "task_end", "partition", "merge"]

## Set style
colors = [mc["black"], mc["dgray"], mc["gray"], mc["white"], mc["dwhite"], mc["white"]]
hatch = ["", "", "", "\\\\", "", ""]


## Draw box
SBP = SBarPlotter(title="Normalized overhead to each device",
                  xlabel="", ylabel="Fraction", figmargin=0.09)

# Set manual ticks
tlabel =   ["S", "GPU", "N", "SYRK", "S", "CPU", "N"] + \
           ["S", "GPU", "N", "GEMM", "S", "CPU", "N"]

L1 = TickLabel(None, tlabel)

tspace = [.5,1,1.5, 2.05, 2.6,3.1,3.6,
          5.6,6.1,6.6, 7.15, 7.7,8.2,8.7,
          10.7,11.2,11.7, 12.25, 12.8,13.3,13.8]
vspace = [0,-.04,0, -.09, 0,-.04,0,
          0,-.04,0, -.09, 0,-.04,0,
          0,-.04,0, -.09, 0,-.04,0]

SBP.setTicks(tspace=tspace, voffset=vspace, label=L1, fontsize=14)

# Set graph styles
SBP.setLegendStyle(ncol=3, size=13, frame=False)
SBP.setStackStyle(colors=colors, hatch=hatch, legend=leg) # alert! transposed data
SBP.setBottomMargin(0.13)

# Draw graphs
SBP.setLimitOn(y=[0, 1.2])
for i in range(len(benchmarks)):
    SBP.draw(S_GPUresult[i], NS_GPUresult[i], barwidth=1)
    SBP.setBaseOffset(1.1)
    SBP.draw(S_CPUresult[i], NS_CPUresult[i], barwidth=1)
    SBP.setBaseOffset(2)

SBP.saveToPdf(output)
