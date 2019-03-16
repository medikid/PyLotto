from hotspot.models import iresult, idraw, idepth;
import tensorflow as tf
import tensorboard as tb
import numpy as np
import matplotlib as plt
import os 


from keras.layers import Dense
from keras import backend as K
from keras.objectives import categorical_crossentropy, binary_crossentropy
from keras.metrics import categorical_accuracy as accuracy

model_name="kr_v_4_00"
data_folder='../../../data/'

input_size = 80;
output_size = 80;
hidden_layer_size = 240;



tf.reset_default_graph();

inputs = tf.placeholder(tf.float32, [None, input_size]);
targets= tf.placeholder(tf.float32, [None, output_size]);

# weights_1 = tf.get_variable("weights_1", [input_size, hidden_layer_size])
# biases_1 = tf.get_variable("biases_1", [hidden_layer_size])
# outputs_1 = tf.nn.relu(tf.matmul(inputs, weights_1)+biases_1);

x = Dense(hidden_layer_size, activation='relu')(inputs)

# weights_2 = tf.get_variable("weights_2", [hidden_layer_size, hidden_layer_size])
# biases_2 = tf.get_variable("biases_2", [hidden_layer_size])
# outputs_2 = tf.nn.relu(tf.matmul(outputs_1, weights_2)+biases_2);

x = Dense(hidden_layer_size, activation='relu')(x)

# weights_3 = tf.get_variable("weights_3", [hidden_layer_size, output_size])
# biases_3 = tf.get_variable("biases_3", [output_size])
# outputs = tf.nn.relu(tf.matmul(outputs_2, weights_3)+biases_3);

outputs = Dense(output_size, activation='sigmoid')(x)


# Keras model



#loss = tf.nn.softmax_cross_entropy_with_logits_v2(logits=outputs, labels=targets);
# final_tensor = tf.nn.sigmoid(outputs, name="outputs")
# cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(logits=outputs,labels=targets)


loss = tf.reduce_mean(categorical_crossentropy(targets, outputs))
#loss = tf.reduce_mean(binary_crossentropy(targets, outputs))

#mean_loss = tf.reduce_mean(cross_entropy) ###### CHECK IF CROSS ENTROPY is the LOSS

#optimizer=tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss);

optimizer = tf.train.GradientDescentOptimizer(0.001).minimize(loss)

##### PLA WITH THIS FOR ACCURACY    
#out_equals_target = tf.equal(tf.arg_max(outputs,1), tf.arg_max(targets,1))


acc_value = accuracy(targets, outputs)
   

sess = tf.InteractiveSession();
initializer = tf.global_variables_initializer();
sess.run(initializer)

K.set_session(sess)

batch_size = 100;
max_epochs =  50000;
prev_validation_loss = 9999999.


for epoch_counter in range(max_epochs):
    cur_epoch_loss = 0;
    

    with np.load(data_folder+'test_75k.npz') as data:
        
        try:
            #_, batch_loss = sess.run([acc_value, loss], feed_dict={inputs: data['train'], targets: data['target']});
            #cur_epoch_loss += batch_loss;
            
            
            
            #print(K.learning_phase())
            optimizer.run(feed_dict={inputs: data['test'], targets: data['target'], K.learning_phase(): 1})
            print(acc_value.eval(feed_dict={inputs: data['test'], targets: data['target']}))
            #print(K.get_value(K.learning_phase()))
        except ValueError:
            print("value error")   
    
    acc_value = accuracy(targets, outputs)   
    #cur_epoch_loss /= train_data.batch_count

    
print('End of Training')

file_path= './model/'
if not os.path.exists(file_path):
    os.mkdir(file_path)
saver = tf.train.Saver()
saver.save(sess, file_path+ 'model.checkpoint')
print('Model saved')

# saver = tf.train.import_meta_graph('model/model.checkpoint.meta')
# saver.restore(sess, tf.train.latest_checkpoint('model/model.checkpoint'))
saver.restore(sess, file_path+ 'model.checkpoint')
print("model loaded")

with np.load(data_folder+'test_75k.npz') as test:
    print(test['test'].shape, test['target'].shape)
    test_loss, test_accuracy = sess.run([loss, accuracy], feed_dict={ inputs: test['test'], targets: test['target']});
     
    print('. test Loss: '+'{0:.3f}'.format(test_loss)+
            '. test Accuracy: '+'{0:.2f}'.format(test_accuracy *100.)+'%')
    
