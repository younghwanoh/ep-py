#!/usr/bin/python

import epic as ep

# color macro dictionary
mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292",
      "blue":"#4455D2", "white":"#FFFFFF", "ddwhite":"#B3B3B3", "dwhite":"#DFDFDF",
      "gray":"#888888", "dgray":"#4F4F4F", "black":"#000000"}


output = "output.pdf"
key = ["GPU comm0", "GPU comm1", "GPU memcp",
   "GPU exe", "CPU comm0", "CPU exe0",
   "CPU exe1", "CPU comm1", "GPU comm2"]
# text = ep.tRead("dat/breakSM.dat")
text = ep.tRead("../dat/breakNoSM.dat")

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
