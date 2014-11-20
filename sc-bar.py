#!/usr/bin/python

import epic as ep

args = ep.parseCommandArgs() 

# color macro dictionary
mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292",
      "blue":"#4455D2", "white":"#FFFFFF", "ddwhite":"#B3B3B3", "dwhite":"#DFDFDF",
      "gray":"#AAAAAA", "dgray":"#3F3F3F", "black":"#000000"}

# output file name
output = "overhead.pdf"
if bool(args.outFile) == True:
    output = args.outFile

if bool(args.inFile) == True:
    text = ep.tRead(args.inFile)

if bool(args.style) == True:
    style = args.style


benchmarks = ["syrk", "gemm"]

S_GPUresult = []
NS_GPUresult = []
S_CPUresult = []
NS_CPUresult = []

# Reproduce data (Normalization, ...)
for i in range(len(benchmarks)):
    txt_share = ep.tRead("dat/jaws-merge/%s.share.log" % benchmarks[i])
    txt_noshare = ep.tRead("dat/jaws-merge/%s.noshare.log" % benchmarks[i])
    
    # Parse text
    PP1 = ep.PatternParser(txt_share)
    PP1.PickKeyWith(": ")
    PP1.ParseWith(",")
    PP2 = ep.PatternParser(txt_noshare)
    PP2.PickKeyWith(": ")
    PP2.ParseWith(",")

    S_CPUresult.append(ep.tTranspose(PP1.datList[:4])[0])
    S_GPUresult.append(ep.tTranspose(PP1.datList[4:])[0])
    NS_CPUresult.append(ep.tTranspose(PP2.datList[:4])[0])
    NS_GPUresult.append(ep.tTranspose(PP2.datList[4:])[0])


for i in range(len(benchmarks)):
    # Normalized to each device's exec
    SGPUOverhead = S_GPUresult[i].pop(2)
    GPUOverhead = NS_GPUresult[i].pop(2)
    SCPUOverhead = S_CPUresult[i].pop(2)
    CPUOverhead = NS_CPUresult[i].pop(2)

    S_GPUresult[i] = [ j/SGPUOverhead for j in S_GPUresult[i] ]
    NS_GPUresult[i] = [ j/GPUOverhead for j in NS_GPUresult[i] ]
    S_CPUresult[i] = [ j/SCPUOverhead for j in S_CPUresult[i] ]
    NS_CPUresult[i] = [ j/CPUOverhead for j in NS_CPUresult[i] ]

## Legend list
leg = ["dispatch", "memcpy", "merge"]

## Assign stack style
colors = [mc["dgray"], mc["white"], mc["gray"], mc["dwhite"], mc["dwhite"], mc["white"]]
hatch = ["", "\\\\\\\\", "", "", "", ""]

## Stacked Bar Plot =================================================================
SBP = ep.SBarPlotter(xlabel="", ylabel="Overhead normalized\n to useful work",
                     ylpos=[-.1, 0.5], width=8, height=4.2)

# Set manual ticks ==================================================================
SBP.annotate(["syrk", "gemm"], [[1.75, -.13], [6.21, -.13]], fontsize=17)
# SBP.annotate(["syrk", "gemm"], [[1.55, -8.24], [6.55, -8.24]], fontsize=18)
tlabel =   ["NoShm", "GPU", "Shm", "NoShm", "CPU", "Shm"] + \
           ["NoShm", "GPU", "Shm", "NoShm", "CPU", "Shm"]
L1 = ep.TickLabel(None, tlabel)

xspace = [.47,1,1.5, 2.57,3.1,3.6,
          5.1,5.6,6.1, 7.2,7.7,8.2]
vspace = [0,-.09,0, 0,-.09,0,
          0,-.09,0, 0,-.09,0]
SBP.setTicks(xspace=xspace, voffset=vspace, label=L1, fontsize=14)

# Set graph styles ==================================================================
SBP.setLegendStyle(ncol=6, size=15, pos=[0.81, 1.15], frame=False, tight=True)
SBP.setFigureStyle(bottomMargin=0.23, figmargin=0.03, fontsize=15, gridy=True)

# if "setStackStyle" method is used, transposed data will be used
# otherwise, group will map the styles to each stack
SBP.setStackStyle(colors=colors, hatch=hatch, legend=leg)

# Draw graphs =======================================================================
for i in range(len(benchmarks)):
    SBP.draw(NS_GPUresult[i], S_GPUresult[i], barwidth=1)
    SBP.setBaseOffset(1.1)
    SBP.draw(NS_CPUresult[i], S_CPUresult[i], barwidth=1)
    SBP.setBaseOffset(1.5)

SBP.saveToPdf(output)
