#!/usr/bin/python
import epic as ep

output = "output.pdf"

# color macro dictionary
mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292",
      "blue":"#4455D2", "white":"#FFFFFF", "ddwhite":"#B3B3B3", "dwhite":"#DFDFDF",
      "gray":"#888888", "dgray":"#4F4F4F", "black":"#000000"}

# Parse text
text = ep.tRead("../dat/box-multi-time.dat")
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
CBOP.setFigureStyle(vertical=False, figmargin=0.4)
CBOP.setTicks(label=L1)
CBOP.draw(G1, G2, G3, boxwidth=2)
CBOP.saveToPdf(output)
