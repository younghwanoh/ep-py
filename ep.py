#!/usr/bin/python

import sys
import re

sys.dont_write_bytecode = True;

# library for ep.py
from parser import PatternParser
from tools import Group
from tools import transpose
from tools import popRow
from tools import popCol
from tools import read
from plotter import LinePlotter

# argument parser
import argparse
argparser = argparse.ArgumentParser()
argparser.add_argument("inFile", help='Specify the name of input data file')
argparser.add_argument("-o","--outFile", help='Specify the name of output PDF file')
argparser.add_argument("-s","--style", help='Specify the style of graphs')
args = argparser.parse_args()

# output file name
output = "output.pdf"
if bool(args.outFile) == True:
    output = arg.outFile

text = read(args.inFile)
style = args.style

# line.dat
if style == "line":

    PP = PatternParser(text)
    PP.PickKeyWith(": ")
    PP.ParseWith(",")

    GPUdata = Group(PP, "GPUprofileQuantum", "GPUthput", color="red", marker="o")
    CPUdata = Group(PP, "CPUprofileQuantum", "CPUthput", color="blue", marker="x")

    GPUdata.setLegend("GPU") 
    CPUdata.setLegend("CPU") 

    LP = LinePlotter(width=5, height=5, title="LinePlot", xlabel="abc", ylabel="ee")
    # LP.setLimitOn(x=[0, 1000], y=[0, 1000])
    LP.draw(GPUdata, CPUdata)
    LP.saveToPdf(output);
    # LP.drawToWindow();

# bar.dat
elif style == "line-data-plain":

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

    LP = LinePlotter(title="LinePlot", xlabel="abc", ylabel="ee")
    LP.setLimitOn(x=[0, 10], y=[0, 10])
    LP.draw(D1,D2,D3,D4)
    LP.saveToPdf(output)

elif style == "3":
    text = "# monitoring\n\
39	29.63501	0-3	2401000\n\
42	31.03067	0-3	2401000\n\
41	31.573883000000002	0-3	2401000\n\
40	30.402679499999998	0-3	2401000\n"
    PP = PatternParser(text);
    PP.ParseWith("\t")
    print(PP.datList)

elif style == "4":
    text = "CPU 0 S: 2.01513671875,796.010986328125,1473.43603515625\n\
CPU 0 E: 795.9951171875,1473.39404296875,2616.083984375\n\
CPU 1 S: 2.02294921875,347.43896484375,685.344970703125,1339.2451171875\n\
CPU 1 E: 347.3779296875,685.326171875,1339.220947265625,2431.3759765625\n\
CPU 2 S: 2.027099609375,348.198974609375,686.010986328125,1361.590087890625\n\
CPU 2 E: 348.18505859375,685.983154296875,1361.51806640625,2549.39111328125\n\
CPU 3 S: 2.031005859375,753.9150390625,1953.3720703125\n\
CPU 3 E: 753.902099609375,1953.31005859375,2056.718017578125\n\
GPU S: 1.994140625,800.839111328125\n\
GPU E: 800.779052734375,2235.4169921875\n"

    PP = PatternParser(text);
    PP.PickKeyWith(": ")
    PP.ParseWith(",")
    print(PP.keyList)
    print("---------------------------------------------")
    print(PP.datList)
