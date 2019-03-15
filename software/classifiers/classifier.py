from keras.models import load_model

class Classifier:
    def __init__(self, model_path):
        print('Loading model from ' +  model_path)
        self.model = load_model(model_path)
        print('Successfully loaded the model: ', self.model)

    def predict(self, input_data):
        return self.model.predict_classes(input_data, verbose=0)


# test purpose, remove when integrating
import pandas as pd
from sklearn.metrics import confusion_matrix

file_name = 'hard'
file_path = '../test_data/' + file_name + '.csv'
dataframe = pd.read_csv(file_path, header=None)
dataset = dataframe.values
X = dataset[:,0:len(dataset[0])-1].astype(float)
y = dataset[:,len(dataset[0])-1].astype(float)
clf = Classifier('../models/' + file_name + '_model.h5')
print(confusion_matrix(y, clf.predict(X)))
