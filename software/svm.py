from sklearn import svm
from preprocessData import processDataset

filePath = 'C:\\Users\\xiejihui\\Desktop\\3002\\test_data\\pulsar_stars.csv'
splitRatio = 0.75  #proportion of training sets
trainingSet = []
testSet = []
processDataset(filePath, splitRatio, trainingSet, testSet)

clf = svm.SVC(gamma=0.001, C=100.)
print(clf)