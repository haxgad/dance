from keras.models import load_model

class Classifier:
    def __init__(self, model_path):
        print('Loading model from ' +  model_path)
        self.model = load_model(model_path)
        print('Successfully loaded the model: ', self.model)

    def data_process(input_data):
        X = []
        for i in range(len(input_data[0])):
            data = []
            for j in range(len(input_data)):
                data.append(input_data[j][i])
            X.append(np.mean(data))
            X.append(np.var(data))
            X.append(np.median(data))
            X.append(max(data))
            X.append(min(data))
        return np.array(X)

    def predict(self, input_data):
        featrues = data_process(input_data)
        return self.model.predict_classes(featrues, verbose=0)


# test purpose, remove when integrating
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix

def data_process(input_data):
    X = []
    for i in range(len(input_data[0])):
        data = []
        for j in range(len(input_data)):
            data.append(input_data[j][i])
        X.append(np.mean(data))
        X.append(np.var(data))
        X.append(np.median(data))
        X.append(max(data))
        X.append(min(data))
    return np.array(X)
    

file_name = 'pulsar_stars'
file_path = '../test_data/' + file_name + '.csv'
dataframe = pd.read_csv(file_path, header=None)
dataset = dataframe.values
X = dataset[:,0:len(dataset[0])-1].astype(float)
# y = dataset[:,len(dataset[0])-1].astype(float)
# clf = Classifier('../models/' + file_name + '_model.h5')
# print(confusion_matrix(y, clf.predict(X)))
X = data_process(X[0:5])
print(X)