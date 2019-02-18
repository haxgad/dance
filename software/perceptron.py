# Perceptron Learning Algorithm
from sklearn.linear_model import Perceptron

def run_perceptron(X_train, X_test, y_train, y_test):
    clf = Perceptron(tol=1e-3, random_state=0)
    clf.fit(X_train, y_train)
    return clf.score(X_test, y_test)


