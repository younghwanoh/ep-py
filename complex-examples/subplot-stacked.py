#!/usr/bin/python

import csv
from sys import stdout

import numpy as np
import epic as ep

args = ep.parseCommandArgs() 

# color macro dictionary
mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292",
      "blue":"#4455D2", "white":"#FFFFFF", "ddwhite":"#B3B3B3", "dwhite":"#DFDFDF",
      "gray":"#888888", "dgray":"#4F4F4F", "black":"#000000"}

# output file name
output = "subplot-stacked.pdf"
if bool(args.outFile) == True:
    output = args.outFile

if bool(args.inFile) == True:
    text = ep.tRead(args.inFile)

if bool(args.style) == True:
    style = args.style

# benchmarks = ["atax", "syrk", "gemm"]
benchmarks = ["QA", "Inference"]

## Assign data directly
result = []

# arc-yhlinux
# # infer
# result.append([100, 0]) # MemN2N
# result.append([45.6, 54.4]) # KV-MemN2N
# result.append([50.7, 49.3]) # BERT - CPU
#
# # qa
# result.append([100, 0]) # MemN2N
# result.append([80.2, 19.8]) # KV-MemN2N
# result.append([50.7, 49.3]) # BERT - CPU

# Xeon
# infer
result.append([100, 0]) # MemN2N
result.append([32.7, 67.3]) # KV-MemN2N
result.append([24.6, 75.4]) # BERT - CPU
result.append([45.3, 54.7]) # BERT - GPU

# qa
result.append([100, 0]) # MemN2N
result.append([95.3, 4.7]) # KV-MemN2N
result.append([24.6, 75.4]) # BERT - CPU
result.append([45.3, 54.7]) # BERT - GPU

## Tag lists that will parse
leg = ["Attention", "Others"]

## Set style
colors = ["#3a3a3a", mc["dwhite"]]
hatch = ["", ""]


SP = ep.SubPlotter((2,1), sharex=True, width=7, height=4)
SP.adjust(hspace=0.3)

## Draw box
SBP = ep.SBarPlotter(axis=SP.getAxis(0), title="",
                  xlabel="", ylabel="FLOPs (%)")

# Set manual ticks
# tlabel = ["BERT (GPU)", "BERT (CPU)", "KV-MemN2N", "MemN2N"]*2
tlabel = ["MemN2N", "KV-\nMemN2N", "BERT\n(CPU)", "BERT\n(GPU)"]*2

L1 = ep.TickLabel(None, tlabel)

# Set graph styles
SBP.setLegendStyle(ncol=2, size=13, frame=False, pos=[0.77,1.4])
SBP.setFigureStyle(figmargin=0.06, bottomMargin=0.35, topMargin=0.87, ylim=[0, 100], gridy=True, fontsize=13)
SBP.setStackStyle(colors=colors, hatch=hatch, legend=leg) # alert! transposed data

SBP.setTicks(label=L1, align="center", fontsize=10)

# annoty = list(np.zeros(len(annotx))+0.76)

# annoty = list(np.zeros(len(annotx))+0.76)
# annotxy = zip(*[annotx,annoty])
# SBP.annotate(["Inference time","QA time"], annotxy, fontsize=13, color=mc["ddwhite"], fontweight='bold')

# Draw graphs
for i in range(len(benchmarks)):
    SBP.draw(result[4*i], barwidth=0.6)
    SBP.setBaseOffset(1.1)
    SBP.draw(result[4*i+1], barwidth=.6)
    SBP.setBaseOffset(1.1)
    SBP.draw(result[4*i+2], barwidth=.6)
    SBP.setBaseOffset(1.1)
    SBP.draw(result[4*i+3], barwidth=.6)
    SBP.setBaseOffset(1.65)

SBP.finish()

SBP1 = ep.SBarPlotter(axis=SP.getAxis(1), title="",
                  xlabel="", ylabel="Latency (%)", flushLegend=True)

# SBP1.setLegendStyle(ncol=2, size=13, frame=False, pos=[0.77,1.35])
SBP1.setFigureStyle(figmargin=0.06, bottomMargin=0.35, topMargin=0.87, ylim=[0, 100], gridy=True, fontsize=13)
SBP1.setStackStyle(colors=colors, hatch=hatch, legend=leg) # alert! transposed data

SBP1.annotate(["(a)"], [[4.08, 1.08]], fontsize=14)
SBP1.annotate(["(b)"], [[4.08, -0.67]], fontsize=14)
annotx = [0.08, 4.71]
annoty = list(np.zeros(len(annotx))-0.62)
annotxy = zip(*[annotx,annoty])
SBP1.annotate(["Whole Inference Time","Question-Answering Time"], annotxy, fontsize=14, fontweight="bold")

L1 = ep.TickLabel(None, tlabel)
SBP1.setTicks(label=L1, align="center", fontsize=10)

for i in range(len(benchmarks)):
    SBP1.draw(result[4*i], barwidth=0.6)
    SBP1.setBaseOffset(1.1)
    SBP1.draw(result[4*i+1], barwidth=.6)
    SBP1.setBaseOffset(1.1)
    SBP1.draw(result[4*i+2], barwidth=.6)
    SBP1.setBaseOffset(1.1)
    SBP1.draw(result[4*i+3], barwidth=.6)
    SBP1.setBaseOffset(1.65)

SBP1.finish()


SP.saveToPdf(output)
