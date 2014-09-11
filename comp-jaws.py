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
      "blue":"#4455D2",
      "white":"#FFFFFF", "dwhite":"#DFDFDF", "ddwhite":"#B3B3B3",
      "gray":"#888888", "wgray":"#CECECE", "dgray":"#909090", "ddgray":"#5F5F5F",
      "black":"#000000"}

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

# label lists
poly_list = ["ATAX", "BICG", "SYRK", "SYR2K", "GEMM", "2MM", "CORR"]
poly_list_l = [ elem.lower() for elem in poly_list ]
webcl_list = ["Mandelbrot", "Nbody", "Sobel-CorG", "Random"]
geo_list = ["geomean"]

L1 = TickLabel(None, poly_list_l + webcl_list + geo_list)
CB = CBarPlotter(ylabel="Speedup over Best Device", width=15, height=3.4)
CB.setTicks(yspace=[0, 0.5, 1, 1.5], label=L1)
CB.annotate(["Polybench", "WebKit-WebCL"], [[27.5, -.30], [85, -.30]], fontsize=15)

# Figure style
CB.setLegendStyle(ncol=3, size=14, pos=[0.59, 1.18], frame=False)
CB.setFigureStyle(ylim=[0, 1.5], bottomMargin=0.18, fontsize=13,
                  interCmargin=.7, figmargin=0.02)

CB.draw(*PD, barwidth=2)
CB.setBaseOffset(14)
CB.draw(*WD, barwidth=2)
CB.setBaseOffset(14)
CB.draw(*GD, barwidth=2)

g_base = CB.getGlobalBase()

# Line Graph ================================================================================
color = mc["ddgray"]
face = mc["black"]
marker = "o"

# Polybench
PP = PatternParser(tRead("dat/jaws-lbf/poly.dat"))
PP.PickKeyWith("col")
PP.ParseWith("\t")

PLB = []
for i, val in enumerate(poly_list):
    PLB.append(Group(PP, [g_base[i], g_base[i]+2, g_base[i]+4],   val, color=color, face=face, marker=marker))
PLB[0].setLegend("Load Balance Factor")

# WebCL
PP = PatternParser(tRead("dat/jaws-lbf/webcl.dat"))
PP.PickKeyWith("col")
PP.ParseWith("\t")

WLB = []
for i, val in enumerate(webcl_list):
    WLB.append(Group(PP, [g_base[i], g_base[i]+2, g_base[i]+4],   val, color=color, face=face, marker=marker))

# Geomean
PP = PatternParser(tRead("dat/jaws-lbf/geomean.dat"))
PP.PickKeyWith("col")
PP.ParseWith("\t")

GLB = []
for i, val in enumerate(geo_list):
    GLB.append(Group(PP, [g_base[i], g_base[i]+2, g_base[i]+4],   val, color=color, face=face, marker=marker))

twinx = CB.getAxis()

LP = LinePlotter(axis=twinx, ylabel="Load Balance Factor")
LP.setLegendStyle(frame=False, pos=[0.83, 1.18], size=14)
LP.setTicks(yspace=[0, 0.5, 1.0, 1.5])
LP.draw(*PLB)
LP.setBaseOffset(75.2)
LP.draw(*WLB)
LP.setBaseOffset(44.6)
LP.draw(*GLB)

LP.FinalCall()

CB.saveToPdf(output)
