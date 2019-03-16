# -*- coding: utf-8 -*-
import numpy as np;
import torch
from torch.utils.data import Dataset, DataLoader
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F

from torch.nn.modules.loss import BCELoss, BCEWithLogitsLoss, MultiMarginLoss, MultiLabelMarginLoss, MultiLabelSoftMarginLoss


from keno.strategies.ai.pytorch.keno_dataset import KenoDataset
from keno.strategies.ai.pytorch.v_2_00.custom_loss import CustomLoss

class Model(nn.Module):

    def __init__(self):
        super(Model, self).__init__()
        # 1 input image channel, 6 output channels, 5x5 square convolution
        # kernel
        
#        x=Variable(input_data,requires_grad=False)
#        y=Variable(target_data,requires_grad=False)
    def setup(self, input_size, outputs_size, hidden_layer_size, hidden_layers):   
        dtype = torch.FloatTensor
        
        self.w1=Variable(torch.randn(hidden_layer_size,input_size).type(dtype), requires_grad=True)
        self.b1=Variable(torch.randn(hidden_layer_size).type(dtype), requires_grad=True)
        self.input_layer = nn.Linear(input_size, hidden_layer_size).type(dtype);
        
        self.w2=Variable(torch.randn(hidden_layer_size,hidden_layer_size).type(dtype), requires_grad=True)
        self.b2=Variable(torch.randn(hidden_layer_size).type(dtype), requires_grad=True)
        self.hidden_layer_1=nn.Linear(hidden_layer_size,hidden_layer_size).type(dtype)
        
        self.w3=Variable(torch.randn(hidden_layer_size,hidden_layer_size).type(dtype), requires_grad=True)
        self.b3=Variable(torch.randn(hidden_layer_size).type(dtype), requires_grad=True)
        self.hidden_layer_2=nn.Linear(hidden_layer_size,hidden_layer_size).type(dtype)
        
        self.w4=Variable(torch.randn(hidden_layer_size, outputs_size).type(dtype), requires_grad=True)
        self.b4=Variable(torch.randn(outputs_size).type(dtype), requires_grad=True)
        self.output_layer=nn.Linear(hidden_layer_size,outputs_size).type(dtype)       
               
        

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
    
    def loss(self, x, y, match_by=20):
        #print(x)
        x=CustomLoss()(x)
        output = self.forward(x);
        
#        loss_fn = nn.MSELoss()
#        loss = loss_fn(output, y)
        loss = self.accuracy(output, y, match_by)
        #print(output)
        return loss;
    
    def accuracy(self, output, target, match_by = 20):
        matches = 0; i = 0; last = 80; # i stops at 79
        
        sorted_output_indexes = np.argsort(output.data.numpy())
        #print(sorted_output_indexes)
        target_numpy = target.data.numpy()
        
        if (match_by == 10):  i = 69;
        elif (match_by == 14): i = 76
        else: i = 59; # this is match by 20
            
        while (i < last):
#           print( target_numpy[sorted_output_indexes[i]])
            if (target_numpy[sorted_output_indexes[i]]==1.0): matches += 1;
            i+=1
        accuracy = matches / match_by;
        return accuracy
        
    
    
model=Model()
model.setup(80, 80, 200, 3)
keno = KenoDataset('train_75k.npz', 'train')

#i = 100 ; #    id 2277411
for i in range(keno.__len__()):
    ids, inputs, targets = keno.__getitem__(i);
    x = Variable(inputs, requires_grad=True).float();
    y= Variable(targets, requires_grad=False).float()
    
    criterion = BCELoss()
#    x=CustomLoss()(x)
    #CustomLoss.apply
#    loss = nn.MSELoss()
    #loss=CustomLoss.apply()
    loss=criterion(x, y);
    
    #loss = model.accuracy(output, target, 10)

    loss.backward();
    #y_pred = model.forward(x)
    #print(i,ids, "accuracy :" , loss , " %");
print("Training Complete")
    
torch.save(model.state_dict(), 'TrainedModel_v_2_00.pt')

  # .. to load your previously training model:
