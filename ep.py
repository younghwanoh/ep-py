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
argparser.add_argument("-o","--outFile", help='Specify the name of output PDF file')
argparser.add_argument("-s","--style", help='Specify the style of graphs')
args = argparser.parse_args()

# output file name
output = "output.pdf"
if bool(args.outFile) == True:
    output = args.outFile

if bool(args.inFile) == True:
    text = tRead(args.inFile)

style = "bar-flat"
if bool(args.style) == True:
    style = args.style

# line graph with special key
if style == "line-key":
    text = tRead("dat/line.dat")

    PP = PatternParser(text)
    PP.PickKeyWith(": ")
    PP.ParseWith(",")

    GPUdata = Group(PP, "GPUprofileQuantum", "GPUthput", color="red", marker="o")
    CPUdata = Group(PP, "CPUprofileQuantum", "CPUthput", color="blue", marker="x")

    GPUdata.setLegend("GPU") 
    CPUdata.setLegend("CPU") 

    LP = LinePlotter(width=5, height=5, title="LinePlot with key", xlabel="abc", ylabel="ee")
    # LP.setLimitOn(x=[0, 1000], y=[0, 1000])
    LP.draw(GPUdata, CPUdata)
    LP.saveToPdf(output);
    # LP.drawToWindow();

# line graph without special key
if style == "line-raw":
    text = tRead("dat/line-raw.dat")

    PP = PatternParser(text)
    PP.ParseWith(",")

    # Grouping input with raw matrix data
    GPUdata = Group(None, PP.datList[1], PP.datList[3], color="red", marker="o")
    CPUdata = Group(None, PP.datList[0], PP.datList[2], color="blue", marker="x")

    GPUdata.setLegend("GPU") 
    CPUdata.setLegend("CPU") 

    LP = LinePlotter(width=5, height=5, title="LinePlot with raw", xlabel="abc", ylabel="ee")
    # LP.setLimitOn(x=[0, 1000], y=[0, 1000])
    LP.draw(GPUdata, CPUdata)
    LP.saveToPdf(output);
    # LP.drawToWindow();

# line graph with single parsed y-array
elif style == "line-flat":
    text = tRead("dat/flat.dat")

    PP = PatternParser(text)
    PP.PickKeyWith("row")
    PP.ParseWith("\t")

    D1 = Group(PP, [1,2,3,4], "seq",      color="red", marker="o")
    D2 = Group(PP, [1,2,3,4], "cpu-only", color="blue", marker="x")
    D3 = Group(PP, [1,2,3,4], "gpu-only", color="green", marker="o")
    D4 = Group(PP, [1,2,3,4], "cpu+gpu",  color="black", marker="x")

    # D1.setLegend("SEQ") 
    # D2.setLegend("CPU-only") 
    # D3.setLegend("GPU-only") 
    # D4.setLegend("CPU+GPU") 

    LP = LinePlotter(title="LinePlot with flattend format", xlabel="abc", ylabel="ee")
    LP.setLimitOn(x=[0, 10], y=[0, 10])
    LP.draw(D1,D2,D3,D4)
    LP.saveToPdf(output)

# line graph with normalization to denoted key
elif style == "line-norm":
    text = tRead("dat/line-norm.dat")

    PP = PatternParser(text)
    PP.PickKeyWith(": ")
    PP.ParseWith("\t")
    PP.datNormTo("SEQavg", opt="speedup") # option: speedup, exetime

    D1 = Group(PP, "data", "Profile", color="red", marker="o")
    D2 = Group(PP, "data", "CGCEavg", color="blue", marker="x")
    D3 = Group(PP, "data", "SEQiavg", color="green", marker="o")
    D4 = Group(PP, "data", "GPUiavg", color="black", marker="x")

    # D1.setLegend("SEQ") 
    # D2.setLegend("CPU-only") 
    # D3.setLegend("GPU-only") 
    # D4.setLegend("CPU+GPU") 

    LP = LinePlotter(title="Normalized LinePlot", xlabel="abc", ylabel="ee")
    LP.draw(D1,D2,D3,D4)
    LP.saveToPdf(output)

# getter test
elif style == "getter-test":
    text = tRead("dat/box.dat")
    writeLine = csv.writer(stdout, delimiter='\n')

    PP = PatternParser(text);
    PP.PickKeyWith(": ")
    PP.ParseWith(",")
    print("Key ---------------------------------------------")
    print(PP.getKeyArr())
    print("\nData --------------------------------------------")
    writeLine.writerow(PP.getDataArr())
    print("\nKey with index 0 --------------------------------")
    print(PP.getKeyArr(0))
    print("\nRow Data with index 0 ---------------------------")
    print(PP.getDataArr(0, opt="row")) # by default, opt is row
    print("\nCol Data with index 0 ---------------------------")
    print(PP.getDataArr(0, opt="col"))
    print("\nGet Data without Copy ------------------------------")
    print("Before return value update")
    print("a = PP.getDataArr(0)")
    a = PP.getDataArr(0)
    print(a)
    print("\nAfter return value update")
    print("a[0] = \"I'm Refed Here !\"")
    a[0] = "I'm Refed Here !"
    print(PP.getDataArr(0))
    print("\nGet Data with Copy ------------------------------")
    print("Before return value update")
    print("a = PP.getDataArr(0, copy=True)")
    b = PP.getDataArr(0, copy=True)
    print(a)
    print("\nAfter return value update")
    print("a[0] = \"I'm Copied Here !\"")
    b[0] = "I'm Copied Here !"
    print(PP.getDataArr(0))

# bar graph
elif style == "bar-clustered":
    text = tRead("dat/bar-clustered.dat")

    # Parse text
    PP = PatternParser(text)
    PP.PickKeyWith("row")
    PP.ParseWith("\t")

    # Set data
    D1 = Group(PP, "seq",      color="red", hatch="-")
    D2 = Group(PP, "cpu-only", color="blue")
    D3 = Group(PP, "gpu-only", color="green", hatch="||")
    D4 = Group(PP, "cpu+gpu",  color="black")

    D1.setLegend("SEQ") 
    D2.setLegend("CPU-only") 
    D3.setLegend("GPU-only") 
    D4.setLegend("CPU+GPU") 

    # Set label with key
    L1 = TickLabel(PP, "label")

    # Set label manually
    # L1 = TickLabel(None, ["label","1","2",1])

    # Draw bar
    CB = CBarPlotter(title="BarPlot with flattend format",
                     xlabel="Input Size", ylabel="Exe time", barwidth=2)
    # CB.setLimitOn(x=[0, 10], y=[0, 10])
    CB.draw(D1,D2,D3,D4, ticklabel=L1)
    CB.saveToPdf(output)

elif style == "bar-norm-clustered":
    text = tRead("dat/bar-clustered.dat")

    # Parse text
    PP = PatternParser(text)
    PP.PickKeyWith("row")
    PP.ParseWith("\t")
    PP.datNormTo("gpu-only", opt="speedup") # option: speedup, exetime

    # Set data
    D1 = Group(PP, "seq",      color="red", hatch="-")
    D2 = Group(PP, "cpu-only", color="blue")
    D3 = Group(PP, "gpu-only", color="green", hatch="||")
    D4 = Group(PP, "cpu+gpu",  color="black")

    D1.setLegend("SEQ") 
    D2.setLegend("CPU-only") 
    D3.setLegend("GPU-only") 
    D4.setLegend("CPU+GPU") 

    # Set label with key
    L1 = TickLabel(PP, "label")

    # Set label manually
    # L1 = TickLabel(None, ["label","1","2",1])

    # Draw bar
    CB = CBarPlotter(title="Normalized BarPlot with flattend format",
                     xlabel="Input Size", ylabel="Speedup", barwidth=2)
    # CB.setLimitOn(x=[0, 10], y=[0, 10])
    CB.draw(D1,D2,D3,D4, ticklabel=L1)
    CB.saveToPdf(output)

elif style == "bar-key-clustered":
    text = tRead("dat/bar-key.dat")

    # Parse text
    PP = PatternParser(text)
    PP.PickKeyWith(": ")
    PP.ParseWith("\t")

    # Set label with key
    L1 = TickLabel(PP, "data")

    # Normalization must be occured after grouping TickLabel
    PP.datNormTo("SEQavg", opt="speedup") # option: speedup, exetime

    # Set data
    D1 = Group(PP, "SEQiavg", color="red", hatch="-")
    D2 = Group(PP, "GPUiavg", color="blue")
    D3 = Group(PP, "CGCEavg", color="green", hatch="||")
    D4 = Group(PP, "Profile", color="black")

    D1.setLegend("CPU-only") 
    D2.setLegend("GPU-only") 
    D3.setLegend("CGCE-only") 
    D4.setLegend("CGCE+profile") 


    # Set label manually
    # L1 = TickLabel(None, ["label","1","2",1])

    # Draw bar
    CB = CBarPlotter(title="BarPlot with key format",
                     xlabel="Input Size", ylabel="Speedup", barwidth=2)
    # CB.setLimitOn(x=[0, 10], y=[0, 10])
    CB.draw(D1,D2,D3,D4, ticklabel=L1, tickangle=45, figmargin=0.05)
    CB.saveToPdf(output)

elif style == "bar-key-cc":
    text = tRead("dat/bar-key-cc.dat")

    # Parse text
    PP = PatternParser(text)
    PP.PickKeyWith(": ")
    PP.ParseWith("\t")

    # Set label with key
    L1 = TickLabel(PP, "data")
    L2 = TickLabel(PP, "data")

    # Normalization must be occured after grouping TickLabel
    PP.datNormTo("SEQavg", opt="speedup") # option: speedup, exetime

    # Set data
    D1 = Group(PP, "SEQiavg", color="red", hatch="-")
    D2 = Group(PP, "GPUiavg", color="blue")
    D3 = Group(PP, "CGCEavg", color="green", hatch="||")
    D4 = Group(PP, "Profile", color="black")
    G1 = Group(D1, D2, D3, D4)

    D5 = Group(PP, "Savg", color="red", hatch="-")
    D6 = Group(PP, "Cavg", color="green", hatch="||")
    D7 = Group(PP, "Prof", color="black")
    G2 = Group(D5, D6, D7)

    D1.setLegend("CPU-only") 
    D2.setLegend("GPU-only") 
    D3.setLegend("CGCE-only") 
    D4.setLegend("CGCE+profile") 

    D5.setLegend("C-only") 
    D6.setLegend("CG-only") 
    D7.setLegend("CG+profile") 

    # Draw bar
    CB = CCBarPlotter(title="BarPlot with key format", width=10, height=4,
                      xlabel="Input Size", ylabel="Speedup", barwidth=2)
    CB.setLegendStyle(ncol=8, size=7.5, frame=False)
    CB.setLimitOn(y=[0, 4.5])
    CB.draw(G1, G2, ticklabel=[L1, L2], tickangle=45, figmargin=0.05, groupmargin=1.1)
    CB.saveToPdf(output)

elif style == "bar-single":
    text = tRead("dat/flat.dat")

    # Parse text
    PP = PatternParser(text)
    PP.PickKeyWith("row")
    PP.ParseWith("\t")

    # Set data
    D1 = Group(PP, "gpu-only", color="green", hatch="||")
    D1.setLegend("GPU-only") 

    # Set label with key
    L1 = TickLabel(PP, "label")

    # Draw bar
    BP = CBarPlotter(title="BarPlot with flattend format",
                     xlabel="Input Size", ylabel="Performance", barwidth=2)
    # BP.setLimitOn(x=[0, 10], y=[0, 10])
    BP.draw(D1, ticklabel=L1, figmargin=0.3)
    BP.saveToPdf(output)

# box graph
elif style == "box-key":
    text = tRead("dat/box.dat")

    # Parse text
    PP = PatternParser(text);
    PP.PickKeyWith(": ")
    PP.ParseWith(",")

    # Set data
    D1 = Group(PP, "CPU 0 S", "CPU 0 E", color="#225522", hatch="")
    D1.setLegend("CPU 0")
    D2 = Group(PP, "CPU 1 S", "CPU 1 E", color="#BC434C", hatch="")
    D2.setLegend("CPU 1")
    D3 = Group(PP, "CPU 2 S", "CPU 2 E", color="#FFBB00", hatch="")
    D3.setLegend("CPU 2")
    D4 = Group(PP, "CPU 3 S", "CPU 3 E", color="#B82E92", hatch="")
    D4.setLegend("CPU 3")
    D5 = Group(PP, "GPU S", "GPU E", color="#4455D2", hatch="")
    D5.setLegend("GPU")

    # Set label with key
    L1 = TickLabel(None, ["CPU 0", "CPU 1", "CPU 2", "CPU 3", "GPU 0"])

    # Draw box
    BOP = BoxPlotter(title="BoxPlot with start/end points",
                     xlabel="Device", ylabel="Degree of process", boxwidth=2, vertical=True, timeline=False) 
    BOP.draw(D1, D2, D3, D4, D5, ticklabel=L1)
    BOP.saveToPdf(output)

# box graph
elif style == "box-time":
    text = tRead("dat/box-time.dat")

    # Parse text
    PP = PatternParser(text);
    PP.PickKeyWith(": ")
    PP.ParseWith(",")

    # Set data
    D1 = Group(PP, "CPU 0 S", "CPU 0 E", color="#225522", hatch="")
    D1.setLegend("CPU 0")
    D2 = Group(PP, "CPU 1 S", "CPU 1 E", color="#BC434C", hatch="")
    D2.setLegend("CPU 1")
    D3 = Group(PP, "CPU 2 S", "CPU 2 E", color="#FFBB00", hatch="")
    D3.setLegend("CPU 2")
    D4 = Group(PP, "CPU 3 S", "CPU 3 E", color="#B82E92", hatch="")
    D4.setLegend("CPU 3")
    D5 = Group(PP, "GPU S", "GPU E", color="#4455D2", hatch="")
    D5.setLegend("GPU")

    # Draw box
    BOP = BoxPlotter(title="BoxPlot with start/end points", width=10, height=4,
                     xlabel="Time", ylabel="Running Device", boxwidth=2, vertical=False, timeline=True)

    BOP.setLegendStyle(ncol=5, size=12, frame=False) 
    BOP.draw(D1, D2, D3, D4, D5, figmargin=0.8)
    BOP.saveToPdf(output)

elif style == "multiplot-2box":
    text = tRead("dat/box-time.dat")

    # Parse text
    PP = PatternParser(text);
    PP.PickKeyWith(": ")
    PP.ParseWith(",")

    # Set data
    D1 = Group(PP, "CPU 0 S", "CPU 0 E", color="#225522", hatch="")
    D2 = Group(PP, "CPU 1 S", "CPU 1 E", color="#BC434C", hatch="")
    D3 = Group(PP, "CPU 2 S", "CPU 2 E", color="#FFBB00", hatch="")
    D4 = Group(PP, "CPU 3 S", "CPU 3 E", color="#B82E92", hatch="")
    D5 = Group(PP, "GPU S", "GPU E", color="#4455D2", hatch="")

    # D1.setLegend("CPU 0")
    # D2.setLegend("CPU 1")
    # D3.setLegend("CPU 2")
    # D4.setLegend("CPU 3")
    # D5.setLegend("GPU")

    # Draw box
    BOP = BoxPlotter(title="BoxPlot with start/end points", width=10, height=4,
                     xlabel="Time", ylabel="Running Device", boxwidth=2, vertical=False, timeline=True)

    # BOP.setLegendStyle(ncol=5, size=12, frame=False) 
    BOP.draw(D1, D2, D3, D4, D5, figmargin=0.8)

    text = tRead("dat/box-time1.dat")

    # Parse text
    PP = PatternParser(text);
    PP.PickKeyWith(": ")
    PP.ParseWith(",")

    # Set data
    D6 = Group(PP, "CPU 0 S", "CPU 0 E", color="#225522", hatch="")

    BOP.draw(D6, figmargin=0.8)
    BOP.saveToPdf(output)
