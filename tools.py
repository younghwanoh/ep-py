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

# Group class: grouping correlated data and its configuration
class Group:
    """Group data to plot each correlated data"""
    def __init__(self, PP, *argv, **kwargs):
        # set default attributes
        self.color = "black"
        self.marker = "o"
        self.keyX = None
        self.keyY = None

        if "color" in kwargs:
            self.color = kwargs["color"]
        if "marker" in kwargs:
            self.marker = kwargs["marker"]

        if len(argv) == 1:
            # Single data array
            print("Single data array")
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

        self.legend = self.keyY if type(self.keyY) is str else "Noname"

    def setLegend(self, string):
        self.legend = string
