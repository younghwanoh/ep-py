#!/usr/bin/python

# import sys
# sys.dont_write_bytecode = True;

# library for ep.py
import epic as ep

args = ep.parseCommandArgs() 

# color macro dictionary
mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292",
      "blue":"#4455D2",
      "white":"#FFFFFF", "dwhite":"#DFDFDF", "ddwhite":"#B3B3B3",
      "gray":"#888888", "wgray":"#CECECE", "dgray":"#909090", "ddgray":"#5F5F5F",
      "black":"#000000"}

# output file name
output = "cbar-line.pdf"
if bool(args.outFile) == True:
    output = args.outFile

if bool(args.inFile) == True:
    text = ep.tRead(args.inFile)

if bool(args.style) == True:
    style = args.style


# Start ===============================================================================

# Comparison clustered bar
# Polybench
PP = ep.PatternParser(ep.tRead("dat/jaws-comp/poly.dat"))
PP.PickKeyWith("row")
PP.ParseWith("\t")
PP.datNormTo("cpu-only", "gpu-only", select="min")

PD = []
PD.append(ep.Group(PP, "SO", color=mc["white"], hatch=""))
PD.append(ep.Group(PP, "Boyer", color=mc["ddwhite"], hatch=""))
PD.append(ep.Group(PP, "jAWS", color=mc["black"], hatch=""))

PD[0].setLegend("FluidiCL")
PD[1].setLegend("Boyer et al.")
PD[2].setLegend("jAWS")

# WebCL
PP = ep.PatternParser(ep.tRead("dat/jaws-comp/webcl.dat"))
PP.PickKeyWith("row")
PP.ParseWith("\t")
PP.datNormTo("cpu-only", "gpu-only", select="min")

WD = []
WD.append(ep.Group(PP, "SO", color=mc["white"], hatch=""))
WD.append(ep.Group(PP, "Boyer", color=mc["ddwhite"], hatch=""))
WD.append(ep.Group(PP, "jAWS", color=mc["black"], hatch=""))

# Geomean
PP = ep.PatternParser(ep.tRead("dat/jaws-comp/geomean-best.dat"))
PP.PickKeyWith("row")
PP.ParseWith("\t")

GD = []
GD.append(ep.Group(PP, "SO", color=mc["white"], hatch=""))
GD.append(ep.Group(PP, "Boyer", color=mc["ddwhite"], hatch=""))
GD.append(ep.Group(PP, "jAWS", color=mc["black"], hatch=""))

# label lists
poly_list = ["ATAX", "BICG", "SYRK", "SYR2K", "GEMM", "2MM", "CORR"]
poly_list_l = [ elem.lower() for elem in poly_list ]
webcl_list = ["Mandelbrot", "Nbody", "Sobel-CorG", "Random"]
geo_list = ["geomean"]

L1 = ep.TickLabel(None, poly_list_l + webcl_list + geo_list)
CB = ep.CBarPlotter(ylabel="Speedup over Best Device", ylpos=[-.035, 0.5], width=30, height=6.8)
CB.setTicks(yspace=[0, 0.5, 1, 1.5], label=L1)
CB.annotate(["Polybench", "WebKit-WebCL"], [[27.5, -.30], [85, -.30]], fontsize=30)

# Figure style
CB.setLegendStyle(ncol=3, size=28, pos=[0.59, 1.18], frame=False)
CB.setFigureStyle(ylim=[0, 1.5], bottomMargin=0.18, fontsize=25,
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
PP = ep.PatternParser(ep.tRead("dat/jaws-lbf/poly.dat"))
PP.PickKeyWith("col")
PP.ParseWith("\t")

PLB = []
for i, val in enumerate(poly_list):
    PLB.append(ep.Group(PP, [g_base[i], g_base[i]+2, g_base[i]+4], val,
                            color=color, face=face, marker=marker))
PLB[0].setLegend("Load Balance Factor")

# WebCL
PP = ep.PatternParser(ep.tRead("dat/jaws-lbf/webcl.dat"))
PP.PickKeyWith("col")
PP.ParseWith("\t")

WLB = []
for i, val in enumerate(webcl_list):
    WLB.append(ep.Group(PP, [g_base[i], g_base[i]+2, g_base[i]+4], val,
                            color=color, face=face, marker=marker))

# Geomean
PP = ep.PatternParser(ep.tRead("dat/jaws-lbf/geomean.dat"))
PP.PickKeyWith("col")
PP.ParseWith("\t")

GLB = []
for i, val in enumerate(geo_list):
    GLB.append(ep.Group(PP, [g_base[i], g_base[i]+2, g_base[i]+4], val,
                            color=color, face=face, marker=marker))

# get duplicated axis from previous plotter
twinx = CB.getAxis()

LP = ep.LinePlotter(axis=twinx, ylabel="Load Balance Factor", ylpos=[1.04, 0.5])
LP.setLegendStyle(frame=False, pos=[0.83, 1.18], size=28)
LP.setFigureStyle(markersize=15)
LP.setTicks(yspace=[0, 0.5, 1.0, 1.5])
LP.setBaseOffset(1)
LP.draw(*PLB)
LP.setBaseOffset(75.2)
LP.draw(*WLB)
LP.setBaseOffset(44.6)
LP.draw(*GLB)

LP.m_finish()

CB.saveToPdf(output)
