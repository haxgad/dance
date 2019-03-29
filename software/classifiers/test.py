import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
import pickle


file_name = 'dance_data_Mar_26'
file_path = '../dance_data/' + file_name + '.csv'
dataframe = pd.read_csv(file_path, header=None)
dataset = dataframe.values
X = preprocessing.normalize(dataset[:,0:len(dataset[0])-1].astype(float))
y = dataset[:,len(dataset[0])-1].astype(float)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# model = MLPClassifier(solver='sgd', alpha=1e-5, activation='relu', max_iter=200, 
#         hidden_layer_sizes=(64, 32, 16, 8), random_state=1, batch_size=10)
# model.fit(X_train, y_train)
# print(model.score(X_test, y_test))
# pickle.dump(model, open("../models/test_model.sav", 'wb'))
loaded_model = pickle.load(open("../models/test_model.sav", 'rb'))
Y = loaded_model.predict(X)
print(confusion_matrix(y, Y))
print(loaded_model.score(X, y))