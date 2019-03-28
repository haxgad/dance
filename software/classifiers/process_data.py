import pandas as pd
import numpy as np
from os import listdir

def data_process(input_data):
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


dance_data = np.array([[0.0]*91])
for f in listdir("../data_26-March/"):
    if ".txt" in f:
        dataframe = pd.read_csv("../data_26-March/"+f, sep=",", header=None)
        dataset = dataframe.values
        i = 0
        while i+25 <= len(dataset): 
            X = dataset[i:i+25,0:15]
            X = data_process(X)
            if "chicken" in f:
                X = np.append(X, 0)
            if "cowboy" in f:
                X = np.append(X, 1)
            if "crab" in f:
                X = np.append(X, 2)
            if "hunchback" in f:
                X = np.append(X, 3)
            if "raffles" in f:
                X = np.append(X, 4)
            dance_data = np.append(dance_data, [X], axis=0)
            i += 1
            print(len(dance_data))
np.savetxt("../data_26-March/data.csv", dance_data, delimiter=",")
