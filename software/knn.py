# k nearest neighbors

import math
import numpy
import operator

def euclidean_distance(point1, point2):
    distance = 0
    for i in range(len(point1)-1):
        distance += pow(point1[i] - point2[i], 2)
    return math.sqrt(distance)
    
def kNN_algo(training_set, test_point, k):
    prediction = {}
    distance = {}
    # compute euclidean distance between the ith data point and each training point
    for j in range(len(training_set)):
        distance[j] = euclidean_distance(test_point, training_set[j])
    # sort the training data according to the distance 
    distance = sorted(distance.items(), key=operator.itemgetter(1))
    # find the class of the k nearest neighbors
    # x is the xth point
    # distance[x][0] is the index of the point in the list of training set
    # assume the last value is the class
    for x in range(k):
        class_of_point = int(training_set[distance[x][0]][len(training_set[distance[x][0]])-1])
        if class_of_point in prediction:  
            prediction[class_of_point] += 1
        else:
            prediction[class_of_point] = 1
    # sort the prediction dictionary according the appearance 
    prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
    # return the class which appeares the most times in the k nearest neighbors
    return prediction[0][0]
    
def run_knn(training_set, test_set, k):
    correct = 0
    for i in range(len(test_set)):
        prediction = kNN_algo(training_set, test_set[i], k)
        if prediction == test_set[i][len(test_set[i])-1]:
            correct += 1
    return correct/len(test_set)         


    