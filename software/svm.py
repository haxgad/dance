# support vector machine

from sklearn import svm
from preprocess_data import split_feature_class_as_float_array

def run_svm(training_set, test_set):
    training_features = []
    training_class = []
    test_features = []
    test_class = []
    split_feature_class_as_float_array(training_set, training_features, training_class)
    split_feature_class_as_float_array(test_set, test_features, test_class)

    clf = svm.SVC(gamma=0.01, C=10.)
    clf.fit(training_features, training_class) 
    prediction = clf.predict(test_features)
    correct = 0
    for i in range(len(prediction)):
        if prediction[i] == test_class[i]:
            correct += 1
    return correct/len(test_class)