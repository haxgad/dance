# aritificial nerual network

import torch
import torch.nn as nn
import torch.nn.functional as F
from preprocess_data import split_feature_class_as_array


def run_ann(training_set, test_set):
    training_feature = []
    training_class = []
    test_feature = []
    test_class = []
    split_feature_class_as_array(training_set, training_feature, training_class)
    split_feature_class_as_array(test_set, test_feature, test_class)

    n_in = len(training_feature[0])
    n_h = 5
    n_out = 1

    model = nn.Sequential(nn.Linear(n_in, n_h),
                        nn.ReLU(),
                        nn.Linear(n_h, n_out),
                        nn.Sigmoid())
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

    x = torch.FloatTensor(training_feature)
    y = torch.FloatTensor(training_class)
    for epoch in range(2000):
        # Forward Propagation
        y_pred = model(x)
        # Compute and print loss
        loss = criterion(y_pred, y)
        # print('epoch: ', epoch,' loss: ', loss.item())
        # Zero the gradients
        optimizer.zero_grad()
        # perform a backward pass (backpropagation)
        loss.backward()
        # Update the parameters
        optimizer.step()
    
    x = torch.FloatTensor(test_feature)
    y = torch.FloatTensor(test_class)
    for epoch in range(500):
        # Forward Propagation.
        y_pred = model(x)
        # Compute and print loss.
        loss = criterion(y_pred, y)
        # print ('epoch: ', epoch, ' loss: ', loss.item())
        # Zero the gradients.
        optimizer.zero_grad()
        # perform a backward pass (backpropagation)
        loss.backward()
        # Update the parameters
        optimizer.step()

    correct = 0
    pred_list = []
    for i in range(len(y_pred)):
        if y_pred.data[i] < 0.5:
             pred_list.append(0)
        else:
            pred_list.append(1)

    for i in range(len(pred_list)):
        if pred_list[i] == test_class[i][0]:
            correct += 1
    return correct/len(pred_list)