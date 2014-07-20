#!/usr/bin/python

import sys
import re

sys.dont_write_bytecode = True;

# library for ep.py
from parser import PatternParser
from tools import Group
from tools import transpose
from tools import popRow
from tools import popCol
from tools import read
from plotter import LinePlotter

# argument parser
import argparse
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--inFile", help='Specify the name of input data file')
argparser.add_argument("-o","--outFile", help='Specify the name of output PDF file')
argparser.add_argument("-s","--style", help='Specify the style of graphs')
args = argparser.parse_args()

# output file name
output = "output.pdf"
if bool(args.outFile) == True:
    output = arg.outFile

if bool(args.outFile) == True:
    text = read(args.inFile)
style = args.style

# line.dat
if style == "line1":
    text = read("line.dat")

    PP = PatternParser(text)
    PP.PickKeyWith(": ")
    PP.ParseWith(",")

    GPUdata = Group(PP, "GPUprofileQuantum", "GPUthput", color="red", marker="o")
    CPUdata = Group(PP, "CPUprofileQuantum", "CPUthput", color="blue", marker="x")

    GPUdata.setLegend("GPU") 
    CPUdata.setLegend("CPU") 

    LP = LinePlotter(width=5, height=5, title="LinePlot", xlabel="abc", ylabel="ee")
    # LP.setLimitOn(x=[0, 1000], y=[0, 1000])
    LP.draw(GPUdata, CPUdata)
    LP.saveToPdf(output);
    # LP.drawToWindow();

# bar.dat
elif style == "line2":
    text = read("bar.dat")

    PP = PatternParser(text)
    PP.ParseWith("\t")
    PP.PickKeyWith("row")

    D1 = Group(PP, [1,2,3,4], "seq",      color="red", marker="o")
    D2 = Group(PP, [1,2,3,4], "cpu-only", color="blue", marker="x")
    D3 = Group(PP, [1,2,3,4], "gpu-only", color="green", marker="o")
    D4 = Group(PP, [1,2,3,4], "cpu+gpu",  color="black", marker="x")

    # D1.setLegend("SEQ") 
    # D2.setLegend("CPU-only") 
    # D3.setLegend("GPU-only") 
    # D4.setLegend("CPU+GPU") 

    LP = LinePlotter(title="LinePlot", xlabel="abc", ylabel="ee")
    LP.setLimitOn(x=[0, 10], y=[0, 10])
    LP.draw(D1,D2,D3,D4)
    LP.saveToPdf(output)

# bar.dat
elif style == "line3":
    text = read("line-norm.dat")
# Profile: 10.206269454210997	24.674265095964074	56.017232621088624	66.50465840473771184.878224115818739	109.81756330467761	140.67703363485634	185.6153317168355	234.73950250074267	295.95925606787205	360.76470395550132	474.06574549153447	558.78607768565416
# dataProfile: 100	150	200	250	300	350	400	450	500	550	600650	700
# CGCEavg: 15.514176804572344	31.64221397601068	64.45726719684899	76.14890020340681	97.77346760965884	119.37319422140718	151.81329138576984	202.42599304765463	246.63688261061907	312.7707237843424	384.6715443301946	503.694925038144	572.2015670035034
# data: 100	150	200	250	300	350	400	450	500	550	600	650700
# SEQiavg: 7.852057414129376	23.690991196781397	53.85806364938617	102.43250601924956172.85463805310428	274.72653980366886	405.56159876286983	574.4705496821553	789.2924030311406	1047.049553412944	1360.3401023894548	1726.5890171285719	2161.971054272726
# SEQavg: 8.41104295104742	26.232343586161733	55.3335799369961	104.89575900137424175.60677086003125	279.34828200377524	411.6636684164405	583.2676463760436	795.5854004714638	1058.6189130786806	1367.4993370193988	1736.6199331823736	2165.341287245974
# GPUiavg: 44.9412758462131	50.675274431705475	52.81108464114368	65.21827224642038	83.00119396299124	111.15627507679164	137.3779967892915	186.36428103782237	233.64471779204905	295.92988905496895	362.5715909875	471.5048497542739	553.1684163957834

    PP = PatternParser(text)
    PP.PickKeyWith(": ")
    PP.ParseWith("\t")
    PP.datNormTo("SEQavg", opt="speedup", skip="data") # option: speedup, exetime

    D1 = Group(PP, "data", "Profile", color="red", marker="o")
    D2 = Group(PP, "data", "CGCEavg", color="blue", marker="x")
    D3 = Group(PP, "data", "SEQiavg", color="green", marker="o")
    D4 = Group(PP, "data", "GPUiavg", color="black", marker="x")

    # D1.setLegend("SEQ") 
    # D2.setLegend("CPU-only") 
    # D3.setLegend("GPU-only") 
    # D4.setLegend("CPU+GPU") 

    LP = LinePlotter(title="LinePlot", xlabel="abc", ylabel="ee")
    LP.draw(D1,D2,D3,D4)
    LP.saveToPdf(output)

elif style == "3":
    text = "# monitoring\n\
39	29.63501	0-3	2401000\n\
42	31.03067	0-3	2401000\n\
41	31.573883000000002	0-3	2401000\n\
40	30.402679499999998	0-3	2401000\n"
    PP = PatternParser(text);
    PP.ParseWith("\t")
    print(PP.datList)

elif style == "4":
    text = "CPU 0 S: 2.01513671875,796.010986328125,1473.43603515625\n\
CPU 0 E: 795.9951171875,1473.39404296875,2616.083984375\n\
CPU 1 S: 2.02294921875,347.43896484375,685.344970703125,1339.2451171875\n\
CPU 1 E: 347.3779296875,685.326171875,1339.220947265625,2431.3759765625\n\
CPU 2 S: 2.027099609375,348.198974609375,686.010986328125,1361.590087890625\n\
CPU 2 E: 348.18505859375,685.983154296875,1361.51806640625,2549.39111328125\n\
CPU 3 S: 2.031005859375,753.9150390625,1953.3720703125\n\
CPU 3 E: 753.902099609375,1953.31005859375,2056.718017578125\n\
GPU S: 1.994140625,800.839111328125\n\
GPU E: 800.779052734375,2235.4169921875\n"

    PP = PatternParser(text);
    PP.PickKeyWith(": ")
    PP.ParseWith(",")
    print(PP.keyList)
    print("---------------------------------------------")
    print(PP.datList)
