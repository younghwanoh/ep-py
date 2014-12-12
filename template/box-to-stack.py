#!/usr/bin/python

import epic as ep
import numpy as np

# color macro dictionary
mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292",
      "blue":"#4455D2", "white":"#FFFFFF", "ddwhite":"#B3B3B3", "dwhite":"#DFDFDF",
      "gray":"#888888", "dgray":"#4F4F4F", "black":"#000000"}


output = "output.pdf"

key = [ "GPU comm0 start", "GPU comm0 end",
    "GPU comm1 start", "GPU comm1 end",
    "GPU memcp start", "GPU memcp end",
    "GPU exe start", "GPU exe end",
    "GPU comm2 start", "GPU comm2 end",
    "GPU schdl start", "GPU schdl end",
    "DONE"]

## Read raw datas
text_sm = ep.tRead("../dat/jaws/atax.share.log")
text_nsm = ep.tRead("../dat/jaws/atax.noshare.log")

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
# NS_GPUresult[2] -= NS_GPUresult[0]
# S_GPUresult[2] -= S_GPUresult[0]
# totOverhead = reduce(np.add, NS_GPUresult)

# Normalized to total sum of data2(NS_GPUresult)
# S_GPUresult = [ i/totOverhead for i in S_GPUresult ]
# NS_GPUresult = [ i/totOverhead for i in NS_GPUresult ]

# Set style
colors = [mc["black"], mc["dgray"], mc["gray"], mc["white"], mc["white"]]
hatch = ["", "", "", "\\\\", ""]

L1 = ep.TickLabel(PP, ["with-Shared", "without-Shared"])

## Draw box
SBP = ep.SBarPlotter(title="atax - GPU",
              xlabel="Strategy", ylabel="Fraction")

# Set graph style
SBP.setStackStyle(colors=colors, hatch=hatch, legend=leg)
SBP.setLegendStyle(ncol=5, size=10, frame=False, loc="upper center")
SBP.setFigureStyle(figmargin=0.4)

# Draw
SBP.setTicks(label=L1)
SBP.draw(S_GPUresult, NS_GPUresult, barwidth=1)
SBP.saveToPdf(output)
