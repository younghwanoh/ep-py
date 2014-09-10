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
      "gray":"#888888", "dgray":"#909090", "black":"#000000"}

# output file name
output = "output.pdf"
if bool(args.outFile) == True:
    output = args.outFile

if bool(args.inFile) == True:
    text = tRead(args.inFile)

if bool(args.style) == True:
    style = args.style


# Start ===============================================================================

# Comparison clustered bar
# Polybench
PP = PatternParser(tRead("dat/jaws-comp/poly.dat"))
PP.PickKeyWith("row")
PP.ParseWith("\t")
PP.datNormTo("cpu-only", "gpu-only", predicate="min")

PD = []
PD.append(Group(PP, "SO", color=mc["white"], hatch=""))
PD.append(Group(PP, "Boyer", color=mc["ddwhite"], hatch=""))
PD.append(Group(PP, "jAWS", color=mc["black"], hatch=""))

PD[0].setLegend("FluidiCL")
PD[1].setLegend("Boyer et al.")
PD[2].setLegend("jAWS")

# WebCL
PP = PatternParser(tRead("dat/jaws-comp/webcl.dat"))
PP.PickKeyWith("row")
PP.ParseWith("\t")
PP.datNormTo("cpu-only", "gpu-only", predicate="min")

WD = []
WD.append(Group(PP, "SO", color=mc["white"], hatch=""))
WD.append(Group(PP, "Boyer", color=mc["ddwhite"], hatch=""))
WD.append(Group(PP, "jAWS", color=mc["black"], hatch=""))

# Geomean
PP = PatternParser(tRead("dat/jaws-comp/geomean-best.dat"))
PP.PickKeyWith("row")
PP.ParseWith("\t")

GD = []
GD.append(Group(PP, "SO", color=mc["white"], hatch=""))
GD.append(Group(PP, "Boyer", color=mc["ddwhite"], hatch=""))
GD.append(Group(PP, "jAWS", color=mc["black"], hatch=""))

# global label
g_label = ["ATAX", "BICG", "SYRK", "SYR2K", "GEMM", "2MM", "CORR",
           "Mandelbrot", "Nbody", "Sobel-CorG", "Random", "geomean"]

L1 = TickLabel(None, g_label)
CB = CBarPlotter(ylabel="Speedup over Best Device", width=15, height=3.4,
                 figmargin=0.02, interCmargin=.7, allFontSize=13)
CB.setTicks(yspace=[0, 0.5, 1, 1.5], label=L1)
CB.setLegendStyle(ncol=3, size=14, pos=[0.47, 1.18], frame=False)
CB.setLimitOn(y=[0, 1.5])
CB.annotate(["Polybench", "WebKit-WebCL"], [[26, -.30], [85, -.30]], fontsize=15)
CB.setBottomMargin(0.18)

CB.draw(*PD, barwidth=2)
CB.setBaseOffset(14)
CB.draw(*WD, barwidth=2)
CB.setBaseOffset(14)
CB.draw(*GD, barwidth=2)

g_base = CB.getGlobalBase()
# Line Graph
# Polybench
PP = PatternParser(tRead("dat/jaws-lbf/poly.dat"))
PP.PickKeyWith("row")
PP.ParseWith("\t")

color = [mc["black"], mc["dwhite"], mc["dgray"]]
# color = [mc["black"], mc["dgray"], mc["dwhite"]]
face = color
marker = ["+","x","v"]

PLB = []
PLB.append(Group(PP, g_base[:7], "Fluidic", color=color[0], face=face[0], marker=marker[0]))
PLB.append(Group(PP, g_base[:7]+2, "Boyer", color=color[1], face=face[1], marker=marker[1]))
PLB.append(Group(PP, g_base[:7]+4, "jAWS", color=color[2], face=face[2], marker=marker[2]))

PLB[0].setLegend("FluidiCL")
PLB[1].setLegend("Boyer et al.")
PLB[2].setLegend("jAWS")

# WebCL
PP = PatternParser(tRead("dat/jaws-lbf/webcl.dat"))
PP.PickKeyWith("row")
PP.ParseWith("\t")

WLB = []
WLB.append(Group(PP, g_base[7:11], "Fluidic", color=color[0], face=face[0], marker=marker[0]))
WLB.append(Group(PP, g_base[7:11]+2, "Boyer", color=color[1], face=face[1], marker=marker[1]))
WLB.append(Group(PP, g_base[7:11]+4, "jAWS", color=color[2], face=face[2], marker=marker[2]))

# WebCL
PP = PatternParser(tRead("dat/jaws-lbf/geomean.dat"))
PP.PickKeyWith("row")
PP.ParseWith("\t")

GLB = []
GLB.append(Group(PP, g_base[11:], "Fluidic", color=color[0], face=face[0], marker=marker[0]))
GLB.append(Group(PP, g_base[11:]+2, "Boyer", color=color[1], face=face[1], marker=marker[1]))
GLB.append(Group(PP, g_base[11:]+4, "jAWS", color=color[2], face=face[2], marker=marker[2]))

twinx = CB.getAxis()

LP = LinePlotter(axis=twinx, ylabel="Load Balance Factor")
LP.setTicks(yspace=[0, 0.5, 1.0, 1.5])
LP.draw(*PLB)
LP.setBaseOffset(0)
LP.draw(*WLB)
LP.setBaseOffset(0)
LP.draw(*GLB)
LP.setLegendStyle(ncol=3, size=14, pos=[0.97, 1.18], frame=False)

LP.FinalCall()

CB.saveToPdf(output)
