'''
Created on Feb 5, 2018

@author: somaj



'''

import numpy as np

class TFOutput:
    np_output= np.array([]);
    sorted_output_indexes=np.array([])
    target = np.array([])
    
    def __init__(self, output, target):
        self.np_output = output;
        self.sorted_output_indexes=np.argsort(output)
        self.target = target
        "TF Output Initiated"
        
        
    def calc_accuracy_20(self):
        match_20=0
        "Accuracy is calculated"
        i=69; len=80; # i stops at 79
        while (i < 80):
            if (self.target[self.sorted_output_indexes[i]]==1.0): match_20 += 1;
            
        return ((match_20/20)*100.00)
