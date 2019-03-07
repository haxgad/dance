from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn import tree

import numpy as np
import pandas
import csv



#wine-quality headers 

# fixed.acidity
# volatile.acidity
# citric.acid
# residual.sugar
# chlorides
# free.sulfur.dioxide
# total.sulfur.dioxide
# density
# pH
# sulphates
# alcohol
# quality

#breast cancer headers

# mean_radius
# mean_texture
# mean_perimeter
# mean_area
# mean_smoothness
# diagnosis

# x_train is the training data set.
# y_train is the set of labels to all the data in x_train.
# The test set is a subset of the data set that you use to test your model after the model has gone through initial vetting by the validation set.

# x_test is the test data set.
# y_test is the set of labels to all the data in x_test.

#adaptive boosting classifier
#https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html
#weak-learners

#It combines multiple classifiers to increase the accuracy of classifiers. 

#Accuracy is about 0.412 for winequality-white for 50 estimators (Rating 1-10)
#Accuracy is about 0.431 for winequality-white for 100 estimators (Rating 1-10)
#Accuracy is about 0.490 for winequality-white for 10 estimators (Rating 1-10)

#Accuracy is about 0.956 for breast-cancer for 10 estimators (binary)
#Accuracy is about 0.938 for breast-cancer for 50 estimators (binary)
#Accuracy is about 0.964 for breast-cancer for 100 estimators (binary)

def ada_boost(X_train, X_test, y_train, y_test): 
    clf=AdaBoostClassifier(n_estimators=10, learning_rate=1) #ideal n_estimators: 10
    clf.fit(X_train,y_train)
    y_pred=clf.predict(X_test)
    return y_pred

#Accuracy is about 0.423 for winequality-white for 50 estimators (Rating 1-10)
#Accuracy is about 0.673 for winequality-white for 100 estimators (Rating 1-10)
#Accuracy is about 0.361 for winequality-white for 10 estimators (Rating 1-10)

#Accuracy is about 0.947 for breast-cancer for 300 estimators (binary)
#Accuracy is about 0.971 for breast-cancer for 100 estimators (binary)
#Accuracy is about 0.921 for breast-cancer for 50 estimators (binary)

def random_forest(X_train, X_test, y_train, y_test):
    clf=RandomForestClassifier(n_estimators=50)
    clf.fit(X_train,y_train)
    y_pred=clf.predict(X_test)
    return y_pred

#Accuracy is about 0.631 for winequality-white  (Rating 1-10)

#Accuracy is about 0.903 for breast-cancer (Binary)

def decision_tree(X_train, X_test, y_train, y_test):
    clf=tree.DecisionTreeClassifier()
    clf.fit(X_train,y_train)
    y_pred=clf.predict(X_test)
    return y_pred

#algo_name is the name of the function you want to run: ada_boost, random_forest, or deicision_tree
#data_set is the name of the dataset without path and file extension: 'winequality-white', or 'Breast_cancer_data'

def run_algo(algo_name, data_set):
    print(algo_name, data_set)
    file_path = 'test_data/' + data_set + '.csv'
    dataframe = pandas.read_csv(file_path, header=None)
    dataset = dataframe.values
    X = dataset[:,0:len(dataset[0])-1].astype(float)
    y = dataset[:,len(dataset[0])-1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    #X_test = [[7,0.27,0.36,20.7,0.045,45,170,1.001,3,0.45,8.8]]

    prediction= algo_name(X_train, X_test, y_train, y_test)

    matrix = confusion_matrix(y_test, prediction)
    print(matrix)

    correct = 0
    for i in range(len(matrix)):
        correct += matrix[i][i]
    print("Accuracy: ", correct/len(y_test))
    print(algo_name, data_set)
    print("End of case")
    print("\n")

#Mutate the function to run for a different number of estimators if random_forest or ada_boost. Currently optimised for highest accuracy.

run_algo(random_forest, 'winequality-white')
run_algo(random_forest, 'Breast_cancer_data')

run_algo(ada_boost, 'winequality-white')
run_algo(ada_boost, 'Breast_cancer_data')

run_algo(decision_tree, 'winequality-white')
run_algo(decision_tree, 'Breast_cancer_data')

#The accuracy for wine quality (about 5000 rows) and breast cancer data (about 600 rows) is significant different. 
#This is expected because breast cancer is a binary data set, while wine quality is a) subjective and b) rated from 1-10

#The goal of k-fold cross-validation is to test the model's ability to predict new data 
# that was not used in estimating it, in order to flag problems like overfitting or selection 
# bias and to give an insight on how the model will generalize to an independent dataset 
# (i.e., an unknown dataset, for instance from a real problem).

