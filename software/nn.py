from ann import run_ann
from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import pandas
import csv


def run_perceptron(X_train, X_test, y_train, y_test):
    clf = Perceptron(tol=1e-3, random_state=0)
    clf.fit(X_train, y_train)
    return clf.score(X_test, y_test)


def run_knn(X_train, X_test, y_train, y_test, k):
    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(X_train, y_train) 
    prediction = neigh.predict(X_test)

    correct = 0
    for i in range(len(y_test)):
        # prediction = kNN_algo(training_set, test_set[i], k)
        # if prediction == test_set[i][len(test_set[i])-1]:
        if prediction[i] == y_test[i]:
            correct += 1
    return correct/len(y_test)       


def run_svm(X_train, X_test, y_train, y_test):
    clf = svm.SVC(gamma=0.01, C=10.)
    clf.fit(X_train, y_train) 
    prediction = clf.predict(X_test)
    correct = 0
    for i in range(len(prediction)):
        if prediction[i] == y_test[i]:
            correct += 1
    return correct/len(y_test)


def get_data_set(file_path):
	dataframe = pandas.read_csv(file_path, header=None)
	dataset = dataframe.values
	X = dataset[:,0:len(dataset[0])-1].astype(float)
	y = dataset[:,len(dataset[0])-1]
        return X, y

file_path = "test_data/bezdekIris.csv"
X, y = get_data_set(file_path)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

y_train = np.asarray(y_train).ravel().astype(int)
y_test = np.asarray(y_test).ravel().astype(int)

# accuracy = run_knn(X_train, X_test, y_train, y_test, k=5)
# accuracy = run_svm(X_train, X_test, y_train, y_test)
accuracy = run_ann(X_train, X_test, y_train, y_test, "pulsar_stars_model")
# accuracy = run_perceptron(X_train, X_test, y_train, y_test)
print(accuracy)
