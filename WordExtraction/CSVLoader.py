import csv

class CSVLoader:
    def __init__(self, csvFileName, newLine=''):
        self.csvFileName = csvFileName
        self.newLine = newLine
        self.provinsiArray = ""

    def __openFile(self):
        with open(self.csvFileName, newline='') as f:
            reader = csv.reader(f)
            self.provinsiArray = list(reader)

    def getCSVArray(self):
        self.__openFile()
        return self.provinsiArray