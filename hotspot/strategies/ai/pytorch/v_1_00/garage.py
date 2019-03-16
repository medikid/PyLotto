# -*- coding: utf-8 -*-
import numpy as np

data = np.load('../../../data/train_75k.npz')
print(data['train'].shape[0])