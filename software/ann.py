import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers import Dense
from keras.utils import np_utils
from sklearn.model_selection import StratifiedKFold
import os.path


def save_model(model, model_name):
    # saving model
    json_model = model.to_json()
    open(model_name + '.json', 'w').write(json_model)
    # saving weights
    model.save_weights(model_name + '_weights.h5', overwrite=True)


def load_model(model_name):
    # loading model
    model = model_from_json(open(model_name + '.json').read())
    model.load_weights(model_name + '_weights.h5')
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model


def build_nn_model(num_feature, num_class):
		# create model
		model = Sequential()
		model.add(Dense(8, input_dim=num_feature, activation='relu'))
		model.add(Dense(6, input_dim=8, activation='linear'))
		model.add(Dense(num_class, activation='softmax'))
		# Compile model
		model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
		return model


def run_ann(X_train, X_test, y_train, y_test, model_name): 
	y_train = np_utils.to_categorical(y_train)
	print(y_train)
	if(os.path.isfile(model_name + '.json')):
		model = load_model(model_name)
	else:
		num_feature = len(X_train[0])
		num_class = max(np.amax(y_train).astype(int), np.amax(y_test).astype(int))+1
		model = build_nn_model(num_feature, num_class)
	
	model.fit(X_train, y_train, epochs=200, batch_size=5, verbose=0)

	save_model(model, model_name)
	return model.predict_classes(X_test, verbose=0)

def k_fold_validate(X, y, model_name):
	seed = 7
	np.random.seed(seed)
	cvscores = []
	kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
	for train, test in kfold.split(X, y):
		model = load_model(model_name)
		model.fit(X[train], y[train], epochs=150, batch_size=10, verbose=0)
		scores = model.evaluate(X[test], y[test], verbose=0)
		print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
		cvscores.append(scores[1] * 100)
	print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))