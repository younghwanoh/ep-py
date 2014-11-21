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
      "gray":"#AAAAAA", "dgray":"#3F3F3F", "black":"#111111"}

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
rawArr = PP.getDataArr()
transArr = ep.tools.tTranspose(rawArr)
accum = np.array([0 for i in range(len(transArr))])

for i, val in enumerate(transArr):
    temp = transArr[i]
    accum[i] += np.array(sum(temp[1:]))

for i in range(len(transArr)):
    for j, val in enumerate(transArr[i]):
        if j == 0:
            pass
        else:
            transArr[i][j] /= accum[i]

arr = ep.tools.tTranspose(transArr)
PP.datList = arr[1:]
leg = arr[0]

# Assign data
D1 = ep.Group(PP, "1~64", color=mc["black"], hatch="")
D2 = ep.Group(PP, "65~128", color=mc["dgray"], hatch="")
D3 = ep.Group(PP, "128~256", color=mc["white"], hatch="\\\\\\")
D4 = ep.Group(PP, "257~512", color=mc["white"], hatch="oo")
D5 = ep.Group(PP, "513~", color=mc["white"], hatch="")

D1.setLegend("1~64")
D2.setLegend("65~128")
D3.setLegend("128~256")
D4.setLegend("257~512")
D5.setLegend("513~")

# set tick labels with data
L1 = ep.TickLabel(None, leg)

# settings ===================================================================
SBP = ep.SBarPlotter(title="Stacked Bar", ylabel="Value", width=17, height=5)

# Set graph style
SBP.setLegendStyle(ncol=5, size=10, frame=False, loc="upper center")
SBP.setFigureStyle(figmargin=0.02, barwidth=0.04, interMargin=0.2, ylim=[0, 1.2], bottomMargin=0.3)

# draw =======================================================================
SBP.setTicks(label=L1, angle=45)
SBP.draw(D1, D2, D3, D4, D5)
SBP.saveToPdf(output)
