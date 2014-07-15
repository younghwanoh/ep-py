#!/usr/bin/python

import sys
import re

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Front-end parser
class PatternParser:
    """Parse EP format data with some exclusive patterns"""
    def __init__(self, raw):
        self.RAWdata = raw
        self.rowParse()

    def rowParse(self):
        # Parse row data with "\n"
        self.rowData = self.RAWdata.split("\n")

        # If final splitted character is EOF delete that void element
        if self.rowData[-1] == "":
            del self.rowData[-1]

        # Delete comment line starting with "#"
        rowDataTemp = []
        for eachRow in self.rowData:
            if eachRow[0] != "#":
                rowDataTemp.append(eachRow)
        self.rowData = rowDataTemp

    def colParse(self, delimiter):
        self.datList = []
        for eachRow in self.rowData:
            self.datList.append(eachRow.split(delimiter))

    # keyParse treats the data with special keys(e.g. GPUchunk: value)
    def keyParse(self, Tdelimiter):
        self.keyParsed = True

        self.keyList = []
        for i in range(0, len(self.rowData)):
            keyAndData = self.rowData[i].split(Tdelimiter, 1)
            self.keyList.append(keyAndData[0])
            self.rowData[i] = keyAndData[1];

    # Parse row first and then col
    def datParse(self, delimiter):
        self.colParse(delimiter)

    # ad-hoc tools
    # Transpose matrix and make list other than tuple
    def transpose(self, arr):
        result = zip(*arr)
        result = [list(i) for i in result]
        return result

    def pickSingleLine(self):
        return 0


class Group:
    """Group data to plot each correlated data"""
    def __init__(self, PP, keyX, keyY, **kwargs):
        self.color = "black"
        self.marker = "o"
        if "color" in kwargs:
            self.color = kwargs["color"]
        if "marker" in kwargs:
            self.marker = kwargs["marker"]

        idxX = PP.keyList.index(keyX)
        idxY = PP.keyList.index(keyY)

        self.keyX = keyX
        self.keyY = keyY
        self.legend = None

        self.X = PP.datList[idxX]
        self.Y = PP.datList[idxY]

    def setLegend(self, string):
        self.legend = string

# Back-end plotter
class LinePlotter:
    """Draw graph with grouped data or column-parsed data"""
    def __init__(self, *argv, **kwargs):
        keyLen = len(argv)
        plt.autoscale(enable=True, axis='x', tight=False)
        plt.autoscale(enable=True, axis='y', tight=False)

        if "ylabel" in kwargs:
            plt.ylabel(kwargs["ylabel"])
        if "xlabel" in kwargs:
            plt.xlabel(kwargs["xlabel"])
        if "title" in kwargs:
            plt.title(kwargs["title"])

        if ("width" in kwargs) & ("height" in kwargs):
            fig = plt.gcf()
            fig.set_size_inches(kwargs["width"], kwargs["height"])

        pc = range(0, keyLen)

        legend = []
        for i in range(0, keyLen):
            pc[i], = plt.plot(argv[i].X, argv[i].Y, linewidth=1, marker=argv[i].marker, color=argv[i].color)
            legend.append(argv[i].legend)

        plt.legend(pc, legend)
        plt.grid()
 
    def drawToPdf(self, output):
        pp = PdfPages(output)
        plt.savefig(pp, format='pdf')
        pp.close()
        plt.close()

    def drawToWindow(self):
        plt.show()
        plt.close()

# test case 1, line.dat
test = sys.argv[1]

if test == "line":
    # Data format with special keys
    text = "CPUprofileQuantum: 586.285888671875,1368.364990234375,2372.23291015625\n\
GPUprofileQuantum: 586.285888671875,1368.364990234375\n\
CPUthput: 224.00001335144123,215.71234010546328,219.21960065942372\n\
GPUthput: 166.91645237462322,167.33084515675637\n\
# ewogihweohg\n"

    PP = PatternParser(text)
    PP.keyParse(": ")
    PP.datParse(",")

    GPUdata = Group(PP, "GPUprofileQuantum", "GPUthput", color="red", marker="o")
    CPUdata = Group(PP, "CPUprofileQuantum", "CPUthput", color="blue", marker="x")

    GPUdata.setLegend("GPU") 
    CPUdata.setLegend("CPU") 

    LP = LinePlotter(GPUdata, CPUdata, width=5, height=5, title="LinePlot", xlabel="abc",ylabel="ee")
    # LP.drawToPdf("output.pdf");
    LP.drawToWindow();

elif test == "2":
    # Data format without special keys
    text = "CPUprofileQuantum: 586.285888671875,1368.364990234375,2372.23291015625\n\
GPUprofileQuantum: 586.285888671875,1368.364990234375\n\
CPUthput: 224.00001335144123,215.71234010546328,219.21960065942372\n\
GPUthput: 166.91645237462322,167.33084515675637\n\
# ewogihweohg\n"

elif test == "3":
    text = "# monitoring\n\
39	29.63501	0-3	2401000\n\
42	31.03067	0-3	2401000\n\
41	31.573883000000002	0-3	2401000\n\
40	30.402679499999998	0-3	2401000\n"
    PP = PatternParser(text);
    PP.datParse("\t")
    print(PP.datList)

elif test == "4":
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
    PP.keyParse(": ")
    PP.datParse(",")
    print(PP.keyList)
    print("---------------------------------------------")
    print(PP.datList)

# bar.dat
# legend	seq	cpu-only	gpu-only	cpu+gpu
# bench1	1	1.99999137377027	22.3087676697517	19.6854781960229
# bench2	1	3.75596934740247	76.131169276427	68.9958321030599
# bench3	1	3.82623912897549	87.9507982694475	86.1686550445522
# bench4	1	2.06257527271315	90.8787359592194	91.636723236338
elif test == "5":
    if sys.argv[3] == "\\t":
        temp = "\t"
    else:
        temp = sys.argv[3]
    with open(sys.argv[2]) as inputFile:
        text = inputFile.read();
        PP = PatternParser(text);
        PP.datParse(temp)
    print("---------------------------------------------")
    print(PP.datList)
