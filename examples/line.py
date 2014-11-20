#!/usr/bin/python

# import sys
# sys.dont_write_bytecode = True;

# library for ep.py
import epic as ep

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
text = ep.tRead("../dat/line.dat")

PP = ep.PatternParser(text)
PP.PickKeyWith(": ")
PP.ParseWith(",")

GPUdata = ep.Group(PP, "GPUprofileQuantum", "GPUthput", color="red", marker="o")
CPUdata = ep.Group(PP, "CPUprofileQuantum", "CPUthput", color="blue", marker="x")

GPUdata.setLegend("GPU") 
CPUdata.setLegend("CPU") 

LP = ep.LinePlotter(width=5, height=5, title="LinePlot with key", xlabel="abc", ylabel="ee")
# LP.setFigureStyle(xlim=[0, 1000], ylim=[0, 1000])
LP.draw(GPUdata, CPUdata)
LP.saveToPdf("line.pdf");
