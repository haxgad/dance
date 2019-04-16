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

window_size = 50
dance_data = np.array([[0.0]*91])
for f in listdir("../final_data/"):
    if ".txt" in f:
        dataframe = pd.read_csv("../final_data/"+f, sep=",", header=None)
        dataset = dataframe.values
        print(f)
        i = 0
        while i+window_size <= len(dataset): 
            X = dataset[i:i+window_size,0:15]
            X = data_process(X)
            if "chicken" in f:
                X = np.append(X, 0)
            if "cowboy_front" in f:
                X = np.append(X, 1)
            if "cowboy_back" in f:
                X = np.append(X, 2)
            if "crab" in f:
                X = np.append(X, 3)
            if "hunchback" in f:
                X = np.append(X, 4)
            if "raffles_left" in f:
                X = np.append(X, 5)
            if "raffles_right" in f:
                X = np.append(X, 6)
            if "running" in f:
                X = np.append(X, 7)
            if "james" in f:
                X = np.append(X, 8)
            if "snake" in f:
                X = np.append(X, 9)
            if "double" in f:
                X = np.append(X, 10)
            if "mermaid" in f:
                X = np.append(X, 11)
            if "final" in f:
                X = np.append(X, 12)
            dance_data = np.append(dance_data, [X], axis=0)
            i += 10
dance_data = dance_data[1:]
np.savetxt("../final_data/processed_data/window50.csv", dance_data, delimiter=",")
