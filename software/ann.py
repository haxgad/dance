# aritificial nerual network

import os
import torch
import torch.nn as nn
import torch.nn.functional as F


def run_ann(X_train, X_test, y_train, y_test, model_name):



    if os.path.isfile(model_name):
        model = torch.load(model_name)
    else:
        n_in = len(X_train[0])
        n_h = 5
        n_out = 1
        model = nn.Sequential(nn.Linear(n_in, n_h),
                            nn.ReLU(),
                            nn.Linear(n_h, n_out),
                            nn.Sigmoid())

    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

    x = torch.FloatTensor(X_train)
    y = torch.FloatTensor(y_train)
    for epoch in range(1000):
        # Forward Propagation
        y_pred = model(x)
        # Compute and print loss
        loss = criterion(y_pred, y)
        print('epoch: ', epoch,' loss: ', loss.item())
        # Zero the gradients
        optimizer.zero_grad()
        # perform a backward pass (backpropagation)
        loss.backward()
        # Update the parameters
        optimizer.step()
    
    x = torch.FloatTensor(X_test)
    y = torch.FloatTensor(y_test)
    for epoch in range(500):
        # Forward Propagation.
        y_pred = model(x)
        # Compute and print loss.
        loss = criterion(y_pred, y)
        print ('epoch: ', epoch, ' loss: ', loss.item())
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

    torch.save(model, model_name)

    for i in range(len(pred_list)):
        if pred_list[i] == y_test[i][0]:
            correct += 1
    return correct/len(pred_list)