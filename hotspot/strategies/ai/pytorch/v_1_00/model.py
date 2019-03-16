# -*- coding: utf-8 -*-
import numpy as np;
import torch
from torch.utils.data import Dataset, DataLoader
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F

from hotspot_dataset import HotSpotDataset

class Model(nn.Module):

    def __init__(self):
        super(Model, self).__init__()
        # 1 input image channel, 6 output channels, 5x5 square convolution
        # kernel
        
#        x=Variable(input_data,requires_grad=False)
#        y=Variable(target_data,requires_grad=False)
        
        dtype = torch.FloatTensor
        
        self.w1=Variable(torch.randn(240,80).type(dtype), requires_grad=True)
        self.b1=Variable(torch.randn(240).type(dtype), requires_grad=True)
        self.input_layer = nn.Linear(80, 240).type(dtype);
        
        self.w2=Variable(torch.randn(240,240).type(dtype), requires_grad=True)
        self.b2=Variable(torch.randn(240).type(dtype), requires_grad=True)
        self.hidden_layer_1=nn.Linear(240,240).type(dtype)
        
        self.w3=Variable(torch.randn(240,240).type(dtype), requires_grad=True)
        self.b3=Variable(torch.randn(240).type(dtype), requires_grad=True)
        self.hidden_layer_2=nn.Linear(240,240).type(dtype)
        
        self.w4=Variable(torch.randn(240, 80).type(dtype), requires_grad=True)
        self.b4=Variable(torch.randn(80).type(dtype), requires_grad=True)
        self.output_layer=nn.Linear(240,80).type(dtype)       
               
        

    def forward(self, x):
        # Max pooling over a (2, 2) window
        #input_1=x.mm(self.w1).add(self.b1)
#        output1=F.relu(self.input_layer((x * self.w1)))
#        output2=F.relu(self.hidden_layer_1(output1.mm(self.w2).add(self.b2)))
#        output3=F.relu(self.hidden_layer_2(output2.mm(self.w3).add(self.b3)))
#        y_pred=F.relu(self.output_layer(output3.mm(self.w4).add(self.b4)))
        
        output1=F.relu(self.input_layer(x))
        output2=F.relu(self.hidden_layer_1(output1))
        output3=F.relu(self.hidden_layer_2(output2))
        y_pred=F.relu(self.output_layer(output3))
       
        return y_pred
    
    def loss(self, x, y):
        #print(x)
        output = self.forward(x);
        #print(output)
        return self.accuracy_10(output, y)
    
    def accuracy_20(self, output, target):
        match_20 =0;
        sorted_output_indexes = np.argsort(output.data.numpy())
        #print(sorted_output_indexes)
        target_numpy = target.data.numpy()
        #print(target_numpy)
        "Accuracy is calculated"
        i=59; last=80; # i stops at 79
        while (i < last):
#           print( target_numpy[sorted_output_indexes[i]])
            if (target_numpy[sorted_output_indexes[i]]==1.0):
                match_20 += 1;
            i+=1
        accuracy_20 = match_20/20;
        return accuracy_20
        
    def accuracy_10(self, output, target):
        match_10 =0;
        sorted_output_indexes = np.argsort(output.data.numpy())
        #print(sorted_output_indexes)
        target_numpy = target.data.numpy()
        #print(target_numpy)
        "Accuracy is calculated"
        i=69; last=80; # i stops at 79
        while (i < last):
#           print( target_numpy[sorted_output_indexes[i]])
            if (target_numpy[sorted_output_indexes[i]]==1.0):
                match_10 += 1;
            i+=1
        accuracy_10 = match_10 / 10;
        return accuracy_10
    
    def accuracy_14(self, output, target):
        match_10 =0;
        sorted_output_indexes = np.argsort(output.data.numpy())
        #print(sorted_output_indexes)
        target_numpy = target.data.numpy()
        #print(target_numpy)
        "Accuracy is calculated"
        i=76; last=80; # i stops at 79
        while (i < last):
#           print( target_numpy[sorted_output_indexes[i]])
            if (target_numpy[sorted_output_indexes[i]]==1.0):
                match_10 += 1;
            i+=1
        accuracy_10 = match_10 / 14;
        return accuracy_10   
    
model=Model()
hotspot = HotSpotDataset('train_75k.npz')

#i = 100 ; #    id 2277411
for i in range(hotspot.__len__()):
    inputs, targets = hotspot.__getitem__(i);
    x = Variable(inputs, requires_grad=True).float();
    y= Variable(targets, requires_grad=True).float()
    loss=model.loss(x, y);
    
    #loss.backward();
    #y_pred = model.forward(x)
    print(i, "accuracy :" , loss , " %");
