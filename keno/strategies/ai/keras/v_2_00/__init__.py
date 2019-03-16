#https://stackoverflow.com/questions/44164749/how-does-keras-handle-multilabel-classification

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import keras.backend as K
from keras.metrics import top_k_categorical_accuracy
import tensorflow as tf
from tensorflow.python.pywrap_tensorflow_internal import TF_SessionRun




data_folder='../../../../data/'
train_data = np.load(data_folder+'train_75k.npz')
val_data = np.load(data_folder+'val_75k.npz')
test_data = np.load(data_folder+'test_75k.npz')
X_train = train_data['train']; Y_train = train_data['target']
X_val = val_data['val']; Y_val = val_data['target']
X_test = test_data['test']; Y_test = test_data['target']


model = Sequential()
model.add(Dense(5000, activation='relu', input_dim=80))
model.add(Dropout(0.1))
model.add(Dense(600, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(80, activation='sigmoid'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

def top_20_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=20)

def top_10_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=10)

def accuracy_top_20(y_true, y_pred):
    #print(K.int_shape(y_pred)[0])
    #K.shape(y_pred).eval(session=K.get_session())
    #top_values, top_indices = K.get_session().run(tf.nn.top_k(y_pred, k=5))
    return top_k_categorical_accuracy(y_true, y_pred, k=20);

def to_binary_pred(y_true, y_pred):
    tf_session = K.get_session();
    threshod = 0.5;
    print(K.eval(y_pred))
    b_pred = K.shape(y_pred).eval(session=tf_session)
    #convert tensor to numpy aray
#     y_pred = y_pred.eval();
#     y_pred[y_pred>=threshod]=1; 
#     y_pred[y_pred< threshod ]=0;
    return b_pred;

def accuracy_match_20(y_true, y_pred):
    match_20 = K.placeholder(shape=[75000,20], dtype= 'float32') * 100;
    #y_pred = K.print_tensor(y_pred, [K.eval(y_pred)], "YPRED: ")
    #print_y =K.print_tensor(y_pred, "YPRED IS: ");
    #K.eval(y_pred)
    #yt_values, yt_indices = tf.nn.top_k(y_true, k=20);
    yp_values, yp_indices = tf.nn.top_k(y_pred, k=20);
    #matched_elements = np.array([i for i in yt_indices if i in yp_indices])
    #match_20 = len(matched_elements)
    #sorted_output_indexes = np.argsort(y_pred)
    #print(sorted_output_indexes)        
#     target_numpy = y_true
#         #print(target_numpy)
#     "Accuracy is calculated"
#     i=59; last=80; # i stops at 79
#     while (i < last):
# #           print( target_numpy[sorted_output_indexes[i]])
#         if (target_numpy[sorted_output_indexes[i]]==1.0):
#             match_20 += 1;
#         i+=1
    #accuracy_20 = match_20/20;
    return match_20;
# 
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy', top_10_accuracy] )
# model.compile(loss='binary_crossentropy',
#               optimizer=sgd,
#               metrics=['accuracy',])
 
 
model.fit(X_train, Y_train,epochs=1,batch_size=10000, shuffle=False)
model.save(data_folder+'trained_model')




# 
# score = model.evaluate(X_val, Y_val, batch_size=2000)
# # score \ \ct_proba(X_test, batch_size=2000)
# #Y_pred[Y_pred>=0.5]=1; Y_pred[Y_pred<0.5]=0;
# print(Y_pred)
