#!/usr/bin/python

import epic as ep

output = "output.pdf"
text = ep.tRead("../dat/box-time.dat")

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
BOP.setFigureStyle(vertical=False, timeline=False, figmargin=0.8)
BOP.draw(D1, D2, D3, D4, D5, boxwidth=2)
BOP.saveToPdf(output)
