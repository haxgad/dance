from ann import run_ann, k_fold_validate
from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas
import csv

def run_perceptron(X_train, X_test, y_train, y_test):
    clf = Perceptron(tol=1e-3, random_state=0)
    clf.fit(X_train, y_train) 
    return clf.predict(X_test)


def run_knn(X_train, X_test, y_train, y_test, k):
    neigh = KNeighborsClassifier(n_neighbors=k)
    neigh.fit(X_train, y_train) 
    return neigh.predict(X_test)


def run_svm(X_train, X_test, y_train, y_test):
    clf = svm.SVC(gamma=0.01, C=10.)
    clf.fit(X_train, y_train) 
    return clf.predict(X_test)

file_name = 'winequality-white'
# file_name = 'bezdekIris'
# file_name = 'ph-data'
# file_name = 'development-index'
file_path = 'test_data/' + file_name + '.csv'
dataframe = pandas.read_csv(file_path, header=None)
dataset = dataframe.values
X = dataset[:,0:len(dataset[0])-1].astype(float)
y = dataset[:,len(dataset[0])-1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 93.3% for bezdekIris
# about 65% for heart
# about 97% for pulsar_stars
# prediction = run_knn(X_train, X_test, y_train, y_test, k=5)

# about 93.3% for bezdekIris
# 50% - 60% for heart
# about 97% for pulsar_stars, obviously slower than knn
# prediction = run_svm(X_train, X_test, y_train, y_test)

# over 96.6% for bezdekIris
# does not work for heart
# over 98% for pulsar_stars, training is slow with large dataset, can use saved trained model
prediction = run_ann(X_train, X_test, y_train, y_test, file_name+'_model')
k_fold_validate(X, y, file_name+'_model')
# 50% - 80% for bezdekIris
# does not work for heart
# about 97% for pulsar_stars
# prediction = run_perceptron(X_train, X_test, y_train, y_test)


matrix = confusion_matrix(y_test, prediction)
print(matrix)
correct = 0
for i in range(len(matrix)):
    correct += matrix[i][i]
print("Accuracy: ", correct/len(y_test))
