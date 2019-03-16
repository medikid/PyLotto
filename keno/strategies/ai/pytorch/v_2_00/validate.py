# -*- coding: utf-8 -*-

    # -*- coding: utf-8 -*-
import numpy as np;
import torch
from torch.utils.data import Dataset, DataLoader
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F

from hotspot_dataset import HotSpotDataset
from model import Model
    
model=Model()
model.setup(80,80,200,3)

#model = torch.load_state_dict(torch.load('TrainedModel_v_3_00.pt'))
model.load_state_dict(torch.load('TrainedModel_v_3_00.pt'))
hotspot = HotSpotDataset('val_75k.npz', 'val')
print(model.state_dict)
#i = 100 ; #    id 2277411
for i in range(hotspot.__len__()):
    ids, inputs, targets = hotspot.__getitem__(i);
    x = Variable(inputs, requires_grad=True).float();
    y= Variable(targets, requires_grad=False).float()
    
    outputs = model.forward(x)
#    x=CustomLoss()(x)
#    CustomLoss.apply
    #model.loss(x)
    #loss=CustomLoss.apply()
    loss=model.loss(x, y, 10);
    #y_pred = model.forward(x)
    print(i,ids, "accuracy :" , loss , " %");
