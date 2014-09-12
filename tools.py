#!/usr/bin/python

import numpy as np

# ad-hoc tools
# Transpose matrix and make list other than tuple
def tTranspose(arr):
    result = zip(*arr)
    result = [list(i) for i in result]
    return result

def tPopRow(arr, idx):
    temp = list(arr)
    popDat = temp.pop(idx)
    return temp, popDat

def tPopCol(arr, idx):
    temp = tTranspose(arr)
    popDat = temp.pop(idx)
    temp = tTranspose(temp)
    return temp, popDat

def tRead(inFile):
    with open(inFile) as inputFile:
        text = inputFile.read()
    return text

def tMergeCrossSpace(val, func):
    space = range(len(val)*2-1)[1::2]
    for idx in space:
        val.insert(idx, func(val, idx))
    return val

def tSetLegend(tag, *argv):
    for i in range(len(argv)):
        argv[i].setLegend(tag[i])

def tCheckArgsExists(t_keys, *argv, **kwargs):
    """Checking directory arguments are exists and set values on each index"""
    for i, key in enumerate(argv):
        if "ifnot" in kwargs:
            t_keys[key] = kwargs["ifnot"][i][0] \
                        = t_keys[key] if key in t_keys else kwargs["ifnot"][i][0]
            # t_keys[key] \
        else:
            t_keys[key] = t_keys[key] if key in t_keys else False

def tIsfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Group class: grouping correlated data and its configuration
class Group:
    """Group data to plot each correlated data"""
    def __init__(self, *argv, **kwargs):
        # Group of grouped data if input is instanceof "Group"
        isMultiDim = True;
        for i in argv:
            if isinstance(i, Group) is False:
                isMultiDim = False
                break;
        if isMultiDim is True:
            self.content = argv
            self.length = len(argv)
            return

        # Group raw data with new copy
        argv=list(argv)
        PP = argv.pop(0)

        # set default attributes
        self.color = "black"
        self.face = "black"
        self.marker = "o"
        self.hatch = ""
        self.keyX = None
        self.keyY = None

        tCheckArgsExists(kwargs, "region")
        if "face" in kwargs:
            self.face = kwargs["face"]
        if "color" in kwargs:
            self.color = kwargs["color"]
        if "marker" in kwargs:
            self.marker = kwargs["marker"]
        if "hatch" in kwargs:
            self.hatch = kwargs["hatch"]

        if kwargs["region"] is True:
            # Group data with region surfix
            self.groupDataWithRegionKey(PP, argv)
        elif len(argv) == 1:
            # Single data array (for bar)
            if type(argv[0]) is str:
                self.keyY = argv[0]
                idx = PP.keyList.index(argv[0])
                self.Y = PP.datList[idx] 
            elif (type(argv[0]) is list) | (type(argv[0]) is np.ndarray):
                self.Y = argv[0]
            else:
                print("Group.dat - Argument type is wrong ! Must be str or list.")
        elif len(argv) == 2:
            # Double(X, Y) data array
            # Group X
            if type(argv[0]) is str:
                self.keyX = argv[0]
                idxX = PP.keyList.index(argv[0])
                self.X = PP.datList[idxX] 
            elif (type(argv[0]) is list) | (type(argv[0]) is np.ndarray):
                self.X = argv[0]
            else:
                print("Group.X - Argument type is wrong ! Must be str or list.")

            # Group Y
            if type(argv[1]) is str:
                self.keyY = argv[1]
                idxY = PP.keyList.index(argv[1])
                self.Y = PP.datList[idxY]
            elif (type(argv[1]) is list) | (type(argv[0]) is np.ndarray):
                self.Y = argv[1]
            else:
                print("Group.Y - Argument type is wrong ! Must be str or list.")
        else:
            # Over-dimensional data array
            print("Group::init - Multi-dimensional data isn't supported yet")

        # self.legend = self.keyY if type(self.keyY) is str else None
        self.legend = []

    def setLegend(self, string):
        self.legend = string

    def groupDataWithRegionKey(self, PP, argv):
        # Find Start Point
        self.keyX = argv[0] + " start"
        idxX = PP.keyList.index(self.keyX)
        self.X = PP.datList[idxX] 

        # Find End Point
        self.keyY = argv[0] + " end"
        idxY = PP.keyList.index(self.keyY)
        self.Y = PP.datList[idxY]
        


# Label class: grouping correlated data and its configuration
class TickLabel:
    """Group data to plot each correlated data"""
    def __init__(self, PP, *argv, **kwargs):
        # cut out if label has floating point
        toint = lambda x: int(x) if type(x) is float else x
        if type(argv[0]) is str:
            self.key = argv[0]
            idx = PP.keyList.index(argv[0])
            self.content = [toint(i) for i in PP.datList[idx]]
        elif (type(argv[0]) is list) | (type(argv[0]) is np.ndarray):
            self.content = [toint(i) for i in argv[0]]
        elif isinstance(argv[0], Group):
            print("Type Group")
        else:
            print("TickLabel::init - Unexpected argument type")
