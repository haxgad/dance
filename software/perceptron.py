# Perceptron Learning Algorithm

from sklearn.datasets import load_digits
from sklearn.linear_model import Perceptron
from preprocess_data import split_feature_class_as_float_array

def run_perceptron(training_set, test_set):
    training_feature = []
    training_class = []
    test_feature = []
    test_class = []
    split_feature_class_as_float_array(training_set, training_feature, training_class)
    split_feature_class_as_float_array(test_set, test_feature, test_class)

    clf = Perceptron(tol=1e-3, random_state=0)
    clf.fit(training_feature, training_class)
    return clf.score(training_feature, training_class)


