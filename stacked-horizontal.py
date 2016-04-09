#!/usr/bin/python

import csv
from sys import stdout

import numpy as np
import epic as ep

import readline
import rlcompleter
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

# args = ep.parseCommandArgs() 

# color macro dictionary
mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292",
      "blue":"#4455D2", "white":"#FFFFFF", "ddwhite":"#B3B3B3", "dwhite":"#DFDFDF",
      "gray":"#888888", "dgray":"#4F4F4F", "black":"#000000"}

# output file name
output = "bytecode-ratio.pdf"
text = ep.tRead("dat/bytecode-ratio.dat")

bench = [ "binarytree","fankuchredux","knucleotide","mandelbrot","nbody","spectralnorm","nsieve","random","fibo","ackermann","pidigits" ]
bench.reverse()
colors = [ mc["black"], mc["dgray"], mc["gray"], mc["white"]  , mc["white"], mc["ddwhite"], mc["white"], mc["white"], mc["white"], mc["white"], mc["white"]]
hatchs = [""          , ""         , ""        , "\\\\\\\\\\\\", ".."        , ""           , "//////", "xxx"      , "++++"     , "...."          , ""]

# Use custom parser mode
PP = ep.PatternParser(text);
PP.PickKeyWith("col")
PP.ParseWith("\t")

D1 = []
keys = PP.getKeyArr()
for i in range(len(keys)):
    D1.append(ep.Group(PP, keys[i], color=colors[i], hatch=hatchs[i]))
    D1[i].setLegend(keys[i])

L1 = ep.TickLabel(None, bench)

## Draw box
SBP = ep.SBarPlotter(width=10.2, height=5, xlabel="Percentage (%)", horizontal=True)

# Set graph style
SBP.setLegendStyle(ncol=6, size=10.5, frame=False, pos=[1,1.16])
SBP.setFigureStyle(figmargin=0, topMargin=0.8, interMargin=1.5, xlim=[0,100])

# Draw
SBP.setTicks(label=L1, voffset=[-0.01]*11, align="right")
SBP.draw(*D1, barwidth=1)
SBP.saveToPdf(output)
