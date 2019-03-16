import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F

import numpy as np


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
        print(x.size, self.w1.size)
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

data_folder='../../../data/'
for epoch in range(100):
    with np.load(data_folder+'train_75k.npz') as data:
        
        inputs =  Variable(torch.from_numpy(data['train']).float())
        targets = Variable(torch.from_numpy(data['target']).float())

        
        
        m=Model();
        for input in inputs:
            #output = torch.nn.functional.sigmoid(m.forward(input))
            output = m.forward(input)
            print(output)
