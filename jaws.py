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
mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292",
      "blue":"#4455D2", "white":"#FFFFFF", "ddwhite":"#B3B3B3", "dwhite":"#DFDFDF",
      "gray":"#888888", "dgray":"#3F3F3F", "black":"#000000"}

# output file name
output = "output.pdf"
if bool(args.outFile) == True:
    output = args.outFile

if bool(args.inFile) == True:
    text = tRead(args.inFile)

if bool(args.style) == True:
    style = args.style


benchmarks = ["syrk", "gemm"]

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

    S_CPUresult.append(tTranspose(PP1.datList[:4])[0])
    S_GPUresult.append(tTranspose(PP1.datList[4:])[0])
    NS_CPUresult.append(tTranspose(PP2.datList[:4])[0])
    NS_GPUresult.append(tTranspose(PP2.datList[4:])[0])


for i in range(len(benchmarks)):
    # del S_GPUresult[i][2]
    # del NS_GPUresult[i][2]
    # del S_CPUresult[i][2]
    # del NS_CPUresult[i][2]

    GPUOverhead = sum(NS_GPUresult[i])
    CPUOverhead = sum(NS_CPUresult[i])

    # Normalized to total sum of data(NS_CPUresult)
    S_GPUresult[i] = [ j/GPUOverhead for j in S_GPUresult[i] ]
    NS_GPUresult[i] = [ j/GPUOverhead for j in NS_GPUresult[i] ]
    S_CPUresult[i] = [ j/CPUOverhead for j in S_CPUresult[i] ]
    NS_CPUresult[i] = [ j/CPUOverhead for j in NS_CPUresult[i] ]

    # Change order of stack
    S_GPUresult[i][0], S_GPUresult[i][2] = S_GPUresult[i][2], S_GPUresult[i][0]
    NS_GPUresult[i][0], NS_GPUresult[i][2] = NS_GPUresult[i][2], NS_GPUresult[i][0]
    S_CPUresult[i][0], S_CPUresult[i][2] = S_CPUresult[i][2], S_CPUresult[i][0]
    NS_CPUresult[i][0], NS_CPUresult[i][2] = NS_CPUresult[i][2], NS_CPUresult[i][0]

## Legend list
leg = ["dispatch", "memcpy", "exec", "merge"]
# del leg[0]

## Assign stack style
colors = [mc["dgray"], mc["white"], mc["gray"], mc["dwhite"], mc["dwhite"], mc["white"]]
# del colors[0]
hatch = ["", "\\\\", "", "", "", ""]
# del hatch[0]

## Stacked Bar Plot =================================================================
SBP = SBarPlotter(xlabel="", ylabel="Overhead normalized\n to useful work",
                  ylpos=[-.1, 0.5], width=8, height=4.2)

# Set manual ticks ==================================================================
SBP.annotate(["syrk", "gemm"], [[1.55, -.24], [6.55, -.24]], fontsize=18)
tlabel =   ["N", "GPU", "S", "N", "CPU", "S"] + \
           ["N", "GPU", "S", "N", "CPU", "S"]
L1 = TickLabel(None, tlabel)

xspace = [.5,1,1.5, 2.6,3.1,3.6,
          5.6,6.1,6.6, 7.7,8.2,8.7,
          10.7,11.2,11.7, 12.8,13.3,13.8]
vspace = [0,-.08,0, 0,-.08,0,
          0,-.08,0, 0,-.08,0,
          0,-.08,0, 0,-.08,0]
SBP.setTicks(xspace=xspace, voffset=vspace, label=L1, fontsize=14)

# Set graph styles ==================================================================
SBP.setLegendStyle(ncol=6, size=15, pos=[0.93, 1.15], frame=False, tight=True)
SBP.setFigureStyle(bottomMargin=0.23, ylim=[0, 1], figmargin=0.09, fontsize=15)

# if "setStackStyle" method is used, transposed data will be used
# otherwise, group will map the styles to each stack
SBP.setStackStyle(colors=colors, hatch=hatch, legend=leg)

# Draw graphs =======================================================================
for i in range(len(benchmarks)):
    SBP.draw(NS_GPUresult[i], S_GPUresult[i], barwidth=1)
    SBP.setBaseOffset(1.1)
    SBP.draw(NS_CPUresult[i], S_CPUresult[i], barwidth=1)
    SBP.setBaseOffset(2)

SBP.saveToPdf(output)
