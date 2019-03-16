#https://stackoverflow.com/questions/44164749/how-does-keras-handle-multilabel-classification

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD


data_folder='../../../../data/'
train_data = np.load(data_folder+'train_2M.npz')
X_train = train_data['train']
Y_train = train_data['target']

val_data = np.load(data_folder+'val_2M.npz')
X_val = val_data['val']
Y_val = val_data['target']

test_data = np.load(data_folder+'test_2M.npz')
X_test = test_data['test']
Y_test = test_data['target']


model = Sequential()
model.add(Dense(5000, activation='relu', input_dim=80))
model.add(Dropout(0.1))
model.add(Dense(600, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(80, activation='sigmoid'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy',])


model.fit(X_train, Y_train,epochs=10,batch_size=10000, shuffle=False)
model.save(data_folder+'trained_model')

# 
# score = model.evaluate(X_val, Y_val, batch_size=2000)
# score
# Y_pred = model.predict_proba(X_test, batch_size=2000)
# Y_pred[Y_pred>=0.5]=1; y_pred[Y_pred<0.5]=0;
# print(Y_pred)