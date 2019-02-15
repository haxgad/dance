from knn import run_knn
from svm import run_svm
from ann import run_ann
from perceptron import run_perceptron
from preprocess_data import process_dataset

data_file_path = "test_data/pulsar_stars.csv"
split_ratio = 0.75  #proportion of training sets
training_set = []
test_set = []
process_dataset(data_file_path, split_ratio, training_set, test_set)

# accuracy = run_knn(training_set, test_set, k=5)
# accuracy = run_svm(training_set, test_set)
# accuracy = run_ann(training_set, test_set, "heart_model")
accuracy = run_perceptron(training_set, test_set)
print(accuracy)