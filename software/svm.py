# support vector machine

from sklearn import svm
from preprocessData import splitFeatureAndClass

def run_svm(trainingSet, testSet):
    trainingFeatures = []
    trainingClass = []
    testFeatures = []
    testClass = []
    splitFeatureAndClass(trainingSet, trainingFeatures, trainingClass)
    splitFeatureAndClass(testSet, testFeatures, testClass)

    clf = svm.SVC(gamma=0.01, C=10.)
    clf.fit(trainingFeatures, trainingClass) 
    prediction = clf.predict(testFeatures)
    correctPrediction = 0
    for i in range(len(prediction)):
        if prediction[i] == testClass[i]:
            correctPrediction += 1
    return correctPrediction/len(testClass)