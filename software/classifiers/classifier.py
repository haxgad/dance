from ann import run_ann, k_fold_cross_validate
from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
import numpy as np
import pandas
import csv

def run_perceptron(X_train, X_test, y_train, y_test):
    clf = Perceptron(tol=1e-3, random_state=0)
    clf.fit(X_train, y_train) 
    prediction = clf.predict(X_test)
    accuracy = accuracy_score(prediction, y_test)
    return prediction, accuracy


def run_knn(X_train, X_test, y_train, y_test, k):
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train) 
    prediction = clf.predict(X_test)
    accuracy = accuracy_score(prediction, y_test)
    return prediction, accuracy


def run_svm(X_train, X_test, y_train, y_test):
    clf = svm.SVC(gamma=0.01, C=10.)
    clf.fit(X_train, y_train) 
    prediction = clf.predict(X_test)
    accuracy = accuracy_score(prediction, y_test)
    return prediction, accuracy


# file_name = 'bezdekIris'
# file_name = 'pulsar_stars'
# file_name = 'heart'
file_name = 'hard'
file_path = '../test_data/' + file_name + '.csv'
dataframe = pandas.read_csv(file_path, header=None)
dataset = dataframe.values
X = dataset[:,0:len(dataset[0])-1].astype(float)
y = dataset[:,len(dataset[0])-1].astype(float)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 93.3% for bezdekIris
# about 65% for heart
# about 97% for pulsar_stars
# prediction, accuracy = run_knn(X_train, X_test, y_train, y_test, k=5)

# about 93.3% for bezdekIris
# 50% - 60% for heart
# about 97% for pulsar_stars, obviously slower than knn
# prediction, accuracy = run_svm(X_train, X_test, y_train, y_test)

# over 96.6% for bezdekIris
# does not work for heart
# over 98% for pulsar_stars, training is slow with large dataset, can use saved trained model
prediction, accuracy = run_ann(X_train, X_test, y_train, y_test, file_name+'_model')
k_fold_cross_validate(X, y, file_name+'_model')

# 50% - 80% for bezdekIris
# does not work for heart
# about 97% for pulsar_stars
# prediction, accuracy = run_perceptron(X_train, X_test, y_train, y_test)


print(confusion_matrix(y_test, prediction))
print("Accuracy: %.2f%%" % (accuracy*100))
