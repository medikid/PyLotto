# -*- coding: utf-8 -*-
from torch.autograd import Function;
import numpy as np;
import torch
from torch.utils.data import Dataset, DataLoader
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F

from hotspot_dataset import HotSpotDataset

class CustomLoss(Function):
    
    @staticmethod
    def forward(inputs):
#        input_size = 80;
#        hidden_layer_size =240;
#        outputs_size = 80;
#        
#        dtype = torch.FloatTensor
#        input_layer = nn.Linear(input_size, hidden_layer_size).type(dtype);
#        hidden_layer_1=nn.Linear(hidden_layer_size,hidden_layer_size).type(dtype)
#        hidden_layer_2=nn.Linear(hidden_layer_size,hidden_layer_size).type(dtype)
#        output_layer=nn.Linear(hidden_layer_size,outputs_size).type(dtype)       
#        
#        
#        output1=F.relu(input_layer(inputs))
#        output2=F.relu(hidden_layer_1(output1))
#        output3=F.relu(hidden_layer_2(output2))
#        y_pred=F.relu(output_layer(output3))
        
#        criterion = nn.CrossEntropyLoss();
#        loss = criterion(y_pred, targets)
        #inputs=inputs.clone();
        return inputs;
        
    @staticmethod
    def backward(grad_output):
        print("CALLING BACKWARD")
        #grad_input = grad_output.clone();
        return grad_output;
    
    

    
#model=CustomLoss()
#hotspot = HotSpotDataset('train_75k.npz')
#
##i = 100 ; #    id 2277411
#for i in range(hotspot.__len__()):
##while(i<101):
#    ids, inputs, targets = hotspot.__getitem__(i);
#    x = Variable(inputs, requires_grad=True).float();
#    y= Variable(targets, requires_grad=False).float()
#    outputs=model.forward(x);
#    loss=model.loss(outputs,y)
#    
#    model.backward();
    #y_pred = model.forward(x)
    #print(ids, y.data, "accuracy :" , loss , " %");