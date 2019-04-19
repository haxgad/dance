import numpy as np
from sklearn.externals import joblib
from scipy import stats
from os import listdir

class Classifier:
    def __init__(self, model_path, scaler_path):
        print('Loading model from ' +  model_path)
        self.scaler = joblib.load(scaler_path)
        self.model = joblib.load(model_path)
        self.model._make_predict_function()
        print('Successfully loaded the model: ', self.model)

    def min(self, segment):
        arr = []
        for i in range(15):
            arr.append(np.min(segment[:,i]))
        return arr

    def max(self, segment):
        arr = []
        for i in range(15):
            arr.append(np.max(segment[:,i]))
        return arr

    def mean(self, segment):
        arr = []
        for i in range(15):
            arr.append(np.mean(segment[:,i]))
        return arr

    def standard_dev(self, segment):
        arr = []
        for i in range(15):
            arr.append(np.std(segment[:,i]))
        return arr

    def rms(self, segment):
        square = 0
        for i in range(15):
            square+=(segment[i]**2)
        mean = (square/float(15))
        root = math.sqrt(mean)
        return root

    def entropy(self, segment):
        arr = []
        for i in range(0,15):
            freq = np.abs(np.fft.rfft(segment[:,i]))
            arr.append(stats.entropy(freq,base =2))
        return arr

    def energy(self, segment):
        arr = []
        for i in range(0,15):
            freq = np.abs(np.fft.rfft(segment[:,i]))
            arr.append(np.sum(freq**2)/len(freq))
        return arr

    def extract(self, segment):
        final = []
        final.extend(self.min(segment))
        final.extend(self.max(segment))
        final.extend(self.mean(segment))
        final.extend(self.standard_dev(segment))
        final.extend(self.energy(segment))
        final.extend(self.entropy(segment))
        return final

    def predict(self, input_data):
        data = np.asarray(self.extract(np.asarray(input_data)))
        data = np.array([data])
        #features = np.nan_to_num(self.scaler.transform(data))
        features = self.scaler.transform(data)
        return self.model.predict_classes(features, verbose=0)
        
