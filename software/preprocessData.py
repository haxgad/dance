import csv
import random
import numpy as np

def processDataset(filename, split, trainingSet=[], testSet=[]):
    with open(filename, 'r') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for i in range(1, len(dataset)):
            if random.random() < split:
                trainingSet.append(dataset[i])
            else:
                testSet.append(dataset[i])

def splitFeatureAndClass(set, featureSet, classSet):
    for i in len(set):

