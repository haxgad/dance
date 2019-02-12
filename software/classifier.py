from knn import run_knn
from svm import run_svm
from preprocessData import processDataset

dataFilePath = "test_data/bezdekIris.csv"
splitRatio = 0.75  #proportion of training sets
trainingSet = []
testSet = []
processDataset(dataFilePath, splitRatio, trainingSet, testSet)

# accuracy = run_knn(trainingSet, testSet, k=5)
accuracy = run_svm(trainingSet, testSet)
print(accuracy)