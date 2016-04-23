#!/usr/bin/python

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(round(y/fraction, 2))
    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'

def saveToPdf(output):
    pp = PdfPages(output)
    plt.savefig(pp, format='pdf')
    pp.close()
    plt.close()

def minRuler(array, step):
    minimum = min(array)
    print " - min: ", minimum
    offset = minimum % step
    return minimum - offset

def maxRuler(array, step):
    maximum = max(array)
    print " - max: ", maximum
    offset = maximum % step
    return maximum - offset + step

step = 0.005
file_list = ["W_fc1.dat", "W_fc2.dat", "W_conv1.dat", "W_conv2.dat"]

for target in file_list:
    print "Target: ", target
    with open("dat/flat-dots/%s" % target) as text:
        x = np.float32(text.read().rstrip("\n").split("\n"))
    n, bins, patches = plt.hist(x, bins=np.arange(minRuler(x,step), maxRuler(x,step), step), alpha=0.75, facecolor="green")

    fraction = float(len(x)) / 100
    formatter = FuncFormatter(to_percent)
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.grid(True)

    saveToPdf("%s.pdf" % target.split(".")[0])