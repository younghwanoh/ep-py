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

        self.ax.grid()

    def setLimitOn(self, **kwargs):
        # set y-space
        if "y" in kwargs:
            plt.ylim(kwargs["y"])
        else:
            plt.autoscale(enable=True, axis='y', tight=False)

        # set x-space
        if "x" in kwargs:
            plt.xlim(kwargs["x"])
        else:
            plt.autoscale(enable=True, axis='x', tight=False)

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

    def draw(self, *argv):
        keyLen = len(argv)
        pc = range(0, keyLen)
        legend = []
        for i in range(0, keyLen):
            pc[i], = self.ax.plot(argv[i].X, argv[i].Y, linewidth=1, marker=argv[i].marker, color=argv[i].color)
            legend.append(argv[i].legend)

        self.ax.legend(pc, legend)

class BarPlotter(AbstractPlotter):
    """Draw bar graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)

    def draw(self, *argv):
        keyLen = len(argv)
        pc = range(0, keyLen)
        legend = []
        rects = []
        for i in range(0, keLen):
            rects.append(self.ax.bar(3*i, argv[i].dat, 2, marker=argv[i].marker, color=argv[i].color))
            legend.append(argv[i].legend)

        self.ax.legend(rects, legend)

