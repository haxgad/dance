import numpy as np
from keras.models import load_model
from sklearn import preprocessing

class Classifier:
    def __init__(self, model_path):
        print('Loading model from ' +  model_path)
        self.model = load_model(model_path)
        print('Successfully loaded the model: ', self.model)

    def data_process(self, input_data):
        # extract features from raw data
        # mean, variance, median, mean absolute deviation, max, min
        X = []
        for i in range(len(input_data[0])):
            data = []
            for j in range(len(input_data)):
                data.append(input_data[j][i])
            # mean
            X.append(np.mean(data))
            # variance
            X.append(np.var(data))
            # median
            X.append(np.median(data))
            # mean absolute deviation
            X.append(np.mean(np.absolute(data - np.mean(data))))
            # max
            X.append(max(data))
            # min
            X.append(min(data))
        return np.array(X)

    def predict(self, input_data):
        features = preprocessing.normalize([self.data_process(input_data)])
        return self.model.predict_classes(features, verbose=0)


# test purpose, remove when integrating
import pandas as pd
# from sklearn.metrics import confusion_matrix

# file_name = 'dance_data_Mar_26'
# file_path = '../dance_data/' + file_name + '.csv'
# dataframe = pd.read_csv(file_path, header=None)
# dataset = dataframe.values
# X = preprocessing.normalize(dataset[:,0:len(dataset[0])-1].astype(float))
# y = dataset[:,len(dataset[0])-1].astype(float)
# clf = Classifier('../models/' + file_name + '_model.h5')
# print(confusion_matrix(y, clf.predict(X)))

dataframe = pd.read_csv("../dance_data/processed_data/everything.txt", sep=",", header=None)
dataset = dataframe.values[:,0:15]
clf = Classifier('../models/dance_data_Mar_26_model.h5')
start = 157
window_size = 25
print(clf.predict(dataset[start:start+window_size]))
