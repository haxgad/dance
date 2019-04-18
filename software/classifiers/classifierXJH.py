from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.utils import np_utils
from keras.regularizers import l2
from sklearn.model_selection import StratifiedKFold
from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn import preprocessing
import numpy as np
import pandas as pd
import os.path

def build_nn_model(num_feature, num_class):
    # create model
    model = Sequential()
    model.add(Dense(64, input_dim=num_feature, activation='relu'))
    model.add(Dense(32, input_dim=64, activation = 'relu'))
    model.add(Dense(32, input_dim=32, activation = 'relu'))
    model.add(Dense(num_class, activation='softmax'))
    # Compile model
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def run_ann(X_train, X_test, y_train, y_test, model_name): 
    if(os.path.isfile('../final_models/' + model_name + '.h5')):
        model = load_model('../final_models/' + model_name + '.h5')
    else:
        num_feature = len(X_train[0])
        num_class = max(np.amax(y_train).astype(int), np.amax(y_test).astype(int))+1
        model = build_nn_model(num_feature, num_class)
        model.fit(X_train, y_train, epochs=200, batch_size=10, verbose=1)

    model.save('../final_models/' + model_name + '.h5')
    prediction = model.predict_classes(X_test, verbose=0)
    accuracy = model.evaluate(X_test, y_test, verbose=0)[1]
    return prediction, accuracy

def k_fold_cross_validate(X, y, model_name):
    model = load_model('../final_models/' + model_name + '.h5')
    
    seed = 7
    np.random.seed(seed)
    cvscores = []
    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
    
    for train, test in kfold.split(X, y):
        scores = model.evaluate(X[test], y[test], verbose=0)
        print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
        cvscores.append(scores*100)

    print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))


def run_perceptron(X_train, X_test, y_train, y_test):
    clf = Perceptron(tol=1e-3, random_state=0)
    clf.fit(X_train, y_train) 
    # load the model from disk
    # loaded_model = pickle.load(open(filename, 'rb'))
    # result = loaded_model.score(X_test, Y_test)
    prediction = clf.predict(X_test)
    accuracy = accuracy_score(prediction, y_test)
    # save the model to disk
    # filename = 'finalized_model.sav'
    # pickle.dump(clf, open(filename, 'wb'))
    return prediction, accuracy


def run_knn(X_train, X_test, y_train, y_test, k):
    # load the model from disk
    # clf = pickle.load(open(filename, 'rb'))
    # result = clf.score(X_test, Y_test)
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train) 
    prediction = clf.predict(X_test)
    accuracy = accuracy_score(prediction, y_test)
    # save the model to disk
    # filename = 'finalized_model.sav'
    # pickle.dump(clf, open(filename, 'wb'))
    return prediction, accuracy


def run_svm(X_train, X_test, y_train, y_test):
    # load the model from disk
    # clf = pickle.load(open(filename, 'rb'))
    # result = clf.score(X_test, Y_test)
    clf = svm.SVC(gamma=0.01, C=10.)
    clf.fit(X_train, y_train) 
    prediction = clf.predict(X_test)
    accuracy = accuracy_score(prediction, y_test)
    # save the model to disk
    # filename = 'finalized_model.sav'
    # pickle.dump(clf, open(filename, 'wb'))
    return prediction, accuracy


# file_name = 'bezdekIris'
# file_name = 'pulsar_stars'
# file_name = 'heart'
# file_name = 'hard'
# file_name = 'data'
# file_path = '../test_data/' + file_name + '.csv'
file_name = 'window50'
file_path = '../final_data/processed_data/' + file_name + '.csv'
dataframe = pd.read_csv(file_path, header=None)
dataset = dataframe.values
X = preprocessing.normalize(dataset[:,0:len(dataset[0])-1].astype(float))
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