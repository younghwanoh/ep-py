#!/usr/bin/python
import csv
from sys import stdout

from tools import *

# ==== Function role ====
# Dump <<key, value>> pares from <<"value", "base_key">>
# if the keys are found in the specified "partial_key"

def dump(value, base_key, partial_key):
    writeLine = csv.writer(stdout, delimiter='\t')
    for k in range(len(base_key)):
        if base_key[k].find(partial_key) >= 0:
            writeLine.writerow([base_key[k]]+value[k])

# Front-end parser
class PatternParser:
    """Parse EP format data with some exclusive patterns"""
    def __init__(self, *argv, **kwargs):
        self.isParsedBefore = False
        self.keyParseType = None
        self.RAWdata = argv[0]

        tCheckArgsExists(kwargs, "arrange", "subtfromfirst")
        if kwargs["arrange"] is False:
            # The case that keys are denoted in files.
            self.rowParse()
        else:
            # The case that keys are denoted manually and must be clustered.
            subtract = None;
            if kwargs["subtfromfirst"] is True:
                subtract = kwargs["subtfromfirst"]

            self.cluster(subtract, kwargs["arrange"])

    def rowParse(self):
        """Parse col data with \n"""
        self.rowData = self.RAWdata.split("\n")

        # If final splitted character is EOF delete that void element
        if self.rowData[-1] == "":
            del self.rowData[-1]

        self.rowData = self.deleteCommentIn(self.rowData)

    def deleteCommentIn(self, target):
        """Subtool: delete comment line starting with #"""
        rowDataTemp = []
        for eachRow in target:
            if eachRow[0] != "#":
                rowDataTemp.append(eachRow)
        return rowDataTemp

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

    # ==== Fimctopm role ====
    # After "cluster", summing up each start/end data with key
    def sumWithRegionKey(self, keys, **kwargs):
        if "prefix" in kwargs:
            keys = [kwargs["prefix"] + i for i in keys]

        _sum = []
        for k in range(0, len(keys)):
            _tmp = 0
            for i in range(0, len(self.datList[self.keyList.index(keys[k]+" end")])):
                _tmp += self.datList[self.keyList.index(keys[k]+" end")][i] \
                        - self.datList[self.keyList.index(keys[k]+" start")][i]
            _sum.append(_tmp)

        if "update" in kwargs:
            if kwargs["get"] == True:
                return _sum

        self.datList = _sum

    # ==== Fimctopm role ====
    # After "cluster", summing up each data with key
    def sumWithKey(self, keys):
        _sum = []
        for k in range(0, len(keys)):
            _tmp = 0
            for i in range(0, len(self.datList[self.keyList.index(keys[k])])):
                _tmp += self.datList[self.keyList.index(keys[k])][i]
            _sum.append(_tmp)

        if "update" in kwargs:
            if kwargs["get"] == True:
                return _sum

        self.datList = _sum

    # ==== Function role ====
    # Cluster raw spread data to each group (only for the data which denotes special key)
    # e.g.
    # before
    #      data 1: 2
    #      data 2: 3
    #      data 1: 1
    # after
    #      data 1: 2,1 (clustered)
    #      data 2: 3
    #
    # ==== Argument specification ====
    # initial: all values are subtracted by initial
    #          if "initial" is None, first line's value is used for "initial"
    # key: key list to customly parse (or clustered)
    def cluster(self, initial, key):
        text = self.RAWdata.split("\n")

        # subtract all data to initial 0 row's data if flag is set
        if bool(initial) == True:
            initial = text[0].split(": ")[1]

        value = []
        for k in range(len(key)):
            value.append([])
            for i in range(len(text)):
                raw = text[i].split(": ")
                if raw[0] == key[k]:
                    value[k].append(float(raw[1]) - float(initial))

        # dump(value, key, "GPU memcp")

        self.keyList = key
        self.datList = value

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
    # if no arguments are specified, whole array is returned
    def getDataArr(self, *argv, **kwargs):
        """Get data arrays from PatternParser"""
        tCheckArgsExists(kwargs, "copy", "opt")

        # copy: pass reference, or not: pass copied value
        CpyOrNot = lambda x: list(x) if kwargs["copy"] is True else x
        # Transpose for column data or not
        TransOrNot = lambda x: tTranspose(x) if kwargs["opt"] is "col" else x

        if len(argv) == 0:
            return [CpyOrNot(i) for i in self.datList]
        else:
            temp = TransOrNot(self.datList)
            return CpyOrNot(temp[argv[0]])

    # arguments: target index, copy=boolean
    def getKeyArr(self, *argv, **kwargs):
        """Get key arrays from PatternParser"""
        tCheckArgsExists(kwargs, "copy")

        # copy: pass reference, or not: pass copied value
        CpyOrNot = lambda x: list(x) if kwargs["copy"] is True else x

        if len(argv) == 0:
            return [CpyOrNot(i) for i in self.keyList]
        else:
            return CpyOrNot(self.keyList[argv[0]])

