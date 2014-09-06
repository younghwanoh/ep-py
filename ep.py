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
mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292", "blue":"#4455D2",
        "white":"#FFFFFF", "dwhite":"#DFDFDF", "gray":"#888888", "dgray":"#4F4F4F", "black":"#000000"}

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

elif style == "pie":
    # Parse text
    text = tRead("dat/pie.dat")
    PP = PatternParser(text);
    PP.PickKeyWith(": ")

    tag = ["CN", "HL", "YH"]
    colors = [mc["red"], mc["yellow"], mc["blue"]]

    # Draw box
    PIP = PiePlotter(title="PiePlot with start/end points")

    PIP.draw(PP.rowData, legend=tag, colors=colors)
    PIP.saveToPdf(output)

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
                     xlabel="Input Size", ylabel="Exe time")
    # CB.setLimitOn(x=[0, 10], y=[0, 10])
    CB.draw(D1,D2,D3,D4, barwidth=2)
    CB.setTicks(label=L1)
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
                     xlabel="Input Size", ylabel="Speedup")
    # CB.setLimitOn(x=[0, 10], y=[0, 10])
    CB.setTicks(label=L1)
    CB.draw(D1,D2,D3,D4, barwidth=2)
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
    CB = CBarPlotter(title="BarPlot with key format", xlabel="Input Size", ylabel="Speedup",
                     figmargin=0.05)
    CB.setTicks(label=L1, angle=45)
    # CB.setLimitOn(x=[0, 10], y=[0, 10])
    CB.draw(D1,D2,D3,D4, barwidth=2)
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
                      xlabel="Input Size", ylabel="Speedup", figmargin=0.05, groupmargin=1.1)

    CB.setLegendStyle(ncol=8, size=7.5, frame=False)
    CB.setTicks(label=[L1, L2], angle=45)
    CB.setLimitOn(y=[0, 4.5])
    CB.draw(G1, G2, barwidth=2)
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
    BP = CBarPlotter(title="BarPlot with flattend format", ticklabel=L1,
                     xlabel="Input Size", ylabel="Performance", figmargin=0.3)
    # BP.setLimitOn(x=[0, 10], y=[0, 10])
    BP.draw(D1, barwidth=2)
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

elif style == "box-multi-time":

    # Parse text
    text = tRead("dat/box-multi-time.dat")
    PP = PatternParser(text);
    PP.PickKeyWith(": ")
    PP.ParseWith(",")

    # Set data
    D1 = Group(PP, "Schedule 0 S", "Schedule 0 E", color=mc["red"], hatch="")
    D2 = Group(PP, "Memory 0 S", "Memory 0 E", color=mc["yellow"], hatch="//")
    D3 = Group(PP, "Compute 0 S", "Compute 0 E", color=mc["blue"], hatch="")
    G1 = Group(D1, D2, D3)

    D1.setLegend("Schedule")
    D2.setLegend("Memory")
    D3.setLegend("Compute")

    # Set data
    D4 = Group(PP, "Schedule 1 S", "Schedule 1 E", color=mc["red"], hatch="")
    D5 = Group(PP, "Memory 1 S", "Memory 1 E", color=mc["yellow"], hatch="//")
    D6 = Group(PP, "Compute 1 S", "Compute 1 E", color=mc["blue"], hatch="")
    G2 = Group(D4, D5, D6)

    # Set data
    D7 = Group(PP, "Schedule G S", "Schedule G E", color=mc["red"], hatch="")
    D8 = Group(PP, "Memory G S", "Memory G E", color=mc["yellow"], hatch="//")
    D9 = Group(PP, "Compute G S", "Compute G E", color=mc["blue"], hatch="")
    G3 = Group(D7, D8, D9)

    L1 = TickLabel(PP, ["CPU 0", "CPU 1", "GPU"])

    # Draw box
    CBOP = CBoxPlotter(title="BoxPlot with start/end points", width=12, height=5,
                     xlabel="Time (ms)", boxwidth=2, vertical=False, timeline=True)

    CBOP.setLegendStyle(ncol=5, size=13, frame=False)
    CBOP.draw(G1, G2, G3, figmargin=0.4, ticklabel=L1)
    CBOP.saveToPdf(output)

elif style == "jaws":

    key = ["GPU comm0 start", "GPU comm0 end", "GPU comm1 start", "GPU comm1 end", "GPU memcp start", "GPU memcp end",
           "GPU exe start", "GPU exe end", "CPU comm0 start", "CPU comm0 end", "CPU exe0 start", "CPU exe0 end",
           "CPU exe1 start", "CPU exe1 end", "CPU comm1 start", "CPU comm1 end", "GPU comm2 start", "GPU comm2 end"]
    # text = tRead("dat/breakSM.dat")
    # initial = 1409813537567.167
    text = tRead("dat/breakNoSM.dat")
    # initial = 1409814899688.332

    # Use custom parser mode
    PP = PatternParser(text, customKey=key, subtract=True);

    # Set GPU data
    D1 = Group(PP, "GPU comm0 start", "GPU comm0 end", color=mc["yellow"], hatch="//")
    D2 = Group(PP, "GPU comm1 start", "GPU comm1 end", color=mc["yellow"], hatch="//")
    D3 = Group(PP, "GPU comm2 start", "GPU comm2 end", color=mc["yellow"], hatch="//")
    G1 = Group(D1, D2, D3)

    D4 = Group(PP, "GPU memcp start", "GPU memcp end", color=mc["red"], hatch="")
    G2 = Group(D4)

    D5 = Group(PP, "GPU exe start", "GPU exe end", color=mc["blue"], hatch="")
    G3 = Group(D5)

    # Set CPU data
    D6 = Group(PP, "CPU comm0 start", "CPU comm0 end", color=mc["yellow"], hatch="//")
    G4 = Group(D6)

    D7 = Group(PP, "CPU comm1 start", "CPU comm1 end", color=mc["yellow"], hatch="//")
    G5 = Group(D7)

    D8 = Group(PP, "CPU exe0 start", "CPU exe0 end", color=mc["blue"], hatch="")
    G6 = Group(D8)

    D9 = Group(PP, "CPU exe1 start", "CPU exe1 end", color=mc["blue"], hatch="")
    G7 = Group(D9)

    tag = ["GPU comm", "GPU memcp", "GPU exe", "CPU comm0", "CPU comm1", "CPU exe0", "CPU exe1"]
    D1.setLegend(tag[0])
    D4.setLegend(tag[1])
    D5.setLegend(tag[2])
    D6.setLegend(tag[3])
    D7.setLegend(tag[4])
    D8.setLegend(tag[5])
    D9.setLegend(tag[6])

    L1 = TickLabel(PP, tag)

    # Draw box
    CBOP = CBoxPlotter(title="BoxPlot with start/end points", width=14, height=5,
                     xlabel="Time (ms)", boxwidth=2, vertical=False)

    CBOP.setLegendStyle(ncol=5, size=13, frame=False)
    CBOP.draw(G1, G2, G3, G4, G5, G6, G7, figmargin=0.4, ticklabel=L1)
    CBOP.saveToPdf(output)

elif style == "jaws-all":

    key = [ "GPU comm0 start", "GPU comm0 end",
            "GPU comm1 start", "GPU comm1 end",
            "GPU memcp start", "GPU memcp end",
            "GPU exe start", "GPU exe end",
            "GPU comm2 start", "GPU comm2 end",
            "GPU schdl start", "GPU schdl end"]
    # text = tRead("dat/jaws/atax.share.log")
    # text = tRead("dat/breakSM.dat")
    ## text = tRead("dat/breakNoSM.dat")

    tag_ = []
    tag_comm_s = []
    tag_comm_e = []
    tag_exe_s = []
    tag_exe_e = []
    for i in range(10):
        tag_.append("CPU%d" % i)
        tag_comm_s.append("CPU%d comm0 start" % i)
        tag_comm_e.append("CPU%d comm0 end" % i)
        tag_comm_s.append("CPU%d comm1 start" % i)
        tag_comm_e.append("CPU%d comm1 end" % i)
        tag_comm_s.append("CPU%d comm2 start" % i)
        tag_comm_e.append("CPU%d comm2 end" % i)
        tag_exe_s.append("CPU%d exe start" % i)
        tag_exe_e.append("CPU%d exe end" % i)
    key = key + tag_comm_s + tag_comm_e + tag_exe_s + tag_exe_e

    # Use custom parser mode
    PP = PatternParser(text, customKey=key, subtract=True);

    # Set GPU data
    D4 = Group(PP, "GPU memcp start", "GPU memcp end", color=mc["green"], hatch="")
    G1 = Group(D4)

    D1 = Group(PP, "GPU comm0 start", "GPU comm0 end", color=mc["red"], hatch="\\")
    D2 = Group(PP, "GPU comm1 start", "GPU comm1 end", color=mc["yellow"], hatch="\\")
    D3 = Group(PP, "GPU comm2 start", "GPU comm2 end", color=mc["yellow"], hatch="//")
    G2 = Group(D1, D2, D3)

    D5 = Group(PP, "GPU exe start", "GPU exe end", color=mc["blue"], hatch="")
    G3 = Group(D5)

    D6 = Group(PP, "GPU schdl start", "GPU schdl end", color="#428bca", hatch="")
    G4 = Group(D6)

    D = []
    G = []
    # Set CPU data
    for i in range(10):
        D.append(Group(PP, "CPU%d comm0 start" % i, "CPU%d comm0 end" % i, color=mc["red"], hatch="\\"))
        D.append(Group(PP, "CPU%d comm1 start" % i, "CPU%d comm1 end" % i, color=mc["yellow"], hatch="\\"))
        D.append(Group(PP, "CPU%d comm2 start" % i, "CPU%d comm2 end" % i, color=mc["yellow"], hatch="//"))
        D.append(Group(PP, "CPU%d exe start" % i, "CPU%d exe end" % i, color=mc["blue"], hatch=""))
        G.append(Group(D[-4], D[-3], D[-2], D[-1]))

    tag = ["GPU schdl", "GPU memcp", "GPU comm", "GPU exe"] + tag_
    # D1.setLegend(tag[0])
    # D4.setLegend(tag[1])
    # D5.setLegend(tag[2])
    # for i in range(10):
    #     D[i].setLegend(tag[i+3])

    L1 = TickLabel(PP, tag)
    argument = [G4, G1, G2, G3] + G


    D1.setLegend("comm0")
    D2.setLegend("comm1")
    D3.setLegend("comm2")
    D4.setLegend("memcpy")
    D5.setLegend("exe")
    D6.setLegend("schdl")

    # Draw box
    CBOP = CBoxPlotter(title="BoxPlot with start/end points", width=12, height=7,
                     xlabel="Time (ms)", boxwidth=2, vertical=False)

    CBOP.setLegendStyle(ncol=6, size=13, frame=False)
    CBOP.draw(*argument, figmargin=0.1, ticklabel=L1)
    CBOP.saveToPdf(output)

elif style == "jaws-pie":
    key = [ "GPU comm0 start", "GPU comm0 end",
            "GPU comm1 start", "GPU comm1 end",
            "GPU memcp start", "GPU memcp end",
            "GPU exe start", "GPU exe end",
            "GPU comm2 start", "GPU comm2 end",
            "GPU schdl start", "GPU schdl end",
            "DONE"]

    text = tRead("dat/jaws/atax.share.log")

    ## Use custom parser mode
    tag = ["memcp", "comm0", "comm1", "comm2", "schdl"]
    PP = PatternParser(text, customKey=key, subtract=True);
    PP.sumWithRegionKey(tag)
    fraction = PP.getDataArr()

    ## Custom data process after parsing
    fraction[2] -= fraction[0]

    # colors = [mc["green"], mc["red"], mc["yellow"], "#FFBBBB", "#428bca", mc["gray"]]
    colors = [mc["gray"], mc["dgray"], mc["black"], mc["white"], mc["white"], mc["white"]]
    hatch = ["", "", "", "\\\\", "", ".."]

    ## Draw box
    PIP = PiePlotter(title="Pie")

    PIP.draw(fraction, legend=tag, colors=colors, hatch=hatch)
    PIP.saveToPdf(output)

elif style == "bar-stacked":
    key = [ "GPU comm0 start", "GPU comm0 end",
            "GPU comm1 start", "GPU comm1 end",
            "GPU memcp start", "GPU memcp end",
            "GPU exe start", "GPU exe end",
            "GPU comm2 start", "GPU comm2 end",
            "GPU schdl start", "GPU schdl end",
            "DONE"]

    ## Read raw datas
    text_sm = tRead("dat/jaws/%s.share.log" % args.signature)
    text_nsm = tRead("dat/jaws/%s.noshare.log" % args.signature)

    ## Tag lists that will parse
    tag = ["memcp", "comm0", "comm1", "comm2", "schdl"]
    leg = ["memcpy", "init", "task_begin", "task_end", "partition"]

    ## First parsing
    PP = PatternParser(text_sm, customKey=key, subtract=True);
    PP.sumWithRegionKey(tag)
    S_GPUresult = PP.getDataArr()

    ## Second parsing
    PN = PatternParser(text_nsm, customKey=key, subtract=True);
    PN.sumWithRegionKey(tag)
    NS_GPUresult = PN.getDataArr()

    ## Custom data process after parsing
    NS_GPUresult[2] -= NS_GPUresult[0]
    S_GPUresult[2] -= S_GPUresult[0]
    totOverhead = reduce(np.add, NS_GPUresult)

    # Normalized to total sum of data2(NS_GPUresult)
    S_GPUresult = [ i/totOverhead for i in S_GPUresult ]
    NS_GPUresult = [ i/totOverhead for i in NS_GPUresult ]

    # Set style
    colors = [mc["black"], mc["dgray"], mc["gray"], mc["white"], mc["white"]]
    hatch = ["", "", "", "\\\\", ""]

    L1 = TickLabel(PP, ["with-Shared", "without-Shared"])

    ## Draw box
    SBP = SBarPlotter(title=args.signature+" - GPU",
                      xlabel="Strategy", ylabel="Fraction", figmargin=0.4)

    # Set graph style
    SBP.setStackStyle(colors=colors, hatch=hatch, legend=leg)
    SBP.setLegendStyle(ncol=5, size=10, frame=False)

    # Draw
    SBP.setLimitOn(y=[0, 1.2])
    SBP.draw(S_GPUresult, NS_GPUresult, ticklabel=L1, barwidth=1)
    SBP.saveToPdf(output)

elif style == "bar-clustacked":

    benchmarks = ["atax", "syrk", "gemm"]

    ## Assign data directly
    S_CPUresult = []
    NS_CPUresult = []
    S_GPUresult = []
    NS_GPUresult = []

    # atax
    S_CPUresult.append([3.877490234375, 15.810107421874996, 3.2838867187500007,
                        1.8818359375, 57.51716308593768])
    NS_CPUresult.append([1200.7843017578125, 36.7966796875, 53.126953125,
                         4343.073974609375, 158.7681152343721])
    S_GPUresult.append([202.099609375, 1.007080078125, 17.988037109375,
                        1.5107421875, 7.1806640625])
    NS_GPUresult.append([197.38525390625, 1062.109130859375, 420.0341796875,
                         6318.2197265625, 746.284423828125])

    # syrk
    S_CPUresult.append([4.66689453125, 12.704321289062502, 1.7093505859374998,
                        0.748779296875, 33.37495117187518])
    NS_CPUresult.append([72.4834716796875, 5.658862304687499, 796.4159423828124,
                         1.311767578125, 429.0301025390618])
    S_GPUresult.append([18.7412109375, 0.7900390625, 18.235595703125,
                        1.321533203125, 0.72705078125])
    NS_GPUresult.append([18.828125, 64.095947265625, 30.923828125,
                         391.0361328125, 93.978759765625])

    # gemm
    S_CPUresult.append([2.2271484375, 7.4610839843750005, 1.4408935546875,
                        0.8291015625, 77.42680664062391])
    NS_CPUresult.append([105.3399658203125, 7.2691894531250005, 590.9168701171875,
                         1.216064453125, 436.6934082031248])
    S_GPUresult.append([35.37109375, 0.986083984375, 1.62646484375,
                        2.89111328125, 1.29638671875])
    NS_GPUresult.append([32.498291015625, 98.093017578125, 43.816650390625,
                         1232.966552734375, 224.430908203125])

#     # Parse GPU data
#     key = [ "GPU comm0 start", "GPU comm0 end",
#             "GPU comm1 start", "GPU comm1 end",
#             "GPU memcp start", "GPU memcp end",
#             "GPU exe start", "GPU exe end",
#             "GPU comm2 start", "GPU comm2 end",
#             "GPU schdl start", "GPU schdl end",
#             "DONE"]
#
#     S_GPUresult = []
#     NS_GPUresult = []
#
#     for target in benchmarks:
#         ## Read raw datas
#         text_sm = tRead("dat/jaws/%s.share.log" % target)
#         text_nsm = tRead("dat/jaws/%s.noshare.log" % target)
#
#         ## First parsing
#         PP = PatternParser(text_sm, customKey=key, subtract=True);
#         PP.sumWithRegionKey(tag_gpu)
#         S_GPUresult.append(PP.getDataArr())
#
#         ## Second parsing
#         PN = PatternParser(text_nsm, customKey=key, subtract=True);
#         PN.sumWithRegionKey(tag_gpu)
#         NS_GPUresult.append(PN.getDataArr())
#
#         ## Custom data process after parsing
#         NS_GPUresult[-1][2] -= NS_GPUresult[-1][0]
#         S_GPUresult[-1][2] -= S_GPUresult[-1][0]
#
#         totOverhead = reduce(np.add, NS_CPUresult[-1])
#         print(NS_CPUresult[-1])

    l1_label = []
    l2_label = []
    for i in range(len(benchmarks)):
        GPUOverhead = reduce(np.add, NS_GPUresult[i])
        CPUOverhead = reduce(np.add, NS_CPUresult[i])

        # Normalized to total sum of data(NS_CPUresult)
        S_GPUresult[i] = [ j/GPUOverhead for j in S_GPUresult[i] ]
        NS_GPUresult[i] = [ j/GPUOverhead for j in NS_GPUresult[i] ]
        S_CPUresult[i] = [ j/CPUOverhead for j in S_CPUresult[i] ]
        NS_CPUresult[i] = [ j/CPUOverhead for j in NS_CPUresult[i] ]
        l1_label += ["S", "N", "S", "N"]
        l2_label += ["GPU", "CPU"]

        # Zero padding for legend
        S_GPUresult[i] = S_GPUresult[i] + [0]
        NS_GPUresult[i] = NS_GPUresult[i] + [0]
        S_CPUresult[i] = [0] + S_CPUresult[i] 
        NS_CPUresult[i] = [0] + NS_CPUresult[i]

    ## Tag lists that will parse
    tag_cpu = ["comm0", "comm1", "comm2", "schdl", "barrier"]
    tag_gpu = ["memcp", "comm0", "comm1", "comm2", "schdl"]
    leg = ["memcpy", "init", "task_begin", "task_end", "partition", "sync"]

    ## Set style
    colors = [mc["black"], mc["dgray"], mc["gray"], mc["white"], mc["white"], mc["dwhite"]]
    hatch = ["", "", "", "\\\\", "", ""]

    ## Level of lables
    L1 = TickLabel(None, l1_label)
    L2 = TickLabel(None, l2_label)

    ## Draw box
    SBP = SBarPlotter(title="Normalized overhead to each device",
                      xlabel="Strategy", ylabel="Fraction", figmargin=0.05,
                      t1_label=L1, t2_label=L2, tickangle=45)

    # Set graph styles
    SBP.setLegendStyle(ncol=3, size=10, frame=False)
    SBP.setStackStyle(colors=colors, hatch=hatch, legend=leg)
    SBP.setBottomMargin(0.15)

    # Draw graphs
    SBP.setLimitOn(y=[0, 1.2])
    for i in range(len(benchmarks)):
        SBP.draw(S_GPUresult[i], NS_GPUresult[i], barwidth=1)
        SBP.setBaseOffset(1.1)
        SBP.draw(S_CPUresult[i], NS_CPUresult[i], barwidth=1)
        SBP.setBaseOffset(2)

    SBP.saveToPdf(output)
