import csv
import random
import numpy as np

def processDataset(filename, split, trainingSet=[], testSet=[]):
    with open(filename, 'r') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for i in range(1, len(dataset)):
            dataset[i] = [float(j) for j in dataset[i]]
            if random.random() < split:
                trainingSet.append(dataset[i])
            else:
                testSet.append(dataset[i])

def splitFeatureAndClass(set, featureSet, classSet):
    for i in range(len(set)):
        featureSet.append(set[i][0:len(set[i])-1])
        classSet.append(set[i][len(set[i])-1])
    featureSet = np.asarray(featureSet)
    classSet = np.asarray(classSet)