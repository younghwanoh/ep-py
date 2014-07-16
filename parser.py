#!/usr/bin/python
from tools import transpose
from tools import popRow
from tools import popCol

# Front-end parser
class PatternParser:
    """Parse EP format data with some exclusive patterns"""
    def __init__(self, *argv):
        self.RAWdata = argv[0]
        self.rowParse()

    def rowParse(self):
        # Parse row data with "\n"
        self.rowData = self.RAWdata.split("\n")

        # If final splitted character is EOF delete that void element
        if self.rowData[-1] == "":
            del self.rowData[-1]

        # Delete comment line starting with "#"
        rowDataTemp = []
        for eachRow in self.rowData:
            if eachRow[0] != "#":
                rowDataTemp.append(eachRow)
        self.rowData = rowDataTemp

    def colParse(self, delimiter):
        self.datList = []
        for eachRow in self.rowData:
            self.datList.append(eachRow.split(delimiter))

    def ParseWith(self, delimiter):
        self.colParse(delimiter)
        if self.keyParseType is "row":
            self.datList, self.keyList = popRow(self.datList, self.keyLineNum)
            self.datList = transpose(self.datList)
        elif self.keyParseType is "col":
            self.datList, self.keyList = popCol(self.datList, self.keyLineNum)

    # Pick specially denoted data to map it to title or legendsi
    # This method should be used after "ParseWith" is called
    # 1) PickKeyWith(SpecialKey) : Find leftmost matched special key from data
    # 2) PickKeyWith("row") : with row 0
    # 3) PickKeyWith("col") : with column 0
    # 4) PickKeyWith("row" or "col", number): column or row wuith denoted number
    def PickKeyWith(self, *argv):
        """PickKeyWith treats the data with special keys"""

        if argv[0] is "row":
            # parse key with row ...
            self.keyParseType = "row"
            self.keyLineNum = 0 if len(argv) == 1 else argv[1]

        elif argv[0] is "col":
            # parse key with col ...
            self.keyParseType = "col"
            self.keyLineNum = 0 if len(argv) == 1 else argv[1]

        elif type(argv[0]) is str:
            # parse key with special key
            self.keyParseType = "custom"
            delimiter = argv[0]
            self.keyList = []
            for i in range(0, len(self.rowData)):
                keyAndData = self.rowData[i].split(delimiter, 1)
                self.keyList.append(keyAndData[0])
                self.rowData[i] = keyAndData[1];
        else:
            print("PP::PickKeyWith - Argument type is wrong! Must be string.")
            exit()
