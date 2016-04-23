#!/usr/bin/python

# import sys
# sys.dont_write_bytecode = True;

# library for ep.py
import epic as ep
import numpy as np

args = ep.parseCommandArgs() 

# color macro dictionary
mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292",
      "blue":"#4455D2", "white":"#FFFFFF", "ddwhite":"#B3B3B3", "dwhite":"#DFDFDF",
      "gray":"#AAAAAA", "dgray":"#3F3F3F", "black":"#000000"}

# output file name
output = "line.pdf"
if bool(args.outFile) == True:
    output = args.outFile

if bool(args.inFile) == True:
    text = ep.tRead(args.inFile)

if bool(args.style) == True:
    style = args.style


# parse ======================================================================
text = ep.tRead("../dat/series-cbar/series.dat")

PP = ep.PatternParser(text)
PP.ParseWith("\t")

# make linear space for x axis
xspace = []
base = 0
for i in range(8):
    xspace += list(base + np.arange(4))
    base = xspace[-1] + 2
print xspace

xticklabel = ep.TickLabel(PP, 0)
LP = ep.LinePlotter(width=13, height=4, title="LinePlot with key", xlabel="", ylabel="")
LP.setTicks(xspace=xspace, label=xticklabel, angle=45)
LP.setLegendStyle(ncol=2, loc="upper center", frame=False)
LP.setFigureStyle(bottomMargin=0.3, xlim=[-1, 39], ylim=[0.5, 2], gridx=False, markersize=9)

for i in np.arange(8)*4:
    series1 = ep.Group(PP, xspace[i:i+4], PP.getDataArr(1)[i:i+4], color=mc["ddwhite"], marker="s")
    series2 = ep.Group(PP, xspace[i:i+4], PP.getDataArr(2)[i:i+4], color="black", marker="x")

    series1.setLegend("Series1") 
    series2.setLegend("Series2") 

    LP.draw(series1, series2)

LP.saveToPdf(output);
