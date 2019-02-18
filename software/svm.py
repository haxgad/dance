# support vector machine

from sklearn import svm

def run_svm(X_train, X_test, y_train, y_test):
    clf = svm.SVC(gamma=0.01, C=10.)
    clf.fit(X_train, y_train) 
    prediction = clf.predict(X_test)
    correct = 0
    for i in range(len(prediction)):
        if prediction[i] == y_test[i]:
            correct += 1
    return correct/len(y_test)