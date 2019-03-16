# -*- coding: utf-8 -*-
import numpy as np;
import torch
from torch.utils.data import Dataset, DataLoader
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F

class HotSpotDataset(Dataset):
    data_folder='../../../data/';
    
    def __init__(self, dataset_name):
        data = np.load(self.data_folder+dataset_name)
        self.len = data['train'].shape[0]
        self.x_data = torch.from_numpy(data['train'])
        self.y_data = torch.from_numpy(data['target'])
        
    def __getitem__(self, index):
        return (self.x_data[index], self.y_data[index])
        
    def __len__(self):
        return self.len
    
#hsp = HotSpotDataset('train_75k.npz', 'train');
#train_loader = DataLoader( dataset=hsp,batch_size=100, shuffle=False, num_workers=1 )






#for epoch in range(100):
#    print(epoch)
#    for i, data in enumerate(train_loader, 0):
#        train, target = data;
#        inputs, labels = Variable(train).float(), Variable(target).float()
#        y_pred = model().forward(inputs)
#        print(epoch, y_pred, labels)
    
#    with np.load(data_folder+'train_75k.npz') as data:
#        inputs =  Variable(torch.from_numpy(data['train']).float())
#        targets = Variable(torch.from_numpy(data['target']).float())
#        
#        
#        
#        m=Model();
#        for input in inputs:
#            #output = torch.nn.functional.sigmoid(m.forward(input))
#            output = m.forward(input)
#            print(output)
# -*- coding: utf-8 -*-

