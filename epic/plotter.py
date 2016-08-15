#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
from tools import tTranspose, tMergeCrossSpace, tCheckArgsExists

# Load Arial fonts as default
# import matplotlib.font_manager as fm
# arial_prop = fm.FontProperties(fname='./Arial.ttf')

# matplotlib.rcParams['pdf.use14corefonts'] = True # Helvetica
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'Arial'

class AbstractProp(object):
    """Holding properties"""
    def __init__(self):
        pass

    def store(self, kwargs):
        myVars = vars(self)

        # tools.py:: Check arguments exist
        # Store
        ifnot = []
        for elem in kwargs.keys():
            try:
                ifnot.append(myVars[elem])
            except:
                print("Warning! Current plotter doesn't have requested props. Remove it.")
                kwargs.pop(elem)

        tCheckArgsExists(kwargs, *kwargs.keys(), ifnot=ifnot)

    def load(self):
        result = {}
        myVars = vars(self)
        for key, val in myVars.items():
            result[key] = val[0]

        return result

    def m_dump(self):
        attrs = vars(self)
        print ', '.join("%s: %s" % item for item in attrs.items())

class LegendProp(AbstractProp):
    """Holding legend properties"""
    def __init__(self):
        AbstractProp.__init__(self)

        # All properties are defined as arrays[0] to reference and update it
        self.loc = [False]
        self.pos = [False]
        self.ncol = [False]
        self.size = [False]
        self.frame = [True]
        self.tight = [False]

    def load(self):
        result = {}
        if bool(self.ncol[0]) is True:
            result["ncol"] = self.ncol[0]
        if bool(self.size[0]) is True:
            result["prop"] = {'size':self.size[0]}
        if bool(self.pos[0]) is True:
            result["bbox_to_anchor"] = self.pos[0]
        if bool(self.loc[0]) is True:
            result["loc"] = self.loc[0]
        if bool(self.tight[0]) is True:
            # result["handlelength"] = 1.3
            result["handletextpad"] = 0.3
            result["columnspacing"] = 0.8
        return result

    def dump(self):
        print("\n========= Legend Properties ===========")
        m_dump()


class PlotterProp(AbstractProp):
    """Holding plotter properties"""
    def __init__(self):
        AbstractProp.__init__(self)

        self.markersize = [False]

    def dump(self):
        print("\n========= Plotter Properties ===========")
        m_dump()


# shell class for subplots
class SubPlotter(object):
    baseOffset = 0
  
    def __init__(self, *argv, **kwargs):
        assert(len(argv) > 0), "Assign the number of subplots @ SubPlotter!"
        if "sharex" in kwargs:
            self.fig, self.ax = plt.subplots(argv[0], sharex=kwargs["sharex"])
        else:
            self.fig, self.ax = plt.subplots(argv[0])
        if "title" in kwargs:
            self.ax[0].set_title(kwargs["title"])
        if "height" in kwargs:
            self.fig.set_figheight(kwargs["height"])
        if "width" in kwargs:
            self.fig.set_figwidth(kwargs["width"])

    def getAxis(self, *argv, **kwargs):
        tCheckArgsExists(kwargs, "twinx")
        assert(len(argv) > 0), "Assign the index ofi a subplot @ SubPlotter!"
        if kwargs["twinx"] is True:
            return self.ax[argv[0]].twinx()
        else:
            return self.ax[argv[0]]

    def getFig(self):
        return self.fig

    def adjust(self, **kwargs):
        plt.subplots_adjust(**kwargs)

    def saveToPdf(self, output):
        pp = PdfPages(output)
        plt.savefig(pp, format='pdf')
        pp.close()
        plt.close()

    def showToWindow(self):
        plt.show()
        plt.close()

class AbstractPlotter(object):
    baseOffset = 0
  
    def __init__(self, **kwargs):
        self.externalAxisMode = False
        self.manualYtick = False
        self.manualXtick = False
        self.fontsize = 12
        self.tickLabel = tickLabelInit()
        self.tickAngle = 0
        self.tickAlign = "center"
        self.FigSideMargin = 0.12 

        # Property classes
        self.legendProp = LegendProp()
        self.splotterProp = PlotterProp()

        if (not ("axis" in kwargs)) & (not ("fig" in kwargs)):
            self.fig, self.ax = plt.subplots()
        if "axis" in kwargs:
            self.externalAxisMode = True
            self.ax = kwargs["axis"]
        if "fig" in kwargs:
            self.fig = kwargs["fig"]
        if "ylabel" in kwargs:
            if type(kwargs["ylabel"]) is list:
                ylabel = kwargs["ylabel"]
                self.ax.set_ylabel(ylabel[0], ha=self.tickAlign,
                                   fontweight=ylabel[1], fontsize=ylabel[2])
            else:
                self.ax.set_ylabel(kwargs["ylabel"], ha=self.tickAlign)
        if "xlabel" in kwargs:
            if type(kwargs["xlabel"]) is list:
                xlabel = kwargs["xlabel"]
                self.ax.set_xlabel(xlabel[0], ha=self.tickAlign,
                                   fontweight=xlabel[1], fontsize=xlabel[2])
            else:
                self.ax.set_xlabel(kwargs["xlabel"], ha=self.tickAlign)
        if "title" in kwargs:
            self.ax.set_title(kwargs["title"])
        if ("width" in kwargs) & ("height" in kwargs):
            self.fig.set_size_inches(kwargs["width"], kwargs["height"])

    def getAxis(self, **kwargs):
        tCheckArgsExists(kwargs, "twinx")
        if kwargs["twinx"] is True:
            return self.ax.twinx()
        else:
            return self.ax

    def annotate(self, text, xy, **kwargs):
        if "fontsize" in kwargs:
            fontsize = kwargs["fontsize"]
        for i in range(len(text)):
            trans = self.ax.get_xaxis_transform()
            self.ax.annotate(text[i], xy=xy[i], xycoords=trans,
                             fontsize=fontsize, annotation_clip=False)

    def setTicks(self, **kwargs):
        if "yspace" in kwargs:
            self.manualYtick = True
            self.yspace=kwargs["yspace"]
            #FIXME:: Maual ytick space settings supports only CBoxPlotter
        if "xspace" in kwargs:
            self.manualXtick = True
            self.xspace = kwargs["xspace"]
            #FIXME:: Maual xtick space settings aren't yet implemented for BoxPlotter
        if "voffset" in kwargs:
            self.voffset = kwargs["voffset"]
        if "label" in kwargs:
            self.tickLabel = kwargs["label"]
        if "angle" in kwargs:
            self.tickAngle = kwargs["angle"]
        if "align" in kwargs:
            self.tickAlign = kwargs["align"]
        if "fontsize" in kwargs:
            self.fontsize = kwargs["fontsize"]

        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off'          # ticks along the top edge are off
        )

    def setBaseOffset(self, offset):
        # Graph's offset if multiple graphs are drawn
        self.baseOffset = offset

    def setLegendStyle(self, **kwargs):
        leg = self.legendProp
        self.legendProp.store(kwargs)

    def vline(self, **kwargs):
        if ("color" in kwargs) & ("linestyle" in kwargs):
            self.ax.axvline(x=kwargs["x"], ymin=kwargs["yrange"][0], ymax=kwargs["yrange"][1],
            color=kwargs["color"], linestyle=kwargs["linestyle"], zorder=100)
        else:
            self.ax.axvline(x=kwargs["x"], ymin=kwargs["yrange"][0], ymax=kwargs["yrange"][1],
            zorder=100)

    def hline(self, **kwargs):
        if ("color" in kwargs) & ("linestyle" in kwargs):
            self.ax.axhline(y=kwargs["y"], xmin=kwargs["xrange"][0], xmax=kwargs["xrange"][1],
            color=kwargs["color"], linestyle=kwargs["linestyle"], zorder=100)
        else:
            self.ax.axhline(y=kwargs["y"], xmin=kwargs["xrange"][0], xmax=kwargs["xrange"][1],
            zorder=100)

    def setFigureStyle(self, **kwargs):
        # set overall figure styles
        if "bottomMargin" in kwargs:
            plt.gcf().subplots_adjust(bottom=kwargs["bottomMargin"])
        if "topMargin" in kwargs:
            plt.gcf().subplots_adjust(top=kwargs["topMargin"])
        if "leftMargin" in kwargs:
            plt.gcf().subplots_adjust(left=kwargs["leftMargin"])
        if "rightMargin" in kwargs:
            plt.gcf().subplots_adjust(right=kwargs["rightMargin"])
        if "fontsize" in kwargs:
            matplotlib.rcParams.update({'font.size': kwargs["fontsize"]})
        if "figmargin" in kwargs:
            self.FigSideMargin = kwargs["figmargin"]

        # grid on/off
        if "grid" in kwargs:
            if kwargs["grid"] is True:
                self.ax.grid(zorder=-1)
        if "gridx" in kwargs:
            if kwargs["gridx"] is True:
                self.ax.xaxis.grid(zorder=-1)
        if "gridy" in kwargs:
            if kwargs["gridy"] is True:
                self.ax.yaxis.grid(zorder=-1)

        # set y-space
        if "ylim" in kwargs:
            self.ax.set_ylim(kwargs["ylim"])
        # set x-space
        if "xlim" in kwargs:
            self.ax.set_xlim(kwargs["xlim"])

        # adjust y-label position
        if "ylpos" in kwargs:
            self.ax.yaxis.set_label_coords(*kwargs["ylpos"])
        # adjust x-label position
        if "xlpos" in kwargs:
            self.ax.xaxis.set_label_coords(*kwargs["xlpos"])

        # private virtual method that differs from Plotter classes
        self.m_setFigureStyle(**kwargs)

    def finish(self):
        self.m_finish()

    def saveToPdf(self, output):
        self.m_finish()
        pp = PdfPages(output)
        plt.savefig(pp, format='pdf')
        pp.close()
        plt.close()

    def showToWindow(self):
        self.m_finish()
        plt.show()
        plt.close()

    # Private function start ====================================================
    def m_setFigureStyle(self, **kwargs):
        # CCBar:: Virtual function while setFigureStyle
        pass

    def m_finish(self):
        # Virtual function called after all draw methods are executed
        pass

    def m_beforeEveryDraw(self):
        # Virtual function called before each draw methods is executed
        pass

    def m_checkDuplicatedKeyIn(self, target, legend):
        temp_legend = []
        temp_target = []
        referedKey = []
        for patch, leg in zip(target, legend):
            try:
                referedKey.index(leg)
            except:
                referedKey.append(leg)
                temp_legend.append(leg)
                temp_target.append(patch)
        return temp_legend, temp_target

    def m_drawLegend(self, target, legend):
        if len(legend) == 0:
            # No legend is specified
            return;

        legend, target = self.m_checkDuplicatedKeyIn(target, legend)
        
        # Get legend properties
        p_legendProp = self.legendProp.load()
        handler = self.ax.legend(target, legend, **p_legendProp)

        # self.legendProp.dump()

        handler.draw_frame(self.legendProp.frame[0])

    # Private function end ======================================================

class tickLabelInit:
    """Initializer of tickLabel class"""
    def __init__(self):
        self.content = [""]

# Back-end plotter
class LinePlotter(AbstractPlotter):
    """Draw line graph with grouped data or column-parsed data"""
    patch = []
    legend = []
    # patch: graph obj lists, legend: legend lists
    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)
        tCheckArgsExists(kwargs, "flushLegend")
        if kwargs["flushLegend"] is True:
            LinePlotter.patch = []
            LinePlotter.legend = []
 
        self.base = 0
        self.linewidth = 2
        # self.ax.yaxis.grid(zorder=-1)

    def draw(self, *argv):
        self.m_beforeEveryDraw()

        p_plotterProp = self.splotterProp.load()
        if p_plotterProp["markersize"] is False:
            p_plotterProp.pop("markersize")

        keyLen = len(argv)
        self.patch = range(keyLen)

        self.base += self.baseOffset
        for i in range(keyLen):
            shiftedX = np.array(argv[i].X) + self.base 
            self.patch[i], = self.ax.plot(shiftedX, argv[i].Y, linewidth=self.linewidth, zorder=3,
                                          marker=argv[i].marker, markeredgecolor=argv[i].face,
                                          color=argv[i].color, mew=1, **p_plotterProp)
            if bool(argv[i].legend):
                self.legend.append(argv[i].legend)

    def m_setFigureStyle(self, **kwargs):
        self.splotterProp.store(kwargs)

    def m_finish(self):
        self.m_drawLegend(self.patch, self.legend);

        if self.manualYtick is True:
            self.ax.set_yticks(self.yspace)
        # set xtick point and label
        if self.manualXtick == True:
            self.ax.set_xticks(self.xspace)
            self.ax.set_xticklabels(self.tickLabel.content, rotation=self.tickAngle, ha=self.tickAlign,
                                    fontsize=self.fontsize)

class DotPlotter(LinePlotter):
    """Draw dot graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        # DotPlotter is exactly same with LinePlotter, but linewidth
        LinePlotter.__init__(self, **kwargs)
        self.linewidth=0

class AbstractBarPlotter(AbstractPlotter):
    """Abstract class for Bar plotter"""
    # patch: graph obj lists, legend: legend lists
    patch = []
    legend = []
    globalBase = np.array([])

    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)
        # Initial base point
        self.base = [0.0]
        self.barwidth = 1.0
        self.interCmargin = 1.4
        self.interMargin = 0

    def getGlobalBase(self):
        return self.globalBase

    def m_setFigureStyle(self, **kwargs):
        if "interCmargin" in kwargs:
            self.interCmargin = kwargs["interCmargin"] + 1 
        if "interMargin" in kwargs:
            self.interMargin = kwargs["interMargin"] 
        if "barwidth" in kwargs:
            # barwidth can be assigned as a style over all bars
            self.barwidth = float(kwargs["barwidth"])

    def m_beforeEveryDraw(self, **kwargs):
        # barwidth can also be assigned to each different elem
        if "barwidth" in kwargs:
            self.barwidth = float(kwargs["barwidth"])


class SBarPlotter(AbstractBarPlotter):
    """Draw stacked bar graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractBarPlotter.__init__(self, **kwargs)
        self.transposedStack = False
        self.vertical = True

        if "vertical" in kwargs:
            self.vertical = kwargs["vertical"]

    def setStackStyle(self, **kwargs):
        # only used if transpose optiion is turned on
        self.transposedStack = True

        self.colors = []
        self.hatch = []

        if "legend" in kwargs:
            self.legend = kwargs["legend"]
        if "colors" in kwargs:
            self.colors = kwargs["colors"]
        if "hatch" in kwargs:
            self.hatch = kwargs["hatch"]

    def draw(self, *argv, **kwargs):
        self.m_beforeEveryDraw(**kwargs)

        if self.transposedStack is True:
            keyLen = len(argv)
        else:
            keyLen = len(argv[0].Y)

        # Calculate tick point
        left = self.base[-1] + self.baseOffset
        right = left + self.barwidth*(keyLen-1) + self.interMargin
        self.base = np.linspace(left, right, keyLen)
        # print("Offset: %d, Base: %s" % (self.baseOffset, self.base))

        # Accumulate tick bases to global base
        self.globalBase = np.concatenate([self.globalBase, self.base])

        if self.transposedStack is True:
            # transposed data
            data = tTranspose(argv)

            stackLen = len(data)
            accum = np.array([0 for i in range(keyLen)])

            for i in range(stackLen):
                accum = [accum[j] + data[i-1][j] for j in range(keyLen)] if i > 0 else accum

                # horizontal or vertical plot
                if self.vertical is False:
                    drawer = self.ax.barh
                    kwd_args = {"left":accum}
                else:
                    drawer = self.ax.bar
                    kwd_args = {"bottom":accum}
                self.patch.append(drawer(self.base, data[i], self.barwidth, zorder=3,
                                  color=self.colors[i], hatch=self.hatch[i], **kwd_args))
        else:
            # not transposed data
            data = argv

            stackLen = len(data)
            accum = np.array([0 for i in range(keyLen)])

            for i in range(stackLen):
                accum = [accum[j] + data[i-1].Y[j] for j in range(keyLen)] if i > 0 else accum

                # horizontal or vertical plot
                if self.vertical is False:
                    drawer = self.ax.barh
                    kwd_args = {"left":accum}
                else:
                    drawer = self.ax.bar
                    kwd_args = {"bottom":accum}
                self.patch.append(drawer(self.base, data[i].Y, self.barwidth, zorder=3,
                                  color=data[i].color, hatch=data[i].hatch, **kwd_args))
                if bool(data[i].legend):
                    self.legend.append(data[i].legend)


    def m_finish(self):
        self.transposedStack = False

        # set legend
        self.m_drawLegend(self.patch, self.legend);

        # set xtick point and label

        if self.vertical is False:
            # Label axis: y, value axis: x
            labelAxisTicker = self.ax.set_yticks
            labelAxisSpace = self.yspace if self.manualYtick else False
            getLabelAxisLabel = self.ax.get_yticklabels if self.manualYtick else False

            valueAxisTicker = self.ax.set_xticks
            valueAxisSpace = self.xspace if self.manualXtick else False
            getValueAxisLabel = self.ax.get_xticklabels if self.manualXtick else False

            labelTicker = self.ax.set_yticklabels
            axis = self.ax.xaxis
            figLimit = plt.ylim
        else:
            # Label axis: x, value axis: y
            labelAxisTicker = self.ax.set_xticks
            labelAxisSpace = self.xspace if self.manualXtick else False
            getLabelAxisLabel = self.ax.get_xticklabels if self.manualXtick else False

            valueAxisTicker = self.ax.set_yticks
            valueAxisSpace = self.yspace if self.manualYtick else False
            getValueAxisLabel = self.ax.get_yticklabels if self.manualYtick else False

            labelTicker = self.ax.set_xticklabels
            axis = self.ax.yaxis
            figLimit = plt.xlim

        if labelAxisSpace:
            # Manually sets label axis
            labelAxisTicker(labelAxisSpace)
            labelTicker(self.tickLabel.content, rotation=self.tickAngle, ha=self.tickAlign,
                        fontsize=self.fontsize)
            for t, offset in zip( getLabelAxisLabel(), self.voffset ):
                if self.vertical is False:
                    t.set_x( offset )
                else:
                    t.set_y( offset )
        else:
            # Automatically generate label axis
            labelAxisTicker(self.globalBase+self.barwidth/2)
            labelTicker(self.tickLabel.content, rotation=self.tickAngle, ha=self.tickAlign,
                        fontsize=self.fontsize)

        if valueAxisSpace:
            # Manually sets value axis
            valueAxisTicker(valueAxisSpace)
            for t, offset in zip( getValueAxisLabel(), self.voffset ):
                if self.vertical is True:
                    t.set_x( offset )
                else:
                    t.set_y( offset )
        else:
            # Automatically generate label axis
            pass

        # Adjust fontsize as denoted
        for tick in axis.get_major_ticks():
            tick.label.set_fontsize(self.fontsize)

        # set label's vertical padding
        # self.ax.xaxis.labelpad=10.3

        LengthOfWholeBar = self.base[-1] + self.barwidth
        figLimit([-LengthOfWholeBar*self.FigSideMargin, LengthOfWholeBar*(1+self.FigSideMargin)])


class CBarPlotter(AbstractBarPlotter):
    """Draw clustered bar graph with grouped data or column-parsed data"""

    def __init__(self, **kwargs):
        AbstractBarPlotter.__init__(self, **kwargs)

    def draw(self, *argv, **kwargs):
        self.m_beforeEveryDraw(**kwargs)

        self.keyLen = keyLen = len(argv)
        datLen = len(argv[0].Y)

        # Interval between clustered bars: 40% of total width in a clustered group
        interClusterOffset = (self.barwidth*keyLen) * self.interCmargin
        self.base = np.arange(datLen) * interClusterOffset + self.baseOffset + self.base[-1]

        # Accumulate tick bases to global base
        self.globalBase = np.concatenate([self.globalBase, self.base])

        for i in range(keyLen):
            self.patch.append(self.ax.bar(self.base+i*self.barwidth, argv[i].Y, self.barwidth,
                                          color=argv[i].color, zorder=3, hatch=argv[i].hatch))
            if bool(argv[i].legend):
                self.legend.append(argv[i].legend)

    def m_finish(self):
        # set legend
        self.m_drawLegend(self.patch, self.legend);

        if self.manualXtick is True:
            # set xtick point and label
            self.ax.set_xticks(self.xspace)
            self.ax.set_xticklabels(self.tickLabel.content, rotation=self.tickAngle, ha=self.tickAlign)
        else:
            # set xtick point and label
            self.ax.set_xticks(self.globalBase+(self.barwidth*self.keyLen)/2)
            self.ax.set_xticklabels(self.tickLabel.content, rotation=self.tickAngle, ha=self.tickAlign)

        if self.manualYtick is True:
            self.ax.set_yticks(self.yspace)

        LengthOfWholeBar = self.globalBase[-1] + self.barwidth*self.keyLen
        plt.xlim([-LengthOfWholeBar*self.FigSideMargin, LengthOfWholeBar*(1+self.FigSideMargin)])


class CCBarPlotter(AbstractBarPlotter):
    cc_globalBase = np.array([])
    """Draw clustered*2 bar graph with grouped parsed data"""
    def __init__(self, **kwargs):
        AbstractBarPlotter.__init__(self, **kwargs)
    
    def m_setFigureStyle(self, **kwargs):
        # set overall figure styles
        if "groupmargin" in kwargs:
            self.BtwGroupMargin = kwargs["groupmargin"]
        if "barwidth" in kwargs:
            # barwidth can be assigned as a style over all bars
            self.barwidth = kwargs["barwidth"] 

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
        self.m_beforeEveryDraw(**kwargs)

        base = []
        globalBase = np.array([])

        # set margin proportional to the first data
        keyLen = argv[0].length
        datLen = len(argv[0].content[0].Y)

        # Interval between clustered bars: 40% of total width in a clustered group
        interClusterOffset = (self.barwidth * keyLen) * self.interCmargin
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
                                              color=elem.color, hatch=elem.hatch, zorder=3))
                if bool(elem.legend):
                    self.legend.append(elem.legend)

        # Accumulate tick bases to global base
        self.cc_globalBase = np.concatenate([self.cc_globalBase, globalBase])

    def m_finish(self):
        # set legend
        self.m_drawLegend(self.patch, self.legend);

        # set xtick point and label
        self.ax.set_xticks(self.cc_globalBase)
        self.ax.set_xticklabels(self.tickLabel, rotation=self.tickAngle)

        LengthOfWholeBar = self.cc_globalBase[-1] + self.barwidth*self.keyLen
        plt.xlim([-LengthOfWholeBar*self.FigSideMargin, LengthOfWholeBar*(1+self.FigSideMargin)])


class AbstractBoxPlotter(AbstractPlotter):
    patch = []
    legend = []
    globalBase = np.array([])
    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)
        # Initial base point
        self.base = [0.0]

        self.boxwidth = 1.0
        self.vertical = True

    def getGlobalBase(self):
        return self.globalBase

    def m_setFigureStyle(self, **kwargs):
        if "vertical" in kwargs:
            self.vertical = kwargs["vertical"]
        if "boxwidth" in kwargs:
            # boxwidth can be assigned as a style over all bars
            self.boxwidth = float(kwargs["boxwidth"])

    def m_beforeEveryDraw(self, **kwargs):
        # boxwidth can also be assigned to each different elem
        if "boxwidth" in kwargs:
            self.boxwidth = float(kwargs["boxwidth"])


class BoxPlotter(AbstractBoxPlotter):
    """Draw clustered bar graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractBoxPlotter.__init__(self, **kwargs)

    def draw(self, *argv, **kwargs):
        self.m_beforeEveryDraw()

        keyLen = len(argv)

        # Calculate global/local base
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

    def m_finish(self):
        # set legend
        self.m_drawLegend(self.patch, self.legend);

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
            self.ax.set_xlim([-LengthOfWholeBar*self.FigSideMargin, LengthOfWholeBar*(1+self.FigSideMargin)])
        else:
            self.ax.autoscale(enable=True, axis='x', tight=False)
            LengthOfWholeBar = self.globalBase[-1] + self.boxwidth
            self.ax.set_ylim([-LengthOfWholeBar*self.FigSideMargin, LengthOfWholeBar*(1+self.FigSideMargin)])


class CBoxPlotter(AbstractBoxPlotter):
    """Draw clustered bar graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractBoxPlotter.__init__(self, **kwargs)

    def draw(self, *argv, **kwargs):
        self.m_beforeEveryDraw()

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

    def m_finish(self):
        # set legend
        self.m_drawLegend(self.patch, self.legend);

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
            self.ax.set_xlim([-LengthOfWholeBar*self.FigSideMargin, LengthOfWholeBar*(1+self.FigSideMargin)])
        else:
            self.ax.autoscale(enable=True, axis='x', tight=False)
            LengthOfWholeBar = self.globalBase[-1] + self.boxwidth
            self.ax.set_ylim([-LengthOfWholeBar*self.FigSideMargin, LengthOfWholeBar*(1+self.FigSideMargin)])


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
