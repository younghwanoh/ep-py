#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import argparse

from matplotlib import font_manager
font_manager.findfont('Arial')

parser = argparse.ArgumentParser()
parser.add_argument("inFile", help='Specify input data file: [ optimizer,others,... ]')
parser.add_argument("-o","--outFile", help='Specify output pdf-file for each benchmark')
parser.add_argument("-t","--title", help='Specify label title (benchmark)')
args = parser.parse_args()

target = args.inFile.split(",")

def preprocess(text):
    # split contents
    text = text.split('\n')
    del text[-1] # trim EOF

    # skip comment statement    
    data = []
    for i in text:
        if  i[0] != "#":
            data.append(i.split('\t'))

    # transpose to make it row-major
    text = zip(*data)
    return text

with open(target[0]) as inputFile:
    text = inputFile.read()

    text = preprocess(text)

    fps = text[0]
    power = text[1]
    core = text[2]
    core = [int(i[2]) for i in core]
    freq = text[3]
    freq = [float(i)/1000000 for i in freq]


    numOfplots = 3
    iterPlotVector = range(0, numOfplots)

    # common settings
    titleOffset = -0.40
    titleFontSize = 16
    labelFontSize = 14
    fig, ax = plt.subplots(numOfplots, sharex=True)
    fig.set_figheight(9.0)
    plt.subplots_adjust(hspace=0.45)

    # line graph =====================================================================================

    # plot fps =======================================================================================
    # ================================================================================================
    xlab = "time (sec)"
    ylab = "FPS"
    ylim = 50
    title = "(i)"
    marker = "o"

    ax[0].set_ylim((0, ylim))
    ax[0].set_ylabel(ylab, fontsize=labelFontSize,
                     fontweight='bold', multialignment='center')
    ax[0].yaxis.set_label_coords(-0.06, 0.5)
    ax[0].set_title(title, y=titleOffset, fontsize=titleFontSize)
    ax[0].grid()

    pc0, = ax[0].plot(fps, linewidth=2, markersize=7, marker=marker)

    # plot freq, core ================================================================================
    # ================================================================================================
    ylab = ["Frequency (GHz)", "# of active cores"]
    ylim = [3, 4]
    title = "(ii)"
    marker = ["o", "x"]

    # plot frequency
    ax[1].set_ylim((0, ylim[0]))
    ax[1].set_ylabel(ylab[0], fontsize=labelFontSize,
                     fontweight='bold', multialignment='center')
    ax[1].yaxis.set_label_coords(-0.06, 0.5)
    ax[1].set_title(title, y=titleOffset, fontsize=titleFontSize)
    ax[1].grid()

    pc1, = ax[1].plot(freq, linewidth=2, markersize=7, marker=marker[0])

    # plot the number of active cores
    ax2 = ax[1].twinx()
    ax2.set_yticks([0, 1, 2, 3, 4])
    ax2.set_ylim((0, ylim[1]))
    ax2.set_ylabel(ylab[1], fontsize=labelFontSize,
                     fontweight='bold', multialignment='center')
    ax2.yaxis.set_label_coords(1.05, 0.5)

    pc2, = ax2.plot(core, linewidth=2, markersize=7, marker=marker[1], color="red")

    # plot power =====================================================================================
    # ================================================================================================
    xlab = "time (sec)"
    ylab = "Power (Watt)"
    ylim = 40
    xlim = 50
    title = "(iii)"
    marker = "o"

    ax[2].set_ylim((0, ylim))
    ax[2].set_xlim((0, xlim))
    ax[2].set_xticks(np.arange(0, 52, 5))
    ax[2].set_xlabel(xlab, fontsize=labelFontSize, fontweight='bold')
    ax[2].set_ylabel(ylab, fontsize=labelFontSize,
                     fontweight='bold', multialignment='center')
    ax[2].yaxis.set_label_coords(-0.06, 0.5)
    ax[2].set_title(title, y=titleOffset, fontsize=titleFontSize)
    ax[2].grid()

    pc3, = ax[2].plot(power, linewidth=2, markersize=7, marker=marker) 

    pp = PdfPages(args.outFile)
    plt.savefig(pp, format='pdf')
    pp.close()
    plt.close()

