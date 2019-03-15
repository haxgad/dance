import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.utils import np_utils
from sklearn.model_selection import StratifiedKFold
import os.path

def build_nn_model(num_feature, num_class):
		# create model
		model = Sequential()
		model.add(Dense(8, input_dim=num_feature, activation='relu'))
		model.add(Dense(6, input_dim=8, activation='linear'))
		model.add(Dense(num_class, activation='softmax'))
		# Compile model
		model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
		return model


def run_ann(X_train, X_test, y_train, y_test, model_name): 

	if(os.path.isfile('../models/' + model_name + '.h5')):
		model = load_model('../models/' + model_name + '.h5')
	else:
		num_feature = len(X_train[0])
		num_class = max(np.amax(y_train).astype(int), np.amax(y_test).astype(int))+1
		model = build_nn_model(num_feature, num_class)
	
	model.fit(X_train, y_train, epochs=200, batch_size=10, verbose=0)

	model.save('../models/' + model_name + '.h5')
	prediction = model.predict_classes(X_test, verbose=0)
	accuracy = model.evaluate(X_test, y_test, verbose=0)[1]
	return prediction, accuracy

def k_fold_cross_validate(X, y, model_name):
	model = load_model('../models/' + model_name + '.h5')

	seed = 7
	np.random.seed(seed)
	cvscores = []
	kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
	
	for train, test in kfold.split(X, y):
		# model.fit(X[train], y[train], epochs=150, batch_size=10, verbose=0)
		scores = model.evaluate(X[test], y[test], verbose=0)
		print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
		cvscores.append(scores*100)

	print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))