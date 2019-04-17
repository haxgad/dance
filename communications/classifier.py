import numpy as np
from sklearn import preprocessing
import pickle
import logging

def create_logger(name, filename='/home/pi/comms/ML.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create a file handler
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    return logger

logger = create_logger('ML')

class Classifier:
    def __init__(self, model_path):
        # print('Loading model from ' +  model_path)
        logger.info('Loading model from {}'.format(model_path))
        self.model = pickle.load(open(model_path, 'rb'))
        # self.model._make_predict_function()
        # print('Successfully loaded the model: ', self.model)
        logger.info('Successfully loaded the model: {}'.format(self.model))

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
