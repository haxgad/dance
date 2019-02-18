import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split


def run_ann(X_train, X_test, y_train, y_test, model_name): 
	num_feature = len(X_train[0])
	num_class = np.amax(y_train).astype(int)+1

	def nn_model():
		# create model
		model = Sequential()
		model.add(Dense(8, input_dim=num_feature, activation='relu'))
		model.add(Dense(num_class, activation='softmax'))
		# Compile model
		model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
		return model

	estimator = KerasClassifier(build_fn=nn_model, epochs=200, batch_size=5, verbose=0)
	estimator.fit(X_train, y_train)
	y_pred = estimator.predict(X_test)
	matrix = confusion_matrix(y_test, y_pred)

	correct = 0
	for i in range(len(matrix)):
		correct += matrix[i][i]
	print(matrix)
	return correct/len(y_pred)