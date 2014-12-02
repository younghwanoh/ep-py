#!/usr/bin/python

import epic as ep

mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292",
      "blue":"#4455D2", "white":"#FFFFFF", "ddwhite":"#B3B3B3", "dwhite":"#DFDFDF",
      "gray":"#AAAAAA", "dgray":"#3F3F3F", "black":"#111111"}

# Parse arguments
args = ep.parseCommandArgs() 
if bool(args.outFile) == True:
    output = args.outFile

if bool(args.inFile) == True:
    text = ep.tRead(args.inFile)

polybench = "/home/papl-note/svnroot/projects/parallelJS/trunk/qpr.js/webkit/opt/polybench_js"
benchmark = "gemm"
# Parse data for governor ==========================================
# Set performance
text = ep.tRead("%s/%s/performance.data" % (polybench, benchmark))
PP = ep.PatternParser(text)
PP.PickKeyWith("row")
PP.ParseWith("\t")
power_perf = PP.getDataArr("power")
thput_perf = PP.getDataArr("thput")

# Set ondemand
text = ep.tRead("%s/%s/ondemand.data" % (polybench, benchmark))
PP = ep.PatternParser(text)
PP.PickKeyWith("row")
PP.ParseWith("\t")
power_ond = PP.getDataArr("power")
thput_ond = PP.getDataArr("thput")

# Set powersave
text = ep.tRead("%s/%s/powersave.data" % (polybench, benchmark))
PP = ep.PatternParser(text)
PP.PickKeyWith("row")
PP.ParseWith("\t")
power_save = PP.getDataArr("power")
thput_save = PP.getDataArr("thput")

# Parse optimizer and set data =====================================
text = ep.tRead("%s/%s/optimizer.data" % (polybench, benchmark))
PP = ep.PatternParser(text)
PP.PickKeyWith("row")
PP.ParseWith("\t", forceType=float)

# Post processing of data
core_data = PP.getDataArr("core")
core_alias = {"0-3":4, "0-2":3, "0-1":2, 0.0:1}
for idx, val in enumerate(core_data):
    core_data[idx] = core_alias[val]

freq_data = PP.getDataArr("freq")
for idx, val in enumerate(freq_data):
    freq_data[idx] = float(val.split(",")[0])/1000000

# Assign data to style
xpoints = range(len(PP.getDataArr(0)))

thput_qpr   = ep.Group(PP,   xpoints, "thput",    color="#000000", marker="s")
thput_perf  = ep.Group(None, xpoints, thput_perf, color="#bbbbbb", marker="x")
thput_ond   = ep.Group(None, xpoints, thput_ond,  color="#a0a0a0", marker="v")
thput_save  = ep.Group(None, xpoints, thput_save, color="#5e5e5e", marker="o")

freq = ep.Group(PP, xpoints, "freq", color="#000000", marker="s")
core = ep.Group(PP, xpoints, "core", color="#a0a0a0", marker="o")

power_qpr  = ep.Group(PP,   xpoints, "power",    color="#000000", marker="s")
power_ond  = ep.Group(None, xpoints, power_ond,  color="#a0a0a0", marker="o")

# void data to assign legend
core_void   = ep.Group(None, [], [], color="#a0a0a0", marker="o")

# Assign legend to data
freq.setLegend("Frequency")
core_void.setLegend("# of active cores")

power_qpr.setLegend("QPR.js")
power_ond.setLegend("Ondemand")

thput_qpr.setLegend("QPR.js")
thput_perf.setLegend("Performance")
thput_ond.setLegend("Ondemand")
thput_save.setLegend("Powersave")

# Custom figure styles over benchmarks
ylim_freq  = [0,3]
ylim_core  = [0,4.99]
if benchmark   == "gesummv":
    ylim_thput = [0.2,1.5]
    ylim_power = [0,25]
elif benchmark == "gemm":
    ylim_thput = [0.2,2.5]
    ylim_power = [0,50]
elif benchmark == "syrk":
    ylim_thput = [0.2,2.5]
    ylim_power = [0,50]
elif benchmark == "syr2k":
    ylim_thput = [0,0.9]
    ylim_power = [0,50]

# Subplotter for multiple plot
SP = ep.SubPlotter(3, sharex=True, height=9.0)
SP.adjust(hspace=0.38)

# Draw thput
LP0 = ep.LinePlotter(axis=SP.getAxis(0), ylabel=["Throughput (1/s)", "bold", 14])
LP0.setLegendStyle(ncol=4, frame=False, pos=[1.03, 1.23], tight=True)
LP0.setFigureStyle(ylim=ylim_thput, ylpos=[-0.07, 0.5], grid=True)
LP0.annotate(["(i)"], [[24.15,-0.13]], fontsize=14)
LP0.draw(thput_qpr, thput_perf, thput_ond, thput_save)
LP0.finish()

# Share an axis of subplot
cf_axis = SP.getAxis(1)

# Draw freq
LP1_freq = ep.LinePlotter(axis=cf_axis, ylabel=["Frequency (GHz)", "bold", 14], flushLegend=True)
LP1_freq.setLegendStyle(ncol=2, frame=False, pos=[0.88, 1.23])
LP1_freq.setFigureStyle(ylim=ylim_freq, ylpos=[-0.07, 0.5], grid=True)
LP1_freq.annotate(["(ii)"], [[24.15,-0.13]], fontsize=14)
LP1_freq.draw(freq, core_void)
LP1_freq.finish()

# Draw core
LP1_core = ep.LinePlotter(axis=cf_axis.twinx(), ylabel=["# of active cores", "bold", 14], flushLegend=True)
LP1_core.setFigureStyle(ylim=ylim_core, ylpos=[1.06, 0.5])
LP1_core.draw(core)
LP1_core.finish()

# Draw power
LP2 = ep.LinePlotter(axis=SP.getAxis(2), ylabel=["Power (Watt)", "bold", 14], xlabel=["Iteration", "bold", 14], flushLegend=True)
LP2.setLegendStyle(ncol=2, frame=False, pos=[0.82, 1.23])
LP2.setFigureStyle(ylim=ylim_power, ylpos=[-0.07, 0.5], grid=True)

LP2.annotate(["(iii)"], [[23.94,-0.36]], fontsize=14)
LP2.setTicks(label=ep.TickLabel(None, range(0,51,5)), xspace=range(0,51,5))
LP2.hline(y=8, xrange=[0, 50], color="#434343", linestyle="--")
LP2.draw(power_qpr, power_ond)
LP2.finish()

# Save to pdf files
SP.saveToPdf(args.outFile)
