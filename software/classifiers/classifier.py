from keras.models import load_model

class Classifier:
    def __init__(self, model_path):
        print('Loading model from ' +  model_path)
        self.model = load_model(model_path)
        print('Successfully loaded the model: ', self.model)

    def predict(self, input_data):
        return self.model.predict_classes(input_data, verbose=0)

