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

    def setPropLegend(self, **kwargs):
        if "ncol" in kwargs:
            self.ncol = kwargs["ncol"]
        if "size" in kwargs:
            self.legsize = kwargs["size"]
        if "frame" in kwargs:
            self.frame = kwargs["frame"]

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

    def showToWindow(self):
        plt.show()
        plt.close()

# Back-end plotter
class LinePlotter(AbstractPlotter):
    """Draw line graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)
        self.ax.grid()

    def draw(self, *argv):
        keyLen = len(argv)
        pc = range(keyLen)

        legend = []
        for i in range(keyLen):
            pc[i], = self.ax.plot(argv[i].X, argv[i].Y, linewidth=1, marker=argv[i].marker, color=argv[i].color)
            legend.append(argv[i].legend)

        self.ax.legend(pc, legend)

class CBarPlotter(AbstractPlotter):
    """Draw clustered bar graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)

        self.barwidth = 1
        self.tickLabel = [""]

        if "barwidth" in kwargs:
            self.barwidth = kwargs["barwidth"]

    def draw(self, *argv, **kwargs):
        # default 12% margin to entire bar width
        FigSideMargin = 0.12 

        if "figmargin" in kwargs:
            FigSideMargin = kwargs["figmargin"]
        if "ticklabel" in kwargs:
            self.tickLabel = kwargs["ticklabel"]

        keyLen = len(argv)
        datLen = len(argv[0].Y)

        # Interval between clustered bars: 40% of total width in a clustered group
        interClusterOffset = (self.barwidth*keyLen) * 1.4
        base = np.arange(datLen) * interClusterOffset

        legend = []
        rects = []
        for i in range(keyLen):
            rects.append(self.ax.bar(base+i*self.barwidth, argv[i].Y, self.barwidth, color=argv[i].color, hatch=argv[i].hatch))
            if bool(argv[i].legend):
                legend.append(argv[i].legend)

        # set legend
        self.ax.legend(rects, legend)

        # set xtick point and label
        self.ax.set_xticks(base+(self.barwidth*keyLen)/2)
        self.ax.set_xticklabels(self.tickLabel.content, rotation=self.tickLabel.rotate)


        LengthOfWholeBar = base[-1] + self.barwidth*keyLen
        plt.xlim([-LengthOfWholeBar*FigSideMargin, LengthOfWholeBar*(1+FigSideMargin)])


class CCBarPlotter(AbstractPlotter):
    """Draw clustered*2 bar graph with grouped parsed data"""
    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)

        self.barwidth = 1
        self.tickLabel = [""]

        if "barwidth" in kwargs:
            self.barwidth = kwargs["barwidth"]

    def draw(self, *argv, **kwargs):
        # default 12% margin to entire bar width
        FigSideMargin = 0.12 

        if "figmargin" in kwargs:
            FigSideMargin = kwargs["figmargin"]
        if "groupmargin" in kwargs:
            BtwGroupMargin = kwargs["groupmargin"]
        if "ticklabel" in kwargs:
            # merge multiple label list
            temp = []
            for i in kwargs["ticklabel"]:
                temp += i.content
            self.tickLabel = temp
        if "ticklabel" in kwargs:
            self.tickAngle = kwargs["tickangle"]

        legend = []
        rects = []
        base = []
        globalBase = np.array([])

        # set margin proportional to the first data
        keyLen = argv[0].length
        datLen = len(argv[0].content[0].Y)

        # Interval between clustered bars: 40% of total width in a clustered group
        interClusterOffset = (self.barwidth * keyLen) * 1.4
        # Interval between clustered group: 
        interGlobalOffset = interClusterOffset * datLen * BtwGroupMargin

        for k, eachGroup in enumerate(argv):
            # base calcuation (x position of bar with array)
            base.append(np.arange(datLen) * interClusterOffset + interGlobalOffset * k)

            # Update global accumulative variables
            globalBase = np.concatenate((globalBase, base[k] + (self.barwidth*keyLen)/2)) 

            for i, elem in enumerate(eachGroup.content):
                rects.append(self.ax.bar(base[k]+i*self.barwidth, elem.Y, self.barwidth,
                                         color=elem.color, hatch=elem.hatch))
                if bool(elem.legend):
                    legend.append(elem.legend)

        # set legend
        leg = self.ax.legend(rects, legend, loc="upper center", 
                            ncol=self.ncol, prop={'size':self.legsize})
        leg.draw_frame(self.frame)

        # set xtick point and label
        self.ax.set_xticks(globalBase)
        self.ax.set_xticklabels(self.tickLabel, rotation=self.tickAngle)

        LengthOfWholeBar = base[-1][-1] + self.barwidth*keyLen
        plt.xlim([-LengthOfWholeBar*FigSideMargin, LengthOfWholeBar*(1+FigSideMargin)])
