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
    
k = 10
trainingSet = []
testSet = []
correct_prediction = 0
handleDataset('C:\\Users\\xiejihui\\Desktop\\3002\\test_data\\heart.csv', 0.75, trainingSet, testSet)
for i in range(len(testSet)):
    distance = {}
    class_one = 0
    prediction = 0
    for j in range(len(trainingSet)):
        distance[j] = euclideanDistance(testSet[i], trainingSet[j])
    distance= sorted(distance.items(), key=operator.itemgetter(1))
    
    for x in range(k):
        n = trainingSet[distance[x][0]][len(trainingSet[distance[x][0]])-1]
        if int(n) == 1:  
            class_one += 1
 
    if class_one > k/2:
        prediction = 1
    if prediction == int(testSet[i][len(testSet[i])-1]):
        correct_prediction += 1

print(correct_prediction/len(testSet))          


    