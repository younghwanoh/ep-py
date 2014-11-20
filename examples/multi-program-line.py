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
      "gray":"#888888", "wgray":"#CECECE", "dgray":"#808080", "ddgray":"#5F5F5F",
      "black":"#000000"}

# output file name
output = "multi.pdf"
if bool(args.outFile) == True:
    output = args.outFile

if bool(args.inFile) == True:
    text = ep.tRead(args.inFile)

if bool(args.style) == True:
    style = args.style


# Clustered bar graph =======================================================================
# ===========================================================================================

# Parse ======================================================================

# Polybench
PP = ep.PatternParser(ep.tRead("../dat/cbar-line/multi-program.dat"))
PP.PickKeyWith("row")
PP.ParseWith("\t")
# PP.datNormTo("col1", "col2", select="min")

PD = []
PD.append(ep.Group(PP, "col1", color=mc["white"], hatch=""))
PD.append(ep.Group(PP, "col2", color=mc["white"], hatch="\\\\"))
PD.append(ep.Group(PP, "col3", color=mc["ddwhite"], hatch=""))
PD.append(ep.Group(PP, "col4", color=mc["dgray"], hatch=""))
PD.append(ep.Group(PP, "col5", color=mc["black"], hatch=""))

PD[0].setLegend("off")
PD[1].setLegend("bank")
PD[2].setLegend("sram")
PD[3].setLegend("tlb")
PD[4].setLegend("\"ideal\"")

#  # WebCL
#  PP = ep.PatternParser(ep.tRead("../dat/cbar-line/webcl.dat"))
#  PP.PickKeyWith("row")
#  PP.ParseWith("\t")
#  PP.datNormTo("col1", "col2", select="min")
#  
#  WD = []
#  WD.append(ep.Group(PP, "col1", color=mc["white"], hatch=""))
#  WD.append(ep.Group(PP, "col2", color=mc["ddwhite"], hatch=""))
#  WD.append(ep.Group(PP, "col3", color=mc["black"], hatch=""))
#  
#  # Geomean
#  PP = ep.PatternParser(ep.tRead("../dat/cbar-line/geomean-best.dat"))
#  PP.PickKeyWith("row")
#  PP.ParseWith("\t")
#  
#  GD = []
#  GD.append(ep.Group(PP, "col1", color=mc["white"], hatch=""))
#  GD.append(ep.Group(PP, "col2", color=mc["ddwhite"], hatch=""))
#  GD.append(ep.Group(PP, "col3", color=mc["black"], hatch=""))

# label lists
poly_list = ["HM1", "HM2", "HM3", "HM4", "HM5", "HM6", "HM7", "HM8"]
#webcl_list = ["Mandelbrot", "Nbody", "Sobel-CorG", "Random"]
#geo_list = ["geomean"]


# Draw ======================================================================

CB = ep.CBarPlotter(ylabel="Speedup over Best Device", ylpos=[-.035, 0.5],
                    width=30, height=6.8)

# Set Ticks
#L1 = ep.TickLabel(None, poly_list + webcl_list + geo_list)
L1 = ep.TickLabel(None, poly_list)
CB.setTicks(yspace=[0, 0.5, 1, 1.9], label=L1)
CB.annotate(["Polybench", "WebKit-WebCL"], [[27.5, -.30], [85, -.30]], fontsize=30)

# Figure style
CB.setLegendStyle(ncol=5, size=28, pos=[0.59, 1.18], frame=False)
CB.setLegendStyle(ncol=5, size=28, pos=[0.65, 1.18], frame=False)
CB.setFigureStyle(ylim=[0, 1.5], bottomMargin=0.18, fontsize=25,
                  interCmargin=.7, figmargin=0.02)

CB.draw(*PD, barwidth=2)
CB.setBaseOffset(14)
#CB.draw(*WD, barwidth=2)
#CB.setBaseOffset(14)
#CB.draw(*GD, barwidth=2)

g_base = CB.getGlobalBase()

# Line Graph ================================================================================
# ===========================================================================================
color = mc["ddgray"]
face = mc["black"]
marker = "o"

# Parse ======================================================================
# Polybench
PP = ep.PatternParser(ep.tRead("../dat/cbar-line/multi-program-line.dat"))
PP.PickKeyWith("col")
PP.ParseWith("\t")

PLB = []
for i, val in enumerate(poly_list):
    print [g_base[i], g_base[i]+2, g_base[i]+4, g_base[i]+6, g_base[i]+8]
    PLB.append(ep.Group(PP, [g_base[i], g_base[i]+2, g_base[i]+4, g_base[i]+6, g_base[i]+8], val, 
                            color=color, face=face, marker=marker))
PLB[0].setLegend("Load Balance Factor")

# # WebCL
# PP = ep.PatternParser(ep.tRead("../dat/cbar-line/webcl-line.dat"))
# PP.PickKeyWith("col")
# PP.ParseWith("\t")
# 
# WLB = []
# for i, val in enumerate(webcl_list):
#     WLB.append(ep.Group(PP, [g_base[i], g_base[i]+2, g_base[i]+4], val,
#                             color=color, face=face, marker=marker))
# 
# # Geomean
# PP = ep.PatternParser(ep.tRead("../dat/cbar-line/geomean-line.dat"))
# PP.PickKeyWith("col")
# PP.ParseWith("\t")
# 
# GLB = []
# for i, val in enumerate(geo_list):
#     GLB.append(ep.Group(PP, [g_base[i], g_base[i]+2, g_base[i]+4], val,
#                             color=color, face=face, marker=marker))
# 
# Draw ======================================================================

# get duplicated axis from previous plotter
twinx = CB.getAxis(twinx=True)

LP = ep.LinePlotter(axis=twinx, ylabel="Load Balance Factor", ylpos=[1.04, 0.5])

# set styles
LP.setTicks(yspace=[0, 0.5, 1.0, 1.5])
LP.setLegendStyle(frame=False, pos=[0.89, 1.18], size=28)
LP.setFigureStyle(markersize=15)

LP.setBaseOffset(1)
LP.draw(*PLB)
LP.finish()

CB.saveToPdf(output)
