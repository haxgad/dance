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

