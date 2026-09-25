import csv

DATA_FOLDER = "data/"

def readFitnessCSV(filename):
    path = DATA_FOLDER + filename
    with open(path, "r") as f:
        data = csv.DictReader(f)
        for row in data:
            print(row)