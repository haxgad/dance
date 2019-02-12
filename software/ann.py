# aritificial nerual network

import torch
import torch.nn as nn
import torch.nn.functional as F
from preprocess_data import split_feature_class_as_array


def run_ann(trainingSet, testSet):
    trainingFeatures = []
    trainingClass = []
    testFeatures = []
    testClass = []
    split_feature_class_as_array(trainingSet, trainingFeatures, trainingClass)
    split_feature_class_as_array(testSet, testFeatures, testClass)

    n_in = len(trainingFeatures[0])
    n_h = 5
    n_out = 1

    x = torch.FloatTensor(trainingFeatures)
    y = torch.FloatTensor(trainingClass)

    model = nn.Sequential(nn.Linear(n_in, n_h),
                        nn.ReLU(),
                        nn.Linear(n_h, n_out),
                        nn.Sigmoid())
    print(model)

    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

    for epoch in range(10000):
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
    
    test = torch.FloatTensor(testFeatures)
    pred = model(test)
    correct = 0
    pred_list = []
    for i in range(len(pred)):
        if pred.data[0] < 0.5:
             pred_list.append(0)
        else:
            pred_list.append(1)

    for i in range(len(pred_list)):
        if pred_list[i] == testClass[i][0]:
            correct += 1

    return correct/len(pred_list)