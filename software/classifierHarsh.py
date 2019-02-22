from ann import run_ann
from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn import tree

import numpy as np
import pandas
import csv


#adaptive boosting classifier
#It combines multiple classifiers to increase the accuracy of classifiers. 
#AdaBoost is an iterative ensemble method. AdaBoost classifier builds a strong classifier by combining multiple poorly performing classifiers so that you will get high accuracy strong classifier. 

def run_AdaBoost(X_train, X_test, y_train, y_test):
    clf=AdaBoostClassifier(n_estimators=50, learning_rate=1)
    clf.fit(X_train,y_train)
    y_pred=clf.predict(X_test)
    return y_pred
                         
def run_random_forest(X_train, X_test, y_train, y_test):
    clf=RandomForestClassifier(n_estimators=200)
    clf.fit(X_train,y_train)
    y_pred=clf.predict(X_test)
    return y_pred

def run_decision_tree(X_train, X_test, y_train, y_test):
    clf=tree.DecisionTreeClassifier()
    clf.fit(X_train,y_train)
    y_pred=clf.predict(X_test)
    return y_pred

file_name = 'winequality-white'
file_path = 'test_data/' + file_name + '.csv'
dataframe = pandas.read_csv(file_path, header=None)
dataset = dataframe.values
X = dataset[:,0:len(dataset[0])-1].astype(float)
y = dataset[:,len(dataset[0])-1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

prediction=run_random_forest(X_train, X_test, y_train, y_test)

#prediction=run_decision_tree(X_train, X_test, y_train, y_test)

#prediction=run_AdaBoost(X_train, X_test, y_train, y_test)

matrix = confusion_matrix(y_test, prediction)
print(matrix)

correct = 0
for i in range(len(matrix)):
    correct += matrix[i][i]
print("Accuracy: ", correct/len(y_test))
