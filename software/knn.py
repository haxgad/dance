import csv
import math
import numpy
import random
import operator

def euclideanDistance(point1, point2):
    distance = 0
    for i in range(len(point1)-1):
        distance += pow((float(point1[i]) - float(point2[i])), 2)
    return math.sqrt(distance)

def handleDataset(filename, split, trainingSet=[], testSet=[]):
    with open(filename, 'r') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for i in range(1, len(dataset)):
            if random.random() < split:
                trainingSet.append(dataset[i])
            else:
                testSet.append(dataset[i])
    
def kNN_algo(trainingSet, testPoint):
    prediction = {}
    distance = {}
    # compute euclidean distance between the ith data point and each training point
    for j in range(len(trainingSet)):
        distance[j] = euclideanDistance(testPoint, trainingSet[j])
    # sort the training data according to the distance 
    distance = sorted(distance.items(), key=operator.itemgetter(1))
    # find the class of the k nearest neighbors
    # x is the xth point
    # distance[x][0] is the index of the point in the list of trainingSet
    # assume the last value is the class
    for x in range(k):
        classOfPoint = int(trainingSet[distance[x][0]][len(trainingSet[distance[x][0]])-1])
        if classOfPoint in prediction:  
            prediction[classOfPoint] += 1
        else:
            prediction[classOfPoint] = 1
    # sort the prediction dictionary according the appearance 
    prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
    # return the class which appeares the most times in the k nearest neighbors
    return prediction[0][0]
    


k = 5
filePath = 'C:\\Users\\xiejihui\\Desktop\\3002\\test_data\\heart.csv'
splitRatio = 0.75  #proportion of training sets
trainingSet = []
testSet = []

handleDataset(filePath, splitRatio, trainingSet, testSet)

correct_prediction = 0
for i in range(len(testSet)):
    prediction = kNN_algo(trainingSet, testSet[i])
    if prediction == int(testSet[i][len(testSet[i])-1]):
        correct_prediction += 1

print(correct_prediction/len(testSet))          


    