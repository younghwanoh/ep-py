#!/usr/bin/python

# import sys
# sys.dont_write_bytecode = True;

# library for ep.py
import epic as ep
import numpy as np
import sys

args = ep.parseCommandArgs() 

# color macro dictionary
mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292",
      "blue":"#4455D2", "white":"#FFFFFF", "ddwhite":"#B3B3B3", "dwhite":"#DFDFDF",
      "gray":"#AAAAAA", "dgray":"#3F3F3F", "black":"#111111"}

# output file name
output = "sc-bar.pdf"
if bool(args.outFile) == True:
    output = args.outFile

if bool(args.inFile) == True:
    text = ep.tRead(args.inFile)
else:
    text = ep.tRead("../dat/sc-bar/c1.dat")

if bool(args.style) == True:
    style = args.style


# parse ======================================================================
PP = ep.PatternParser(text)
PP.PickKeyWith("row")
PP.ParseWith("\t")

del PP.keyList[0]

# Assign data: Cluster 1
D1 = ep.Group(None, PP.getDataArr(0, opt="col")[1:], color=mc["black"], hatch="")
D2 = ep.Group(None, PP.getDataArr(1, opt="col")[1:], color=mc["dwhite"], hatch="")

# Assign data: Cluster 2
D3 = ep.Group(None, PP.getDataArr(0, opt="col")[1:], color=mc["black"], hatch="")
D4 = ep.Group(None, PP.getDataArr(1, opt="col")[1:], color=mc["dwhite"], hatch="")

D1.setLegend("on-package bandwidth")
D2.setLegend("off-package bandwidth")

# set tick labels with data
label = PP.getKeyArr()
L1 = ep.TickLabel(None, label + label)

# settings ===================================================================
SBP = ep.SBarPlotter(title="Stacked Bar", ylabel="Value")

# Set graph style
SBP.setLegendStyle(ncol=5, size=10, frame=False, loc="upper center")
SBP.setFigureStyle(figmargin=0.05, barwidth=1, interMargin=0.5, bottomMargin=0.3)

# draw =======================================================================
SBP.setTicks(label=L1, angle=45)
SBP.draw(D1, D2)
SBP.setBaseOffset(1.7)
SBP.draw(D3, D4)
SBP.saveToPdf(output)
