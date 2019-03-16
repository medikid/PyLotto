

import keras as K
import numpy as np

class KRS:
    
    _model = None;
    _model_path = None;
    _data_folder = '../../../../data/';
    
    def __init__(self, Model, ModelPath=None, Version=1.00):
        self._model = Model;
        self._model_path=ModelPath
        self._version = Version;
        
    
    def SaveModel(self):
        #self._model.save(self._model_path +'trained_model')
        
                # serialize model to JSON
        model_json = self._model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self._model.save_weights(self._model_path + "model.h5")
        print("Saved model to disk")
        
    def LoadModel(self):
        #self._model.load_weights(self._model_path + "model.h5")
        # load json and create model
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = self._model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(self._model_path + "model.h5")
        print("Loaded model from disk")
        
    def findMatches(self, a, b):
        x, y = a.shape
        matches = np.zeros((x,1), dtype=np.int32) 
        for z in range(x):
            match = np.array([i for i in a[z] if i in b[z]])
            print(match)
            matches[z] = len(match)
            #np.append(matches, len(match), axis=0)
            #matches[z] = match
                   
        return matches;
        
k = KRS(None)
a = np.array([[11, 33, 22, 55, 44, 77, 66, 88], [111, 222, 333, 444, 555, 666, 777, 888]], dtype=np.int32)
b = np.array([[11, 22, 33, 4, 55, 6, 77, 8], [1, 222, 3, 444, 5, 666, 7, 888]], dtype=np.int32)

a_ = np.argmax(a[0], axis=-1)
#c = np.in1d(a,b)
#c = np.array([i for i in a[0] if i in b[0]])
print(k.findMatches(a, b))
        
        
