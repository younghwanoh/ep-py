#!/usr/bin/python

import epic as ep
mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292",
      "blue":"#4455D2", "white":"#FFFFFF", "ddwhite":"#B3B3B3", "dwhite":"#DFDFDF",
      "gray":"#AAAAAA", "dgray":"#3F3F3F", "black":"#111111"}

# Parse data
# text = ep.tRead("../dat/subplot-line/total.data")
text = ep.tRead("../dat/subplot-line/syrk.data")
PP = ep.PatternParser(text)
PP.PickKeyWith("row")
PP.ParseWith("\t", forceType=float)

# Post processing of data
core_data = PP.getDataArr(3)
core_alias = {"0-3":4, "0-2":3, "0-1":2, 0.0:1}
for idx, val in enumerate(core_data):
    core_data[idx] = core_alias[val]

freq_data = PP.getDataArr(4)
for idx, val in enumerate(freq_data):
    freq_data[idx] = float(val.split(",")[0])/1000000

# Assign data to style
xTickSpace = range(len(PP.getDataArr(0)))
core = ep.Group(PP, xTickSpace, "core", color=mc["green"], marker="x")
freq = ep.Group(PP, xTickSpace, "freq", color=mc["red"], marker="o")
qpr_power = ep.Group(PP, xTickSpace, "power", color=mc["yellow"], marker="s")
qpr_thput = ep.Group(PP, xTickSpace, "thput", color=mc["blue"], marker="x")

# FIXME: legend partially appears now
# Assign legend to data
# core.setLegend("# of active cores")
# freq.setLegend("Frequency")
# qpr_power.setLegend("QPR.js")
# qpr_thput.setLegend("QPR.js")

# Subplotter for multiple plot
SP = ep.SubPlotter(3, title="subplots")

# Draw thput
LP0 = ep.LinePlotter(axis=SP.getAxis(0), ylabel="Throughput (1/s)")
LP0.setFigureStyle(ylim=[0.2,1.8], ylpos=[-0.07, 0.5])
LP0.draw(qpr_thput)
LP0.finish()

# Share subplots
cf_axis = SP.getAxis(1)

# Draw core
LP1_core = ep.LinePlotter(axis=cf_axis, ylabel="# of actice cores")
LP1_core.setTicks(yspace=[1,2,3,4])
LP1_core.setFigureStyle(ylim=[0,6.3], ylpos=[-0.07, 0.5])
LP1_core.draw(core)
LP1_core.finish()

# Draw freq
LP1_freq = ep.LinePlotter(axis=cf_axis.twinx(), ylabel="Frequency (Ghz)")
LP1_freq.setTicks(yspace=[1, 1.4, 1.8, 2.2, 2.6, 3])
LP1_freq.setFigureStyle(ylim=[1,3.5], ylpos=[1.08, 0.5])
LP1_freq.draw(freq)
LP1_freq.finish()

# Draw power
LP2 = ep.LinePlotter(axis=SP.getAxis(2), ylabel="Power (Watt)")
LP2.setFigureStyle(ylim=[0,28], ylpos=[-0.07, 0.5])
LP2.hline(y=8, xrange=[0, 50], color="#434343", linestyle="--")
LP2.draw(qpr_power)
LP2.finish()

# Save to pdf files
SP.saveToPdf("subplot-line.pdf")
