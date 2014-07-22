#!/usr/bin/python

globals()['__display'] = True

import argparse
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.font_manager
matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
# rowwriter = csv.writer(sys.stdout, delimiter='\n')
# colwriter = csv.writer(sys.stdout, delimiter='\t')


# Argument parsing
# title = None
# xlabel = None
# ylabel = None
# output = None
delimiter = '\t'
# delimiter = ','
parser = argparse.ArgumentParser()
parser.add_argument("input", help='Specify input files to draw graph')
parser.add_argument("-o","--output", help='Specify output files to save graph')
parser.add_argument("-f","--format", help='Specify graph format: bar / box / line')
parser.add_argument("-t","--title", help='Write your graph title')
parser.add_argument("-xl","--xlabel", help='Write x-label')
parser.add_argument("-yl","--ylabel", help='Write y-label')
parser.add_argument("-lw","--width", help='Figure width')
parser.add_argument("-lh","--height", help='Figure height')
args = parser.parse_args()
fname = args.input
form = args.format
title = args.title if bool(args.title) else "notitle"
xlabel = args.xlabel if bool(args.xlabel) else "noname"
ylabel = args.ylabel if bool(args.ylabel) else "noname"
output = args.output if bool(args.output) else "output.pdf"

# util function
def parseAndSplit (key, dataType, text, delimiter):
    temp = re.search(r'%s: .*' % (key), text).group()
    temp = re.sub(r'%s: (.*)' % (key), r'\g<1>', temp)
    temp = re.split(delimiter, temp)
    return [dataType(e) for e in temp]


with open(fname) as inputFile:
    text = inputFile.read()

    # Clustered bar format
    # xxlabel: cpu / gpu / static / dynamic
    # xlabel: bench1 / bench2
    # bench   \t cpu \t gpu \t static \t dynamic
    # bench1  \t 1   \t 2   \t 3      \t 4
    # bench2  \t 1   \t 2   \t 3      \t 4

    if form == "bar":
        delimiter = '\t'
        color = ['r','g','b','orange','purple']
        hatch = ['/','//','/','///','/']

        lineText = re.split('\n', text)
        lineText.pop()
        xxlabels = re.split(delimiter, lineText[0])
        del xxlabels[0]
        del lineText[0]

        xlabels = []
        for i in range(0, len(lineText)):
            lineText[i] = re.split(delimiter, lineText[i])
            xlabels.append(lineText[i].pop(0))
            lineText[i] = [float(e) for e in lineText[i]]

        # plot clustered bar
        width = 0.15       # the width of the bars
        margin = 0.2
        data = zip(*lineText)
        ind = np.arange(len(xlabels))  # the x locations for the groups

        # figure size settings
        fig, ax = plt.subplots()
        if bool(args.width):
            fig.set_figwidth(args.width)
        if bool(args.height):
            fig.set_figheight(args.height)

        # draw rectangles
        rects = []
        for i in range(0, len(xlabels)):
            rects.append(ax.bar(ind+width*i, data[i], width, color=color[i], hatch=hatch[i]))

        # add some
        plt.xlim([-margin, ind[len(xlabels)-1] + width*(len(xlabels)+1) + margin])
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.set_xticks(ind+width*2)
        ax.set_xticklabels(xlabels)

        ax.legend( rects, xxlabels )

        pp = PdfPages(output)
        plt.savefig(pp, format='pdf')
        pp.close()
        plt.close()

    # Clustered bar from parseKey
    if form == "bar-norm":
        # parseKeysX = ["data", "data", "data", "data", "data", "dataProfile"]
        # parseKeysY = ["SEQavg","CPUavg", "GPUavg", "SEQiavg", "GPUiavg", "Profile"]
        normalizeKey = "SEQavg"
        stddevKey = "stddev"
        parseKeysX = ["data"]
        parseKeysY = ["SEQiavg", "GPUiavg", "CGCEavg", "Profile"]
        legend = ["CPU-only", "GPU-only", "CGCE-only", "This work"]
        color = ["#ffffff", "grey", "#ffffff", "#000000"]
        hatch = ["", "", "..",""]
        delimiter = '\t'

        # plot settings for bar-norm-diff
        width = 0.25      # width of the bars
        SpaceBtwBars = 0.7   # space between bars (ratio to width)
        margin = 0.2
        fig, ax = plt.subplots()     # figure width and height
        if bool(args.width):
            fig.set_figwidth(args.width)
        if bool(args.height):
            fig.set_figheight(args.height)

        # sub var
        keyLen = len(parseKeysY)
        parseDataX = []
        parseDataY = [[] for i in range(0, keyLen)]

        # parse global x-axis
        DataX = parseAndSplit(parseKeysX, int, text, delimiter)
        DataLen = len(DataX)

        # make x-axis point
        ind = np.array([e*width*(keyLen+SpaceBtwBars) for e in range(0, DataLen)])

        # parse normalize key and its data
        normData = parseAndSplit(normalizeKey, float, text, delimiter)

        # parse standard deviation key and its data
        stddev = [1 for e in range(0, DataLen)]
        # stddev = parseAndSplit(stddevKey, float, text, delimiter)

        # parse y-data and draw bars
        rects = []
        for i in range(0, keyLen):
            parseDataY[i] = parseAndSplit(parseKeysY[i], float, text, delimiter)

            # normalize (with reverse ratio)
            parseDataY[i] = [(normData[k]/parseDataY[i][k]) for k in range(0, len(parseDataY[i]))]

            rects.append(plt.bar(ind+width*i, parseDataY[i], width, color=color[i], hatch=hatch[i], yerr=stddev))

        # plot settings 
        plt.autoscale(enable=True,axis='y',tight=False)
        # plt.autoscale(enable=True,axis='x',tight=False)
        plt.xlim([-margin*2, ind[len(DataX)-1] + width*(keyLen) + margin*2])
        # plt.ylim([0, max([e for e in parseDataY[1]])+0.5])

        labelfnt = '20'
        plt.xticks(ind+(width*keyLen)/2, DataX, rotation='45', fontsize=labelfnt)
        plt.tick_params(axis='y', labelsize=labelfnt, pad=13, size=10)
        plt.ylabel(ylabel, fontsize=labelfnt)
        plt.xlabel(xlabel, fontsize=labelfnt)
        plt.subplots_adjust(bottom=0.15)
        
        plt.legend(rects, legend, loc="upper left", ncol=1, prop={'size':20})

        pp = PdfPages(output)
        plt.savefig(pp, format='pdf')
        pp.close()
        plt.close()

    # Rectangle format (parsing key: clustered) -- runtime box graph
                # CPU 0 S: 2.01513671875,796.010986328125,1473.43603515625
                # CPU 0 E: 795.9951171875,1473.39404296875,2616.083984375
                # CPU 1 S: 2.02294921875,347.43896484375,685.344970703125,1339.2451171875
                # CPU 1 E: 347.3779296875,685.326171875,1339.220947265625,2431.3759765625
                # CPU 2 S: 2.027099609375,348.198974609375,686.010986328125,1361.590087890625
                # CPU 2 E: 348.18505859375,685.983154296875,1361.51806640625,2549.39111328125
                # CPU 3 S: 2.031005859375,753.9150390625,1953.3720703125
                # CPU 3 E: 753.902099609375,1953.31005859375,2056.718017578125
                # GPU S: 1.994140625,800.839111328125
                # GPU E: 800.779052734375,2235.4169921875

    if form == "box":
        parseKeys = ["CPU 0", "CPU 1", "CPU 2", "CPU 3", "GPU"]
        color = ["#aaaaaa", "#aaaaaa", "#aaaaaa", "#aaaaaa", "purple"]
        hatch = ["/", "//", "///", "/", "/"]
        delimiter = ','

        # sub control variables
        keyLen = len(parseKeys)
        parseData = [[] for i in range(0, keyLen)]
        parseEndData = [[] for i in range(0, keyLen)]
        for i in range(0, keyLen):
            # start time parsing
            temp = re.search(r'%s S: .*' % (parseKeys[i]), text).group()
            parseData[i] = re.sub(r'%s S: (.*)' % (parseKeys[i]), r'\g<1>', temp)
            parseData[i] = re.split(delimiter, parseData[i])
            parseData[i] = np.array([float(e) for e in parseData[i]])
            # end time parsing
            temp = re.search(r'%s E: .*' % (parseKeys[i]), text).group()
            parseEndData[i] = re.sub(r'%s E: (.*)' % (parseKeys[i]), r'\g<1>', temp)
            parseEndData[i] = re.split(delimiter, parseEndData[i])
            parseEndData[i] = np.array([float(e) for e in parseEndData[i]])

        # plot time diagram (bar)
        width=1.2  # bar width
        xBarPosition = np.linspace(0, width*(keyLen+2), keyLen) + width  # bar x-position
        for i in range(0, keyLen):  # device traversion (CPU/GPU) and plot rectangle
            for j in range(0, parseData[i].size):  # chunks per device traversion
                rect = plt.Rectangle([xBarPosition[i], parseData[i][j]], width, parseEndData[i][j] - parseData[i][j],
                       facecolor=color[i], hatch=hatch[i])
                plt.gca().add_patch(rect)

        finalMax = 0
        for i in range(0, keyLen):
            currentMax = np.max(parseEndData[i])
            if finalMax < currentMax:
                finalMax = currentMax

        # plot information
        plt.xticks(np.concatenate([xBarPosition + width/2, np.array([xBarPosition[4]+ width*2])]),
                   parseKeys)
        plt.autoscale(enable=True,axis='y',tight=False)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)

        totaltime = float(re.search(r'\d+.\d+', text).group())
        plt.annotate('Total Time: %f ms\n' % (totaltime), xy=(0.05, 1.05), xycoords='axes fraction')

        # save to pdf files
        pp = PdfPages(output)
        plt.savefig(pp, format='pdf')
        pp.close()
        plt.close()


    if form == "line":
        parseKeysX = ["CPUprofileQuantum", "GPUprofileQuantum"]
        parseKeysY = ["CPUthput", "GPUthput"]
        # parseKeysX = ["data"]
        # parseKeysY = ["SEQavg"]
        # parseKeysX = ["data", "data", "data"]
        # parseKeysY = ["SEQavg","CPUavg", "GPUavg"]
        color = ["red", "purple", "blue", "green", "black"]
        marker = ['x', 'o', "+", "*", "x"]
        delimiter = ','
        legend = ["Out of the box", "Tracking best"]

        # sub control
        keyLen = len(parseKeysY)
        parseDataX = [[] for i in range(0, keyLen)]
        parseDataY = [[] for i in range(0, keyLen)]

        # plot throughput variation diagram (point)
        plt.autoscale(enable=True,axis='x',tight=False)
        plt.autoscale(enable=True,axis='y',tight=False)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        pc=range(0,keyLen)

        idx=0
        for i in range(0, keyLen):
            temp1 = re.search(r'%s: .*' % (parseKeysX[i]), text)
            temp2 = re.search(r'%s: .*' % (parseKeysY[i]), text)
            if bool(temp1) & bool(temp2):
                temp = temp1.group()
                parseDataX[i] = re.sub(r'%s: (.*)' % (parseKeysX[i]), r'\g<1>', temp)
                parseDataX[i] = re.split(delimiter, parseDataX[i])
                parseDataX[i] = np.array([float(e) for e in parseDataX[i]])
                temp = temp2.group()
                parseDataY[i] = re.sub(r'%s: (.*)' % (parseKeysY[i]), r'\g<1>', temp)
                parseDataY[i] = re.split(delimiter, parseDataY[i])
                parseDataY[i] = np.array([float(e) for e in parseDataY[i]])
                pc[idx], = plt.plot(parseDataX[i], parseDataY[i], linewidth=1, marker=marker[i], color=color[i])
                idx += 1
                

        # plt.annotate('Total Time: %f ms\n' % (totaltime), xy=(0.05, 1.05), xycoords='axes fraction')
        plt.legend(pc, legend)
        plt.grid()

        pp = PdfPages(output)
        plt.savefig(pp, format='pdf')
        pp.close()
        plt.close()

    if form == "line-norm":
        normalizeIdx = 0;
        # parseKeysX = ["data", "data", "data", "data", "data", "dataProfile"]
        # parseKeysY = ["SEQavg","CPUavg", "GPUavg", "SEQiavg", "GPUiavg", "Profile"]
        parseKeysX = ["data", "data", "data", "data", "data", "dataProfile"]
        parseKeysY = ["SEQavg","CPUavg", "CGCEavg", "SEQiavg", "GPUiavg", "Profile"]
        legend = ["Out of the box", "Tracking best", "CPU-only", "GPU-only", "Lifelong prof"]
        color = ["red", "purple", "blue", "green", "black", "brown"]
        marker = ['x', 'o', '+', '*', 'x', '+']
        delimiter = '\t'

        # sub control
        keyLen = len(parseKeysY)
        parseDataX = [[] for i in range(0, keyLen)]
        parseDataY = [[] for i in range(0, keyLen)]

        # plot throughput variation diagram (point)
        plt.autoscale(enable=True,axis='x',tight=False)
        plt.autoscale(enable=True,axis='y',tight=False)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        pc=range(0,keyLen)

        idx=0
        # legend=[]
        for i in range(0, keyLen):
            temp1 = re.search(r'%s: .*' % (parseKeysX[i]), text)
            temp2 = re.search(r'%s: .*' % (parseKeysY[i]), text)
            if bool(temp1) & bool(temp2):
                temp = temp1.group()
                parseDataX[i] = re.sub(r'%s: (.*)' % (parseKeysX[i]), r'\g<1>', temp)
                parseDataX[i] = re.split(delimiter, parseDataX[i])
                npDataX = np.array([float(e) for e in parseDataX[i]])

                temp = temp2.group()
                parseDataY[i] = re.sub(r'%s: (.*)' % (parseKeysY[i]), r'\g<1>', temp)
                parseDataY[i] = re.split(delimiter, parseDataY[i])
                parseDataY[i] = [float(e) for e in parseDataY[i]]
                if i == normalizeIdx:
                    nData = parseDataY[i]
                parseDataY[i] = [(nData[k]/parseDataY[i][k]) for k in range(0, len(parseDataY[i]))]
                npDataY = np.array(parseDataY[i])

                pc[idx], = plt.plot(npDataX, npDataY, linewidth=1, marker=marker[i], color=color[i])
                # legend.append(parseKeysY[i])
                idx += 1
                

        # plt.annotate('Total Time: %f ms\n' % (totaltime), xy=(0.05, 1.05), xycoords='axes fraction')
        plt.legend(pc, legend)
        plt.grid()

        pp = PdfPages(output)
        plt.savefig(pp, format='pdf')
        pp.close()
        plt.close()
