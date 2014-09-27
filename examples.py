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
output = "output.pdf"
if bool(args.outFile) == True:
    output = args.outFile

if bool(args.inFile) == True:
    text = ep.tRead(args.inFile)

if bool(args.style) == True:
    style = args.style

# line graph with special key
if style == "line-key":
    text = ep.tRead("dat/line.dat")

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
    LP.saveToPdf(output);
    # LP.drawToWindow();

# line graph without special key
if style == "line-raw":
    text = ep.tRead("dat/line-raw.dat")

    PP = ep.PatternParser(text)
    PP.ParseWith(",")

    # Grouping input with raw matrix data
    GPUdata = ep.Group(None, PP.datList[1], PP.datList[3], color="red", marker="o")
    CPUdata = ep.Group(None, PP.datList[0], PP.datList[2], color="blue", marker="x")

    GPUdata.setLegend("GPU") 
    CPUdata.setLegend("CPU") 

    LP = ep.LinePlotter(width=5, height=5, title="LinePlot with raw", xlabel="abc", ylabel="ee")
    # LP.setFigureStyle(xlim=[0, 1000], ylim=[0, 1000])
    LP.draw(GPUdata, CPUdata)
    LP.saveToPdf(output);
    # LP.drawToWindow();

# line graph with single parsed y-array
elif style == "line-flat":
    text = ep.tRead("dat/flat.dat")

    PP = ep.PatternParser(text)
    PP.PickKeyWith("row")
    PP.ParseWith("\t")

    D1 = ep.Group(PP, [1,2,3,4], "seq",      color="red", marker="o")
    D2 = ep.Group(PP, [1,2,3,4], "cpu-only", color="blue", marker="x")
    D3 = ep.Group(PP, [1,2,3,4], "gpu-only", color="green", marker="o")
    D4 = ep.Group(PP, [1,2,3,4], "cpu+gpu",  color="black", marker="x")

    D1.setLegend("SEQ") 
    D2.setLegend("CPU-only") 
    D3.setLegend("GPU-only") 
    D4.setLegend("CPU+GPU") 

    LP = ep.LinePlotter(title="LinePlot with flattend format", xlabel="abc", ylabel="ee")
    LP.setFigureStyle(xlim=[0, 10], ylim=[0, 10])
    LP.draw(D1,D2,D3,D4)
    LP.saveToPdf(output)

# line graph with normalization to denoted key
elif style == "line-norm":
    text = ep.tRead("dat/line-norm.dat")

    PP = ep.PatternParser(text)
    PP.PickKeyWith(": ")
    PP.ParseWith("\t")
    PP.datNormTo("SEQavg", opt="speedup") # option: speedup, exetime

    D1 = ep.Group(PP, "data", "Profile", color="red", marker="o")
    D2 = ep.Group(PP, "data", "CGCEavg", color="blue", marker="x")
    D3 = ep.Group(PP, "data", "SEQiavg", color="green", marker="o")
    D4 = ep.Group(PP, "data", "GPUiavg", color="black", marker="x")

    D1.setLegend("SEQ") 
    D2.setLegend("CPU-only") 
    D3.setLegend("GPU-only") 
    D4.setLegend("CPU+GPU") 

    LP = ep.LinePlotter(title="Normalized LinePlot", xlabel="abc", ylabel="ee")
    LP.draw(D1,D2,D3,D4)
    LP.saveToPdf(output)

elif style == "pie":
    # Parse text
    text = ep.tRead("dat/pie.dat")
    PP = ep.PatternParser(text);
    PP.PickKeyWith(": ")

    tag = ["CN", "HL", "YH"]
    colors = [mc["red"], mc["yellow"], mc["blue"]]

    # Draw box
    PIP = ep.PiePlotter(title="PiePlot with start/end points")

    PIP.draw(PP.rowData, legend=tag, colors=colors)
    PIP.saveToPdf(output)

# getter test
elif style == "getter-test":
    text = ep.tRead("dat/box.dat")
    writeLine = csv.writer(stdout, delimiter='\n')

    PP = ep.PatternParser(text);
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
    text = ep.tRead("dat/bar-clustered.dat")

    # Parse text
    PP = ep.PatternParser(text)
    PP.PickKeyWith("row")
    PP.ParseWith("\t")

    # Set data
    D1 = ep.Group(PP, "seq",      color="red", hatch="-")
    D2 = ep.Group(PP, "cpu-only", color="blue")
    D3 = ep.Group(PP, "gpu-only", color="green", hatch="||")
    D4 = ep.Group(PP, "cpu+gpu",  color="black")

    D1.setLegend("SEQ") 
    D2.setLegend("CPU-only") 
    D3.setLegend("GPU-only") 
    D4.setLegend("CPU+GPU") 

    # Set label with key
    L1 = ep.TickLabel(PP, "label")

    # Set label manually
    # L1 = ep.TickLabel(None, ["label","1","2",1])

    # Draw bar
    CB = ep.CBarPlotter(title="BarPlot with flattend format",
                     xlabel="Input Size", ylabel="Exe time")
    # CB.setLimitOn(x=[0, 10], y=[0, 10])
    CB.draw(D1,D2,D3,D4, barwidth=2)
    CB.setTicks(label=L1)
    CB.saveToPdf(output)

elif style == "bar-norm-clustered":
    text = ep.tRead("dat/bar-clustered.dat")

    # Parse text
    PP = ep.PatternParser(text)
    PP.PickKeyWith("row")
    PP.ParseWith("\t")
    PP.datNormTo("gpu-only", opt="speedup") # option: speedup, exetime

    # Set data
    D1 = ep.Group(PP, "seq",      color="red", hatch="-")
    D2 = ep.Group(PP, "cpu-only", color="blue")
    D3 = ep.Group(PP, "gpu-only", color="green", hatch="||")
    D4 = ep.Group(PP, "cpu+gpu",  color="black")

    D1.setLegend("SEQ") 
    D2.setLegend("CPU-only") 
    D3.setLegend("GPU-only") 
    D4.setLegend("CPU+GPU") 

    # Set label with key
    L1 = ep.TickLabel(PP, "label")

    # Set label manually
    # L1 = ep.TickLabel(None, ["label","1","2",1])

    # Draw bar
    CB = ep.CBarPlotter(title="Normalized BarPlot with flattend format",
                     xlabel="Input Size", ylabel="Speedup")
    # CB.setLimitOn(x=[0, 10], y=[0, 10])
    CB.setTicks(label=L1)
    CB.draw(D1,D2,D3,D4, barwidth=2)
    CB.saveToPdf(output)

elif style == "bar-key-clustered":
    text = ep.tRead("dat/bar-key.dat")

    # Parse text
    PP = ep.PatternParser(text)
    PP.PickKeyWith(": ")
    PP.ParseWith("\t")

    # Set label with key
    L1 = ep.TickLabel(PP, "data")

    # Normalization must be occured after grouping TickLabel
    PP.datNormTo("SEQavg", opt="speedup") # option: speedup, exetime

    # Set data
    D1 = ep.Group(PP, "SEQiavg", color="red", hatch="-")
    D2 = ep.Group(PP, "GPUiavg", color="blue")
    D3 = ep.Group(PP, "CGCEavg", color="green", hatch="||")
    D4 = ep.Group(PP, "Profile", color="black")

    D1.setLegend("CPU-only") 
    D2.setLegend("GPU-only") 
    D3.setLegend("CGCE-only") 
    D4.setLegend("CGCE+profile") 

    # Set label manually
    # L1 = ep.TickLabel(None, ["label","1","2",1])

    # Draw bar
    CB = ep.CBarPlotter(title="BarPlot with key format", xlabel="Input Size", ylabel="Speedup")
    CB.setTicks(label=L1, angle=45)
    CB.setFigureStyle(figmargin=0.05, xlim=[0, 10], ylim=[0, 5])
    CB.draw(D1,D2,D3,D4, barwidth=2)
    CB.saveToPdf(output)

elif style == "bar-key-cc":
    text = ep.tRead("dat/bar-key-cc.dat")

    # Parse text
    PP = ep.PatternParser(text)
    PP.PickKeyWith(": ")
    PP.ParseWith("\t")

    # Set label with key
    L1 = ep.TickLabel(PP, "data")
    L2 = ep.TickLabel(PP, "data2")

    # Normalization must be occured after grouping TickLabel
    PP.datNormTo("SEQavg", opt="speedup") # option: speedup, exetime

    # Set data
    D1 = ep.Group(PP, "SEQiavg", color="red", hatch="-")
    D2 = ep.Group(PP, "GPUiavg", color="blue")
    D3 = ep.Group(PP, "CGCEavg", color="green", hatch="||")
    D4 = ep.Group(PP, "Profile", color="black")
    G1 = ep.Group(D1, D2, D3, D4)

    D5 = ep.Group(PP, "Savg", color="red", hatch="-")
    D6 = ep.Group(PP, "Cavg", color="green", hatch="||")
    D7 = ep.Group(PP, "Prof", color="black")
    G2 = ep.Group(D5, D6, D7)

    D1.setLegend("CPU-only") 
    D2.setLegend("GPU-only") 
    D3.setLegend("CGCE-only") 
    D4.setLegend("CGCE+profile") 

    D5.setLegend("C-only") 
    D6.setLegend("CG-only") 
    D7.setLegend("CG+profile") 

    # Draw bar
    CB = ep.CCBarPlotter(title="BarPlot with key format", width=10, height=4,
                         xlabel="Input Size", ylabel="Speedup")

    CB.setLegendStyle(ncol=8, size=7.5, frame=False, loc="upper center")
    CB.setTicks(label=[L1, L2], angle=45)
    CB.setFigureStyle(ylim=[0, 4.5], figmargin=0.05, groupmargin=1.1)
    CB.draw(G1, G2, barwidth=2)
    CB.saveToPdf(output)

elif style == "bar-single":
    text = ep.tRead("dat/flat.dat")

    # Parse text
    PP = ep.PatternParser(text)
    PP.PickKeyWith("row")
    PP.ParseWith("\t")

    # Set data
    D1 = ep.Group(PP, "gpu-only", color="green", hatch="||")
    D1.setLegend("GPU-only") 

    # Set label with key
    L1 = ep.TickLabel(PP, "label")

    # Draw bar
    BP = ep.CBarPlotter(title="BarPlot with flattend format",
                        xlabel="Input Size", ylabel="Performance")
    # BP.setFigureStyle(xlim=[0, 10], ylim=[0, 10], figmargin=0.3)
    BP.setFigureStyle(figmargin=0.3)
    BP.setTicks(label=L1)
    BP.draw(D1, barwidth=2)
    BP.saveToPdf(output)

# box graph
elif style == "box-key":
    text = ep.tRead("dat/box.dat")

    # Parse text
    PP = ep.PatternParser(text);
    PP.PickKeyWith(": ")
    PP.ParseWith(",")

    # Set data
    D1 = ep.Group(PP, "CPU 0 S", "CPU 0 E", color="#225522", hatch="")
    D1.setLegend("CPU 0")
    D2 = ep.Group(PP, "CPU 1 S", "CPU 1 E", color="#BC434C", hatch="")
    D2.setLegend("CPU 1")
    D3 = ep.Group(PP, "CPU 2 S", "CPU 2 E", color="#FFBB00", hatch="")
    D3.setLegend("CPU 2")
    D4 = ep.Group(PP, "CPU 3 S", "CPU 3 E", color="#B82E92", hatch="")
    D4.setLegend("CPU 3")
    D5 = ep.Group(PP, "GPU S", "GPU E", color="#4455D2", hatch="")
    D5.setLegend("GPU")

    # Set label with key
    L1 = ep.TickLabel(None, ["CPU 0", "CPU 1", "CPU 2", "CPU 3", "GPU 0"])

    # Draw box
    BOP = ep.BoxPlotter(title="BoxPlot with start/end points", xlabel="Device",
                     ylabel="Degree of process")
    BOP.setFigureStyle(vertical=True, timeline=False, boxwidth=2)
    BOP.setTicks(label=L1)
    BOP.draw(D1, D2, D3, D4, D5)
    BOP.saveToPdf(output)

# box graph
elif style == "box-time":
    text = ep.tRead("dat/box-time.dat")

    # Parse text
    PP = ep.PatternParser(text);
    PP.PickKeyWith(": ")
    PP.ParseWith(",")

    # Set data
    D1 = ep.Group(PP, "CPU 0 S", "CPU 0 E", color="#225522", hatch="")
    D1.setLegend("CPU 0")
    D2 = ep.Group(PP, "CPU 1 S", "CPU 1 E", color="#BC434C", hatch="")
    D2.setLegend("CPU 1")
    D3 = ep.Group(PP, "CPU 2 S", "CPU 2 E", color="#FFBB00", hatch="")
    D3.setLegend("CPU 2")
    D4 = ep.Group(PP, "CPU 3 S", "CPU 3 E", color="#B82E92", hatch="")
    D4.setLegend("CPU 3")
    D5 = ep.Group(PP, "GPU S", "GPU E", color="#4455D2", hatch="")
    D5.setLegend("GPU")

    # Draw box
    BOP = ep.BoxPlotter(title="BoxPlot with start/end points", width=10, height=4,
                     xlabel="Time", ylabel="Running Device")

    BOP.setLegendStyle(ncol=5, size=12, frame=False, loc="upper center") 
    BOP.setFigureStyle(vertical=False, timeline=True, figmargin=0.8)
    BOP.draw(D1, D2, D3, D4, D5, boxwidth=2)
    BOP.saveToPdf(output)

elif style == "box-multi-time":

    # Parse text
    text = ep.tRead("dat/box-multi-time.dat")
    PP = ep.PatternParser(text);
    PP.PickKeyWith(": ")
    PP.ParseWith(",")

    # Set data
    D1 = ep.Group(PP, "Schedule 0 S", "Schedule 0 E", color=mc["red"], hatch="")
    D2 = ep.Group(PP, "Memory 0 S", "Memory 0 E", color=mc["yellow"], hatch="//")
    D3 = ep.Group(PP, "Compute 0 S", "Compute 0 E", color=mc["blue"], hatch="")
    G1 = ep.Group(D1, D2, D3)

    D1.setLegend("Schedule")
    D2.setLegend("Memory")
    D3.setLegend("Compute")

    # Set data
    D4 = ep.Group(PP, "Schedule 1 S", "Schedule 1 E", color=mc["red"], hatch="")
    D5 = ep.Group(PP, "Memory 1 S", "Memory 1 E", color=mc["yellow"], hatch="//")
    D6 = ep.Group(PP, "Compute 1 S", "Compute 1 E", color=mc["blue"], hatch="")
    G2 = ep.Group(D4, D5, D6)

    # Set data
    D7 = ep.Group(PP, "Schedule G S", "Schedule G E", color=mc["red"], hatch="")
    D8 = ep.Group(PP, "Memory G S", "Memory G E", color=mc["yellow"], hatch="//")
    D9 = ep.Group(PP, "Compute G S", "Compute G E", color=mc["blue"], hatch="")
    G3 = ep.Group(D7, D8, D9)

    L1 = ep.TickLabel(PP, ["CPU 0", "CPU 1", "GPU"])

    # Draw box
    CBOP = ep.CBoxPlotter(title="BoxPlot with start/end points", width=12, height=5,
                       xlabel="Time (ms)")

    CBOP.setLegendStyle(ncol=5, size=13, frame=False, loc="upper center")
    CBOP.setFigureStyle(vertical=False, timeline=True, figmargin=0.4)
    CBOP.setTicks(label=L1)
    CBOP.draw(G1, G2, G3, boxwidth=2)
    CBOP.saveToPdf(output)

elif style == "jaws":

    key = ["GPU comm0", "GPU comm1", "GPU memcp",
           "GPU exe", "CPU comm0", "CPU exe0",
           "CPU exe1", "CPU comm1", "GPU comm2"]
    # text = ep.tRead("dat/breakSM.dat")
    text = ep.tRead("dat/breakNoSM.dat")

    # Use custom parser mode
    PP = ep.PatternParser(text);
    PP.PickKeyWith(": ", clusterByRegion=key, subtfromfirst=True)

    # Set GPU data
    D1 = ep.Group(PP, "GPU comm0", color=mc["yellow"], hatch="//")
    D2 = ep.Group(PP, "GPU comm1", color=mc["yellow"], hatch="//")
    D3 = ep.Group(PP, "GPU comm2", color=mc["yellow"], hatch="//")
    G1 = ep.Group(D1, D2, D3)

    D4 = ep.Group(PP, "GPU memcp", color=mc["red"], hatch="")
    G2 = ep.Group(D4)

    D5 = ep.Group(PP, "GPU exe", color=mc["blue"], hatch="")
    G3 = ep.Group(D5)

    # Set CPU data
    D6 = ep.Group(PP, "CPU comm0", color=mc["yellow"], hatch="//")
    G4 = ep.Group(D6)

    D7 = ep.Group(PP, "CPU comm1", color=mc["yellow"], hatch="//")
    G5 = ep.Group(D7)

    D8 = ep.Group(PP, "CPU exe0", color=mc["blue"], hatch="")
    G6 = ep.Group(D8)

    D9 = ep.Group(PP, "CPU exe1", color=mc["blue"], hatch="")
    G7 = ep.Group(D9)

    tag = ["GPU comm", "GPU memcp", "GPU exe", "CPU comm0", "CPU comm1", "CPU exe0", "CPU exe1"]

    # Set legend and label to data
    ep.tSetLegend(tag, D1,D4,D5,D6,D7,D8,D9)
    L1 = ep.TickLabel(PP, tag)

    # Draw box
    CBOP = ep.CBoxPlotter(title="BoxPlot with start/end points", width=14, height=5,
                       xlabel="Time (ms)")

    CBOP.setLegendStyle(ncol=5, size=13, frame=False, loc="upper center")
    CBOP.setFigureStyle(vertical=False, figmargin=0.4)
    CBOP.setTicks(label=L1)
    CBOP.draw(G1, G2, G3, G4, G5, G6, G7, boxwidth=2)
    CBOP.saveToPdf(output)

elif style == "jaws-all":

    key = [ "GPU comm0","GPU comm1","GPU memcp","GPU exe","GPU comm2","GPU schdl"]
    # text = ep.tRead("dat/jaws/atax.share.log")
    # text = ep.tRead("dat/breakSM.dat")
    ## text = ep.tRead("dat/breakNoSM.dat")

    cpu_tag = []
    gpu_tag = ["GPU schdl", "GPU memcp", "GPU comm", "GPU exe"]
    key_comm = []
    key_exe = []
    for i in range(10):
        cpu_tag.append("CPU%d" % i)
        key_comm.append("CPU%d comm0" % i)
        key_comm.append("CPU%d comm1" % i)
        key_comm.append("CPU%d comm2" % i)
        key_exe.append("CPU%d exe" % i)
    key = key + key_comm + key_exe

    # Use custom parser mode
    PP = ep.PatternParser(text);
    PP.PickKeyWith(": ", clusterByRegion=key, subtfromfirst=True)

    # Set GPU data
    D4 = ep.Group(PP, "GPU memcp", color=mc["green"], hatch="")
    G1 = ep.Group(D4)

    D1 = ep.Group(PP, "GPU comm0", color=mc["red"], hatch="\\")
    D2 = ep.Group(PP, "GPU comm1", color=mc["yellow"], hatch="\\")
    D3 = ep.Group(PP, "GPU comm2", color=mc["yellow"], hatch="//")
    G2 = ep.Group(D1, D2, D3)

    D5 = ep.Group(PP, "GPU exe", color=mc["blue"], hatch="")
    G3 = ep.Group(D5)

    D6 = ep.Group(PP, "GPU schdl", color="#428bca", hatch="")
    G4 = ep.Group(D6)

    D = []
    G = []
    # Set CPU data
    for i in range(10):
        D7 = ep.Group(PP, "CPU%d comm0" % i, color=mc["red"], hatch="\\")
        D8 = ep.Group(PP, "CPU%d comm1" % i, color=mc["yellow"], hatch="\\")
        D9 = ep.Group(PP, "CPU%d comm2" % i, color=mc["yellow"], hatch="//")
        D10= ep.Group(PP, "CPU%d exe" % i, color=mc["blue"], hatch="")
        G.append(ep.Group(D7, D8, D9, D10))

    tag = gpu_tag + cpu_tag
    L1 = ep.TickLabel(PP, tag)

    argument = [G4, G1, G2, G3] + G

    D1.setLegend("comm0")
    D2.setLegend("comm1")
    D3.setLegend("comm2")
    D4.setLegend("memcpy")
    D5.setLegend("exe")
    D6.setLegend("schdl")

    # Draw box
    CBOP = ep.CBoxPlotter(title="BoxPlot with start/end points", width=12, height=7,
                     xlabel="Time (ms)")

    CBOP.setLegendStyle(ncol=6, size=13, frame=False, loc="upper center")
    CBOP.setFigureStyle(vertical=False, figmargin=0.1)
    CBOP.setTicks(label=L1)
    CBOP.draw(*argument, boxwidth=2)
    CBOP.saveToPdf(output)

elif style == "jaws-pie":
    key = [ "GPU comm0 start", "GPU comm0 end",
            "GPU comm1 start", "GPU comm1 end",
            "GPU memcp start", "GPU memcp end",
            "GPU exe start", "GPU exe end",
            "GPU comm2 start", "GPU comm2 end",
            "GPU schdl start", "GPU schdl end",
            "DONE"]

    text = ep.tRead("dat/jaws/atax.share.log")

    ## Use custom parser mode
    tag = ["memcp", "comm0", "comm1", "comm2", "schdl"]
    PP = ep.PatternParser(text, clusterBy=key, subtfromfirst=True);
    PP.sumWithRegionKey(tag, prefix="GPU ")
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

    PP = ep.PatternParser(" ")
    D1 = ep.Group(None, [1,2,3,4], color=mc["red"], hatch="")
    D2 = ep.Group(None, [2,4,5,3], color=mc["blue"], hatch="")
    D3 = ep.Group(None, [1,1,1,1], color=mc["yellow"], hatch="")

    D1.setLegend("A")
    D2.setLegend("B")
    D3.setLegend("C")

    L1 = ep.TickLabel(None, ["A", "B", "C", "D"])

    ## Draw box
    SBP = ep.SBarPlotter(title="Stacked Bar", xlabel="Strategy", ylabel="Value")

    # Set graph style
    SBP.setLegendStyle(ncol=3, size=10, frame=False, loc="upper center")
    SBP.setFigureStyle(figmargin=0.1)

    # Draw
    SBP.setTicks(label=L1)
    SBP.draw(D1, D2, D3, barwidth=1)
    SBP.saveToPdf(output)

elif style == "bar-stacked-trans":
    key = [ "GPU comm0 start", "GPU comm0 end",
            "GPU comm1 start", "GPU comm1 end",
            "GPU memcp start", "GPU memcp end",
            "GPU exe start", "GPU exe end",
            "GPU comm2 start", "GPU comm2 end",
            "GPU schdl start", "GPU schdl end",
            "DONE"]

    ## Read raw datas
    args.signature = "atax"
    text_sm = ep.tRead("dat/jaws/%s.share.log" % args.signature)
    text_nsm = ep.tRead("dat/jaws/%s.noshare.log" % args.signature)

    ## Tag lists that will parse
    tag = ["memcp", "comm0", "comm1", "comm2", "schdl"]
    leg = ["memcpy", "init", "task_begin", "task_end", "partition"]

    ## First parsing
    PP = ep.PatternParser(text_sm)
    PP.PickKeyWith(": ", clusterBy=key, subtfromfirst=True);
    PP.sumWithRegionKey(tag, prefix="GPU ")
    S_GPUresult = PP.getDataArr()

    ## Second parsing
    PN = ep.PatternParser(text_nsm);
    PN.PickKeyWith(": ", clusterBy=key, subtfromfirst=True);
    PN.sumWithRegionKey(tag, prefix="GPU ")
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

    L1 = ep.TickLabel(PP, ["with-Shared", "without-Shared"])

    ## Draw box
    SBP = ep.SBarPlotter(title=args.signature+" - GPU",
                      xlabel="Strategy", ylabel="Fraction")

    # Set graph style
    SBP.setStackStyle(colors=colors, hatch=hatch, legend=leg)
    SBP.setLegendStyle(ncol=5, size=10, frame=False, loc="upper center")
    SBP.setFigureStyle(figmargin=0.4, ylim=[0, 1.2])

    # Draw
    SBP.setTicks(label=L1)
    SBP.draw(S_GPUresult, NS_GPUresult, barwidth=1)
    SBP.saveToPdf(output)

elif style == "bar-clustacked":

    # benchmarks = ["atax", "syrk", "gemm"]
    benchmarks = ["syrk", "gemm"]

    ## Assign data directly
    S_CPUresult = []
    NS_CPUresult = []
    S_GPUresult = []
    NS_GPUresult = []

    # atax
    # S_CPUresult.append([3.877490234375, 15.810107421874996, 3.2838867187500007,
    #                     1.8818359375, 57.51716308593768])
    # NS_CPUresult.append([1200.7843017578125, 36.7966796875, 53.126953125,
    #                      4343.073974609375, 158.7681152343721])
    # S_GPUresult.append([202.099609375, 1.007080078125, 17.988037109375,
    #                     1.5107421875, 7.1806640625])
    # NS_GPUresult.append([197.38525390625, 1062.109130859375, 420.0341796875,
    #                      6318.2197265625, 746.284423828125])

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

    # Reproduce data (Normalization, ...)
    for i in range(len(benchmarks)):
        GPUOverhead = reduce(np.add, NS_GPUresult[i])
        CPUOverhead = reduce(np.add, NS_CPUresult[i])

        # Normalized to total sum of data(NS_CPUresult)
        S_GPUresult[i] = [ j/GPUOverhead for j in S_GPUresult[i] ]
        NS_GPUresult[i] = [ j/GPUOverhead for j in NS_GPUresult[i] ]
        S_CPUresult[i] = [ j/CPUOverhead for j in S_CPUresult[i] ]
        NS_CPUresult[i] = [ j/CPUOverhead for j in NS_CPUresult[i] ]

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


    ## Draw box
    SBP = ep.SBarPlotter(title="Normalized overhead to each device",
                      xlabel="", ylabel="Fraction")

    # Set manual ticks
    tlabel = ["S", "GPU", "N", "ATAX", "S", "CPU", "N"] + \
             ["S", "GPU", "N", "SYRK", "S", "CPU", "N"] + \
             ["S", "GPU", "N", "GEMM", "S", "CPU", "N"]

    L1 = ep.TickLabel(None, tlabel)

    xspace = [.5,1,1.5, 2.05, 2.6,3.1,3.6,
              5.6,6.1,6.6, 7.15, 7.7,8.2,8.7,
              10.7,11.2,11.7, 12.25, 12.8,13.3,13.8]
    vspace = [0,-.04,0, -.08, 0,-.04,0,
              0,-.04,0, -.08, 0,-.04,0,
              0,-.04,0, -.08, 0,-.04,0]

    SBP.setTicks(xspace=xspace, voffset=vspace, label=L1)

    # Set graph styles
    SBP.setLegendStyle(ncol=3, size=10, frame=False, loc="upper center")
    SBP.setFigureStyle(figmargin=0.05, bottomMargin=0.15, ylim=[0, 1.2])
    SBP.setStackStyle(colors=colors, hatch=hatch, legend=leg) # alert! transposed data

    # Draw graphs
    for i in range(len(benchmarks)):
        SBP.draw(S_GPUresult[i], NS_GPUresult[i], barwidth=1)
        SBP.setBaseOffset(1.1)
        SBP.draw(S_CPUresult[i], NS_CPUresult[i], barwidth=1)
        SBP.setBaseOffset(2)

    SBP.saveToPdf(output)


elif style == "cbp+lp":
    # Line data
    X1=[1,3,5,7,9]
    Y1=[1,1.5,2,2.5,3]
    D1 = ep.Group(None, X1, Y1, color=mc["red"], hatch="")

    # Bar data
    D2 = ep.Group(None, [0.4,0.9,1.7,1.9,2.7], color=mc["blue"], hatch="")
    D3 = ep.Group(None, [0.45,0.9,1.0,2.0,2.0], color=mc["yellow"], hatch="")

    LP = ep.LinePlotter(title="title", xlabel="", ylabel="")
    LP.draw(D1)

    BP = ep.CBarPlotter(axis=LP.getAxis())
    BP.draw(D2, D3)
    BP.finish()

    LP.saveToPdf(output)

elif style == "cbp+sbp+line":
    # SBar data
    A1=[1,3,7]
    A2=[1,1.5,2]
    D1 = ep.Group(None, A1, color=mc["purple"], hatch="")
    D2 = ep.Group(None, A2, color=mc["blue"], hatch="")

    # CBar data
    D3 = ep.Group(None, [0.4,0.9,1.7,1.9,2.7], color=mc["green"], hatch="")
    D4 = ep.Group(None, [0.45,0.9,1.0,2.0,2.0], color=mc["yellow"], hatch="")

    # plot SBP
    SBP = ep.SBarPlotter(title="title", xlabel="", ylabel="")
    SBP.draw(D1, D2)

    # plot CBP
    BP = ep.CBarPlotter(axis=SBP.getAxis())
    BP.setBaseOffset(4)
    BP.draw(D3, D4)
    BP.finish()

    # line data from bar's base
    xpoint = np.concatenate([SBP.getGlobalBase(), BP.getGlobalBase()]) + 0.5
    ypoint = np.array(range(len(xpoint))) + 9.5
    LD = ep.Group(None, xpoint, ypoint, color=mc["black"], hatch="")

    # plot Line
    LP = ep.LinePlotter(axis=SBP.getAxis())
    LP.draw(LD)

    # FIXME:: Currently, automatic tickers for multiplot isn't supported
    # Combination of ticker with bar plotting is needed, that merges bases
    label = ep.TickLabel(None, ["l1", "l2", "l3"] +
                               ["clus1", "clus2", "clus3", "clus4", "clus5"])
    # LP.setTicks(xspace=[0.5,1.5,2.5] + [4.5,7.3,10.1,12.9,15.7], label=label)
    LP.setTicks(xspace=xpoint, label=label)

    LP.saveToPdf(output)
