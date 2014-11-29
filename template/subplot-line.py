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
xpoints = range(len(PP.getDataArr(0)))
core = ep.Group(PP, xpoints, "core", color="#a0a0a0", marker="o")
freq = ep.Group(PP, xpoints, "freq", color=mc["black"], marker="s")
qpr_power = ep.Group(PP, xpoints, "power", color=mc["black"], marker="s")
qpr_thput = ep.Group(PP, xpoints, "thput", color=mc["black"], marker="s")

# FIXME: legend partially appears now
# Assign legend to data
# core.setLegend("# of active cores")
# freq.setLegend("Frequency")
# qpr_power.setLegend("QPR.js")
# qpr_thput.setLegend("QPR.js")

# Subplotter for multiple plot
SP = ep.SubPlotter(3, sharex=True, height=9.0)
SP.adjust(hspace=0.38)

# Draw thput
LP0 = ep.LinePlotter(axis=SP.getAxis(0), ylabel=["Throughput (1/s)", "bold", 14])
LP0.setFigureStyle(ylim=[0.2,1.8], ylpos=[-0.07, 0.5], grid=True)
LP0.annotate(["(i)"], [[24.15,-0.13]], fontsize=14)
LP0.draw(qpr_thput)
LP0.finish()

# Share subplots
cf_axis = SP.getAxis(1)

# Draw freq
LP1_freq = ep.LinePlotter(axis=cf_axis, ylabel=["Frequency (GHz)", "bold", 14])
LP1_freq.setFigureStyle(ylim=[0,3], ylpos=[-0.07, 0.5], grid=True)
LP1_freq.annotate(["(ii)"], [[24.15,-0.13]], fontsize=14)
LP1_freq.draw(freq)
LP1_freq.finish()

# Draw core
LP1_core = ep.LinePlotter(axis=cf_axis.twinx(), ylabel=["# of active cores", "bold", 14])
LP1_core.setFigureStyle(ylim=[0,4.99], ylpos=[1.06, 0.5])
LP1_core.draw(core)
LP1_core.finish()

# Draw power
LP2 = ep.LinePlotter(axis=SP.getAxis(2), ylabel=["Power (Watt)", "bold", 14], xlabel=["Iteration", "bold", 14])
LP2.setFigureStyle(ylim=[0,30], ylpos=[-0.07, 0.5], grid=True)

LP2.annotate(["(iii)"], [[23.94,-0.36]], fontsize=14)
LP2.setTicks(label=ep.TickLabel(None, range(0,51,5)), xspace=range(0,51,5))
LP2.hline(y=8, xrange=[0, 50], color="#434343", linestyle="--")
LP2.draw(qpr_power)
LP2.finish()

# Save to pdf files
SP.saveToPdf("subplot-line.pdf")
