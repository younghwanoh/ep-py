#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class AbstractPlotter(object):
    def __init__(self, **kwargs):
        self.fig, self.ax = plt.subplots()
        if "ylabel" in kwargs:
            self.ax.set_ylabel(kwargs["ylabel"])
        if "xlabel" in kwargs:
            self.ax.set_xlabel(kwargs["xlabel"])
        if "title" in kwargs:
            self.ax.set_title(kwargs["title"])

        if ("width" in kwargs) & ("height" in kwargs):
            self.fig.set_size_inches(kwargs["width"], kwargs["height"])

        self.ax.autoscale(enable=True, axis='y', tight=False)
        self.ax.autoscale(enable=True, axis='x', tight=False)
        self.ax.grid()

    def setLimitOn(self, **kwargs):
        # set y-space
        if "y" in kwargs:
            plt.ylim(kwargs["y"])

        # set x-space
        if "x" in kwargs:
            plt.xlim(kwargs["x"])

    def saveToPdf(self, output):
        pp = PdfPages(output)
        plt.savefig(pp, format='pdf')
        pp.close()
        plt.close()

    def showToWbeginow(self):
        plt.show()
        plt.close()

# Back-end plotter
class LinePlotter(AbstractPlotter):
    """Draw line graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)

    def draw(self, *argv):
        keyLen = len(argv)
        pc = range(keyLen)

        legend = []
        for i in range(keyLen):
            pc[i], = self.ax.plot(argv[i].X, argv[i].Y, linewidth=1, marker=argv[i].marker, color=argv[i].color)
            legend.append(argv[i].legend)

        self.ax.legend(pc, legend)

class CBarPlotter(AbstractPlotter):
    """Draw bar graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)

        self.barwidth = 1
        self.tickLabel = [""]

        if "barwidth" in kwargs:
            self.barwidth = kwargs["barwidth"]

    def draw(self, *argv, **kwargs):
        # default 12% margin to entire bar width
        PerFigToMargin = 0.12 

        if "margin" in kwargs:
            PerFigToMargin = kwargs["margin"]
        if "ticklabel" in kwargs:
            self.tickLabel = kwargs["ticklabel"].content

        keyLen = len(argv)
        datLen = len(argv[0].Y)
        pc = range(keyLen)

        # Interval between clustered bars: 40% of total width in a clustered group
        interGlobalOffset = (self.barwidth*keyLen) * 1.4
        begin = np.arange(datLen) * interGlobalOffset

        legend = []
        rects = []
        for i in range(keyLen):
            rects.append(self.ax.bar(begin+i*self.barwidth, argv[i].Y, self.barwidth, color=argv[i].color, hatch=argv[i].hatch))
            if bool(argv[i].legend):
                legend.append(argv[i].legend)

        # set legend
        self.ax.legend(rects, legend)

        # set xtick point and label
        self.ax.set_xticks(begin+(self.barwidth*keyLen)/2)
        self.ax.set_xticklabels(self.tickLabel)


        LengthOfWholeBar = begin[-1] + self.barwidth*keyLen
        plt.xlim([-LengthOfWholeBar*PerFigToMargin, LengthOfWholeBar*(1+PerFigToMargin)])

    def ticks(self, *tickLabel):
        self.tickLabel = tickLabel
