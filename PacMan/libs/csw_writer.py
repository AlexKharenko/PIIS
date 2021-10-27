import csv

class CSVWriter:
    def __init__(self, path='./') -> None:
        self.path = path
        self.file = open(self.path, 'a', encoding='UTF8', newline='')   
        self.writer = csv.writer(self.file)
        self.header = ['Win', 'Time', 'Score', 'Algorythm']

    def writeData(self, data):
        file = open(self.path)
        reader = csv.reader(file)   
        if len(list(reader)) == 0:
            self.writer.writerow(self.header)
        self.writer.writerow(data)
