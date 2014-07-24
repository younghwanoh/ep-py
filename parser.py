#!/usr/bin/python
from tools import *

# Front-end parser
class PatternParser:
    """Parse EP format data with some exclusive patterns"""
    def __init__(self, *argv):
        self.isParsedBefore = False
        self.keyParseType = None

        self.RAWdata = argv[0]
        self.rowParse()

    def deleteCommentIn(self, target):
        """Subtool: delete comment line starting with #"""
        rowDataTemp = []
        for eachRow in target:
            if eachRow[0] != "#":
                rowDataTemp.append(eachRow)
        return rowDataTemp

    def rowParse(self):
        """Parse col data with \n"""
        self.rowData = self.RAWdata.split("\n")

        # If final splitted character is EOF delete that void element
        if self.rowData[-1] == "":
            del self.rowData[-1]

        self.rowData = self.deleteCommentIn(self.rowData)

    def colParse(self, delimiter):
        """Parse col data with delimiter"""
        self.datList = []
        for eachRow in self.rowData:
            self.datList.append(eachRow.split(delimiter))

    def ParseWith(self, delimiter):
        """Parse data with delimiter"""
        self.isParsedBefore = True
        self.colParse(delimiter)

        # Lazy key parse for the denoted row/col
        if self.keyParseType is "row":
            self.datList, self.keyList = tPopRow(self.datList, self.keyLineNum)
            self.datList = tTranspose(self.datList)
        elif self.keyParseType is "col":
            self.datList, self.keyList = tPopCol(self.datList, self.keyLineNum)

        # Data type change: string to float
        toFloat = lambda x: float(x) if tIsfloat(x) == True else x
        for i, curDat in enumerate(self.datList):
            self.datList[i] = [toFloat(k) for k in curDat]

    # Pick specially denoted data to map it to title or legendsi
    # This method should be used after "ParseWith" is called
    # 1) PickKeyWith(SpecialKey) : Find leftmost matched special key from data
    # 2) PickKeyWith("row") : with row 0
    # 3) PickKeyWith("col") : with column 0
    # 4) PickKeyWith("row" or "col", number): column or row wuith denoted number

    def PickKeyWith(self, *argv):
        """PickKeyWith treats the data with special keys"""
        if self.isParsedBefore is True:
            print("Alert: You must pick key first before parsing data!"), exit()
        self.isParsedBefore = False

        # Parse the denoted row/col key
        if argv[0] is "row":
            self.keyParseType = "row"
            self.keyLineNum = 0 if len(argv) == 1 else argv[1]
        elif argv[0] is "col":
            self.keyParseType = "col"
            self.keyLineNum = 0 if len(argv) == 1 else argv[1]

        # Parse the special key
        elif type(argv[0]) is str:
            self.keyParseType = "custom"
            delimiter = argv[0]
            self.keyList = []
            for i in range(0, len(self.rowData)):
                keyAndData = self.rowData[i].split(delimiter, 1)
                self.keyList.append(keyAndData[0])
                self.rowData[i] = keyAndData[1];
        else:
            print("PP::PickKeyWith - Argument type is wrong! Must be string."), exit()

    # Normalize to data denoted by a special key
    # 1) datNormTo("normalizeToThisKey")
    # 2) datNormTo("normalizeToThisKey", skip="skipThisKey")
    #
    # ==== Argument specification ====
    # where: target key to normalize data. (normalized to "where")
    # opt  : "speedup": x divided by "where" (default)
    #        "exetime": "where" divided by x
    # skip : skip nomarlization fpr this key
    def datNormTo(self, where, **kwargs):
        """Normalize data to spcified row or col"""
        # calc = lambda x,y: x/y
        if "opt" in kwargs:
            calc = lambda x,y: x/y if kwargs["opt"] == "exetime" else y/x

        if type(where) is str:
            idx = self.keyList.index(where)
            normArr = self.datList[idx]
            for i, datArr in enumerate(self.datList):
                if type(datArr[0]) is float:
                    self.datList[i] = [ calc(dat, norm) for dat, norm in zip(datArr, normArr)]
        else:
            print("PP::datNormTo - First argument must be key string."), exit()

    # arguments: target index, opt="row"|"col", copy=boolean
    def getDataArr(self, *argv, **kwargs):
        """Get data arrays from PatternParser"""
        tCheckArgsExists(kwargs, "copy", "opt")

        # copy: pass reference, or not: pass copied value
        CpyOrNot = lambda x: list(x) if bool(kwargs["copy"]) is True else x
        # Transpose for column data or not
        TransOrNot = lambda x: tTranspose(x) if kwargs["opt"] is "col" else x

        if len(argv) == 0:
            return CpyOrNot(self.datList)
        else:
            temp = TransOrNot(self.datList)
            return temp[argv[0]]

    # arguments: target index, copy=boolean
    def getKeyArr(self, *argv, **kwargs):
        """Get key arrays from PatternParser"""
        tCheckArgsExists(kwargs, "copy")

        # copy: pass reference, or not: pass copied value
        CpyOrNot = lambda x: list(x) if kwargs["copy"] is True else x

        if len(argv) == 0:
            return CpyOrNot(self.keyList)
        else:
            return self.keyList[argv[0]]

