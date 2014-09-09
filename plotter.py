#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from tools import tTranspose, tMergeCrossSpace

class AbstractPlotter(object):
    # patch: graph obj lists, legend: legend lists
    patch = []
    legend = []

    baseOffset = 0
    globalBase = np.array([])
    def __init__(self, **kwargs):
        self.fig, self.ax = plt.subplots()

        self.manualLegendStyle=False
        self.manualBase = False
        self.tickLabel = tickLabelInit()
        self.tickAngle = 0
        self.FigSideMargin = 0.12 

        if "figmargin" in kwargs:
            self.FigSideMargin = kwargs["figmargin"]
        if "ylabel" in kwargs:
            self.ax.set_ylabel(kwargs["ylabel"])
        if "xlabel" in kwargs:
            self.ax.set_xlabel(kwargs["xlabel"])
        if "title" in kwargs:
            self.ax.set_title(kwargs["title"])
        if ("width" in kwargs) & ("height" in kwargs):
            self.fig.set_size_inches(kwargs["width"], kwargs["height"])

    def setTicks(self, **kwargs):
        if "tspace" in kwargs:
            self.manualBase = True
            self.tspace = kwargs["tspace"]
            #FIXME:: Maual tick space settings aren't yet implemented for BoxPlotter
        if "voffset" in kwargs:
            self.voffset = kwargs["voffset"]
        if "label" in kwargs:
            self.tickLabel = kwargs["label"]
        if "angle" in kwargs:
            self.tickAngle = kwargs["angle"]

    def setBaseOffset(self, offset):
        # Graph's offset if multiple graphs are drawn
        self.baseOffset = offset

    def setLegendStyle(self, **kwargs):
        # Flag for manual legend style change
        self.manualLegendStyle=True

        # Initial values
        self.ncol = 5
        self.legsize = 10
        self.frame = True

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

    def FinalCall(self):
        # Virtual function called after all draw methods are executed
        pass

    def setBottomMargin(self, margin):
        # bottom margin for labels of multiple colomns
        plt.gcf().subplots_adjust(bottom=margin)

    def saveToPdf(self, output):
        self.FinalCall()
        pp = PdfPages(output)
        plt.savefig(pp, format='pdf')
        pp.close()
        plt.close()

    def showToWindow(self):
        self.FinalCall()
        plt.show()
        plt.close()

    # Private function start ====================================================
    def callBeforeDraw(self):
        pass

    def drawLegend(self, target, legend):
        if len(legend) == 0:
            # No legend is specified
            return;

        if self.manualLegendStyle is True:
            leg = self.ax.legend(target, legend, loc="upper center", 
                                 ncol=self.ncol, prop={'size':self.legsize})
            leg.draw_frame(self.frame)
        else:
            self.ax.legend(target, legend)
        self.manualLegendStyle=False
    # Private function end ======================================================

class tickLabelInit:
    """Initializer of tickLabel class"""
    def __init__(self):
        self.content = [""]

# Back-end plotter
class LinePlotter(AbstractPlotter):
    """Draw line graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)
        self.ax.grid()

    def draw(self, *argv):
        self.callBeforeDraw()

        keyLen = len(argv)
        self.patch = range(keyLen)

        for i in range(keyLen):
            self.patch[i], = self.ax.plot(argv[i].X, argv[i].Y, linewidth=1,
                                          marker=argv[i].marker, color=argv[i].color)
            self.legend.append(argv[i].legend)

    def FinalCall(self):
        self.drawLegend(self.patch, self.legend);


class AbstractBarPlotter(AbstractPlotter):
    """Abstract class for Bar plotter"""
    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)
        # Initial base point
        self.base = [0]
        self.barwidth = 1

        if "barwidth" in kwargs:
            # barwidth can be assigned as a style over all bars
            self.barwidth = kwargs["barwidth"] 

    def callBeforeDraw(self, **kwargs):
        # barwidth can also be assigned to each different elem
        if "barwidth" in kwargs:
            self.barwidth = kwargs["barwidth"]


class SBarPlotter(AbstractBarPlotter):
    """Draw stacked bar graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractBarPlotter.__init__(self, **kwargs)

    def setStackStyle(self, **kwargs):
        self.colors = []
        self.hatch = []

        if "legend" in kwargs:
            self.legend = kwargs["legend"]
        if "colors" in kwargs:
            self.colors = kwargs["colors"]
        if "hatch" in kwargs:
            self.hatch = kwargs["hatch"]

    def draw(self, *argv, **kwargs):
        self.callBeforeDraw(**kwargs)

        # Calculate tick point
        keyLen = len(argv)
        left = self.base[-1] + self.baseOffset
        right = left + self.barwidth*(keyLen-1)
        self.base = np.linspace(left, right, keyLen)
        print("Offset: %d, Base: %s" % (self.baseOffset, self.base))

        data = tTranspose(argv)

        # Accumulate tick bases to global base
        self.globalBase = np.concatenate([self.globalBase, self.base])

        stackLen = len(data)
        accum = np.array([0 for i in range(keyLen)])
        for i in range(stackLen):
            accum = [accum[j] + data[i-1][j] for j in range(keyLen)] if i > 0 else accum
            self.patch.append(self.ax.bar(self.base, data[i], self.barwidth,
                              color=self.colors[i], hatch=self.hatch[i], bottom=accum))

    def FinalCall(self):
        # set legend
        self.drawLegend(self.patch, self.legend);

        # set xtick point and label
        if self.manualBase == False:
            self.ax.set_xticks(self.globalBase+float(self.barwidth)/2)
        else:
            self.ax.set_xticks(self.tspace)
            self.ax.set_xticklabels(self.tickLabel.content, rotation=self.tickAngle)

            for t, y in zip( self.ax.get_xticklabels( ), self.voffset ):
                t.set_y( y )
            self.manualBase = True

        self.ax.xaxis.labelpad=10

        LengthOfWholeBar = self.base[-1] + self.barwidth
        plt.xlim([-LengthOfWholeBar*self.FigSideMargin, LengthOfWholeBar*(1+self.FigSideMargin)])


class CBarPlotter(AbstractBarPlotter):
    """Draw clustered bar graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractBarPlotter.__init__(self, **kwargs)

    def draw(self, *argv, **kwargs):
        self.callBeforeDraw(**kwargs)

        self.keyLen = keyLen = len(argv)
        datLen = len(argv[0].Y)

        # Interval between clustered bars: 40% of total width in a clustered group
        interClusterOffset = (self.barwidth*keyLen) * 1.4
        self.base = np.arange(datLen) * interClusterOffset + self.baseOffset + self.base[-1]

        # Accumulate tick bases to global base
        self.globalBase = np.concatenate([self.globalBase, self.base])

        for i in range(keyLen):
            self.patch.append(self.ax.bar(self.base+i*self.barwidth, argv[i].Y,
                                          self.barwidth, color=argv[i].color, hatch=argv[i].hatch))
            if bool(argv[i].legend):
                self.legend.append(argv[i].legend)

    def FinalCall(self):
        # set legend
        self.drawLegend(self.patch, self.legend);

        # set xtick point and label
        self.ax.set_xticks(self.globalBase+(self.barwidth*self.keyLen)/2)
        self.ax.set_xticklabels(self.tickLabel.content, rotation=self.tickAngle)

        LengthOfWholeBar = self.globalBase[-1] + self.barwidth*self.keyLen
        plt.xlim([-LengthOfWholeBar*self.FigSideMargin, LengthOfWholeBar*(1+self.FigSideMargin)])


class CCBarPlotter(AbstractBarPlotter):
    cc_globalBase = np.array([])
    """Draw clustered*2 bar graph with grouped parsed data"""
    def __init__(self, **kwargs):
        AbstractBarPlotter.__init__(self, **kwargs)
        if "groupmargin" in kwargs:
            self.BtwGroupMargin = kwargs["groupmargin"]

    def setTicks(self, **kwargs):
        if "label" in kwargs:
            # merge multiple label list
            temp = []
            for i in kwargs["label"]:
                temp += i.content
            self.tickLabel = temp
        if "angle" in kwargs:
            self.tickAngle = kwargs["angle"]

    def draw(self, *argv, **kwargs):
        self.callBeforeDraw(**kwargs)

        base = []
        globalBase = np.array([])

        # set margin proportional to the first data
        keyLen = argv[0].length
        datLen = len(argv[0].content[0].Y)

        # Interval between clustered bars: 40% of total width in a clustered group
        interClusterOffset = (self.barwidth * keyLen) * 1.4
        # Interval between clustered group: 
        interGlobalOffset = interClusterOffset * datLen * self.BtwGroupMargin

        for k, eachGroup in enumerate(argv):
            self.keyLen = eachGroup.length
            datLen = len(eachGroup.content[0].Y)
            # base calcuation (x position of bar with array)
            base.append(np.arange(datLen) * interClusterOffset +
                        interGlobalOffset * k + self.baseOffset)

            # Update global accumulative variables
            globalBase = np.concatenate((globalBase, base[k] + (self.barwidth*keyLen)/2)) 

            for i, elem in enumerate(eachGroup.content):
                self.patch.append(self.ax.bar(base[k]+i*self.barwidth, elem.Y, self.barwidth,
                                              color=elem.color, hatch=elem.hatch))
                if bool(elem.legend):
                    self.legend.append(elem.legend)

        # Accumulate tick bases to global base
        self.cc_globalBase = np.concatenate([self.cc_globalBase, globalBase])

    def FinalCall(self):
        # set legend
        self.drawLegend(self.patch, self.legend);

        # set xtick point and label
        self.ax.set_xticks(self.cc_globalBase)
        self.ax.set_xticklabels(self.tickLabel, rotation=self.tickAngle)

        LengthOfWholeBar = self.cc_globalBase[-1] + self.barwidth*self.keyLen
        plt.xlim([-LengthOfWholeBar*self.FigSideMargin, LengthOfWholeBar*(1+self.FigSideMargin)])


class AbstractBoxPlotter(AbstractPlotter):
    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)
        # Initial base point
        self.base = [0]

        self.boxwidth = 1
        self.vertical = True

        if "vertical" in kwargs:
            self.vertical = kwargs["vertical"]
        if "boxwidth" in kwargs:
            self.boxwidth = float(kwargs["boxwidth"])

    def callBeforeDraw(self, **kwargs):
        # boxwidth can also be assigned to each different elem
        if "boxwidth" in kwargs:
            self.boxwidth = kwargs["boxwidth"]


class BoxPlotter(AbstractBoxPlotter):
    """Draw clustered bar graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractBoxPlotter.__init__(self, **kwargs)
        # Default properties
        self.timeline = False

        if "timeline" in kwargs:
            self.timeline = kwargs["timeline"]

    def draw(self, *argv, **kwargs):
        self.callBeforeDraw()

        keyLen = len(argv)

        # Calculate global/local base
        if self.timeline is True:
            base = np.linspace(0, 0, keyLen) + self.baseOffset
        else:
            base = np.linspace(0, self.boxwidth*(keyLen+2), keyLen) + self.baseOffset

        # Accumulate tick bases to global base
        self.globalBase = np.concatenate([self.globalBase, base])

        for i in range(keyLen):
            datLen = len(argv[i].X)
            for j in range(datLen):
                if self.vertical is True:
                    rect = plt.Rectangle([base[i], argv[i].X[j]], self.boxwidth, argv[i].Y[j] - argv[i].X[j],
                                         facecolor=argv[i].color, hatch=argv[i].hatch)
                else:
                    rect = plt.Rectangle([argv[i].X[j], base[i]], argv[i].Y[j] - argv[i].X[j], self.boxwidth,
                                         facecolor=argv[i].color, hatch=argv[i].hatch)
                self.ax.add_patch(rect)
            if bool(argv[i].legend):
                self.patch.append(rect)
                self.legend.append(argv[i].legend)

    def FinalCall(self):
        # set legend
        self.drawLegend(self.patch, self.legend);

        # set xtick point and label
        if self.vertical is True:
            self.ax.set_xticks(self.globalBase + self.boxwidth/2)
            self.ax.set_xticklabels(self.tickLabel.content, rotation=self.tickAngle)
        else:
            self.ax.set_yticks(self.globalBase + self.boxwidth/2)
            self.ax.set_yticklabels(self.tickLabel.content, rotation=self.tickAngle)

        # set x / y-range
        if self.vertical is True:
            self.ax.autoscale(enable=True, axis='y', tight=False)
            LengthOfWholeBar = self.globalBase[-1] + self.boxwidth
            plt.xlim([-LengthOfWholeBar*self.FigSideMargin, LengthOfWholeBar*(1+self.FigSideMargin)])
        else:
            self.ax.autoscale(enable=True, axis='x', tight=False)
            LengthOfWholeBar = self.globalBase[-1] + self.boxwidth
            plt.ylim([-LengthOfWholeBar*self.FigSideMargin, LengthOfWholeBar*(1+self.FigSideMargin)])


class CBoxPlotter(AbstractBoxPlotter):
    """Draw clustered bar graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractBoxPlotter.__init__(self, **kwargs)

    def draw(self, *argv, **kwargs):
        self.callBeforeDraw()

        GroupLen = len(argv)

        keyLen = []
        for i in range(GroupLen):
            keyLen.append(argv[i].length)

        # By default, CBoxPlotter draws timeline
        base = np.linspace(0, self.boxwidth*(GroupLen+1), GroupLen) + self.baseOffset

        # Accumulate tick bases to global base
        self.globalBase = np.concatenate([self.globalBase, base])

        for z in range(GroupLen):
            arg = argv[z].content
            for i in range(keyLen[z]):
                datLen = len(arg[i].X)
                for j in range(datLen):
                    if self.vertical is True:
                        rect = plt.Rectangle([base[z], arg[i].X[j]], self.boxwidth, arg[i].Y[j] - arg[i].X[j],
                                             facecolor=arg[i].color, hatch=arg[i].hatch)
                    else:
                        rect = plt.Rectangle([arg[i].X[j], base[z]], arg[i].Y[j] - arg[i].X[j], self.boxwidth,
                                             facecolor=arg[i].color, hatch=arg[i].hatch)
                    self.ax.add_patch(rect)
                if bool(arg[i].legend):
                    self.patch.append(rect)
                    self.legend.append(arg[i].legend)

    def FinalCall(self):
        # set legend
        self.drawLegend(self.patch, self.legend);

        # set xtick point and label
        if self.vertical is True:
            self.ax.set_xticks(self.globalBase + self.boxwidth/2)
            self.ax.set_xticklabels(self.tickLabel.content, rotation=self.tickAngle)
        else:
            self.ax.set_yticks(self.globalBase + self.boxwidth/2)
            self.ax.set_yticklabels(self.tickLabel.content, rotation=self.tickAngle)

        # set x / y-range
        if self.vertical is True:
            self.ax.autoscale(enable=True, axis='y', tight=False)
            LengthOfWholeBar = self.globalBase[-1] + self.boxwidth
            plt.xlim([-LengthOfWholeBar*self.FigSideMargin, LengthOfWholeBar*(1+self.FigSideMargin)])
        else:
            self.ax.autoscale(enable=True, axis='x', tight=False)
            LengthOfWholeBar = self.globalBase[-1] + self.boxwidth
            plt.ylim([-LengthOfWholeBar*self.FigSideMargin, LengthOfWholeBar*(1+self.FigSideMargin)])


class PiePlotter(AbstractPlotter):
    """Draw pie graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)
        self.ax.axis("equal")

    def draw(self, *argv, **kwargs):
        colors = []
        hatch = [0 for i in range(len(argv[0]))]
        legend = []
        if "legend" in kwargs:
            legend = kwargs["legend"]
        if "colors" in kwargs:
            colors = kwargs["colors"]
        if "hatch" in kwargs:
            hatch = kwargs["hatch"]

        patches = self.ax.pie(argv[0], colors=colors, labels=legend)[0]

        for i, val in enumerate(patches):
            patches[i].set_hatch(hatch[i])
