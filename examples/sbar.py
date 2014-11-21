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
output = "sbar.pdf"
if bool(args.outFile) == True:
    output = args.outFile

if bool(args.inFile) == True:
    text = ep.tRead(args.inFile)

if bool(args.style) == True:
    style = args.style


# parse ======================================================================
PP = ep.PatternParser(ep.tRead("../dat/sbar/optimize.data"))
PP.PickKeyWith("row")
PP.ParseWith("\t")

# Normalize data to total sum
key = ["s1", "s2", "s3"]
accum = np.array([0 for i in range(len(key))])

rawArr = PP.getDataArr()
transArr = ep.tools.tTranspose(rawArr)

for i, val in enumerate(key):
    temp = transArr[i]
    accum[i] += np.array(sum(temp[1:]))

for i, val in enumerate(key):
    for j, val in enumerate(transArr[i]):
        if j == 0:
            pass
        else:
            transArr[i][j] /= accum[i]

PP.datList = ep.tools.tTranspose(transArr)

D1 = ep.Group(PP, "s1", color=mc["dgray"], hatch="")
D2 = ep.Group(PP, "s2", color=mc["white"], hatch="\\\\\\")
D3 = ep.Group(PP, "s3", color=mc["dwhite"], hatch="")

D1.setLegend("A")
D2.setLegend("B")
D3.setLegend("C")

# set tick labels manually
L1 = ep.TickLabel(None, ["A", "B", "C"])

# set tick labels with data
# L1 = ep.TickLabel(PP, "name")

# settings ===================================================================
SBP = ep.SBarPlotter(title="Stacked Bar", xlabel="Strategy", ylabel="Value")

# Set graph style
SBP.setLegendStyle(ncol=3, size=10, frame=False, loc="upper center")
SBP.setFigureStyle(figmargin=0.1, barwidth=1, interMargin=0.1, ylim=[0, 1.2])

# draw =======================================================================
SBP.setTicks(label=L1)
SBP.draw(D1, D2, D3)
SBP.saveToPdf(output)
