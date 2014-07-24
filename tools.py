#!/usr/bin/python

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
    temp = transpose(arr)
    popDat = temp.pop(idx)
    temp = transpose(temp)
    return temp, popDat

def tRead(inFile):
    with open(inFile) as inputFile:
        text = inputFile.read()
    return text

def tCheckArgsExists(kwargs, *argv):
    """Checking directory arguments are exists and set values on each index"""
    for key in argv:
        kwargs[key] = kwargs[key] if key in kwargs else False

def tIsfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Group class: grouping correlated data and its configuration
class Group:
    """Group data to plot each correlated data"""
    def __init__(self, PP, *argv, **kwargs):
        # set default attributes
        self.color = "black"
        self.marker = "o"
        self.hatch = ""
        self.keyX = None
        self.keyY = None

        if "color" in kwargs:
            self.color = kwargs["color"]
        if "marker" in kwargs:
            self.marker = kwargs["marker"]
        if "hatch" in kwargs:
            self.hatch = kwargs["hatch"]

        if len(argv) == 1:
            # Single data array (for bar)
            if type(argv[0]) is str:
                self.keyY = argv[0]
                idx = PP.keyList.index(argv[0])
                self.Y = PP.datList[idx] 
            elif type(argv[0]) is list:
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
            elif type(argv[0]) is list:
                self.X = argv[0]
            else:
                print("Group.X - Argument type is wrong ! Must be str or list.")

            # Group Y
            if type(argv[1]) is str:
                self.keyY = argv[1]
                idxY = PP.keyList.index(argv[1])
                self.Y = PP.datList[idxY]
            elif type(argv[1]) is list:
                self.Y = argv[1]
            else:
                print("Group.Y - Argument type is wrong ! Must be str or list.")
        else:
            # Over-dimensional data array
            print("Group::init - Multi-dimensional data isn't supported yet")

        self.legend = self.keyY if type(self.keyY) is str else None

    def setLegend(self, string):
        self.legend = string

class GGroup:
    """Group already grouped data to plot ClusteredClustered Bar"""
    def __init__(self, *argv, **kwargs):
        for i in argv:
            if isinstance(i, Group) == False:
                print("GGroup::init - Wrong argument type. Group must be assigned."), exit()

        self.group = argv

# Label class: grouping correlated data and its configuration
class TickLabel:
    """Group data to plot each correlated data"""
    def __init__(self, PP, *argv, **kwargs):
        self.rotate = 0
        if "rotate" in kwargs:
            self.rotate = kwargs["rotate"]

        # cut out if label has floating point
        toint = lambda x: int(x) if type(x) is float else x
        if type(argv[0]) is str:
            self.key = argv[0]
            idx = PP.keyList.index(argv[0])
            self.content = [toint(i) for i in PP.datList[idx]]
        elif type(argv[0]) is list:
            self.content = [toint(i) for i in argv[0]]
        elif isinstance(argv[0], Group):
            print("Type Group")
        else:
            print("TickLabel::init - Unexpected argument type")
