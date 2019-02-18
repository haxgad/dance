from ann import run_ann
from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import csv

def get_data_set(file_path):
    with open(file_path, 'r') as csvfile:
            lines = csv.reader(csvfile)
            dataset = list(lines)
            X = []
            y = []
            for i in range(1, len(dataset)):
                dataset[i] = [float(j) for j in dataset[i]]
                X.append(dataset[i][0:len(dataset[i])-1])
                y.append(dataset[i][len(dataset[i])-1:len(dataset[i])])
    return X, y


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
        if prediction[i] == test_class[i]:
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


file_path = "test_data/heart.csv"
X, y = get_data_set(file_path)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=0.2)

# accuracy = run_knn(X_train, X_test, y_train, y_test, k=5)
# accuracy = run_svm(X_train, X_test, y_train, y_test)
accuracy = run_ann(X_train, X_test, y_train, y_test, "heart_model")
# accuracy = run_perceptron(X_train, X_test, y_train, y_test)
print(accuracy)
