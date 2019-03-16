from hotspot.models import iresult, idraw, idepth;

from hotspot.strategies.ai.tf import TFOutput;

import tensorflow as tf
import tensorboard as tb
import numpy as np
import matplotlib as plt
import os 

'''
multi-label classification

HOT TO SAVE/RESTORE MODEL
http://cv-tricks.com/tensorflow-tutorial/save-restore-tensorflow-models-quick-complete-tutorial/
https://blog.metaflow.fr/tensorflow-how-to-freeze-a-model-and-serve-it-with-a-python-api-d4f3596b3adc

TimeSeries
https://mapr.com/blog/deep-learning-tensorflow/
https://medium.com/mlreview/a-simple-deep-learning-model-for-stock-price-prediction-using-tensorflow-30505541d877


check https://github.com/tensorflow/skflow/issues/113
https://towardsdatascience.com/multi-label-image-classification-with-inception-net-cbb2ee538e30


1. 0,1,0,0,0,1,1,0 change to 0,0.05,0,0,0,0..05,   1/20=0.05 prob for each positive label

'''
model_name="tf_v_3_00"
data_folder='../../../data/'

input_size = 80;
output_size = 80;
hidden_layer_size = 240;

tf.reset_default_graph();

inputs = tf.placeholder(tf.float32, [None, input_size]);
targets= tf.placeholder(tf.float32, [None, output_size]);

weights_1 = tf.get_variable("weights_1", [input_size, hidden_layer_size])
biases_1 = tf.get_variable("biases_1", [hidden_layer_size])
outputs_1 = tf.nn.relu(tf.matmul(inputs, weights_1)+biases_1);

weights_2 = tf.get_variable("weights_2", [hidden_layer_size, hidden_layer_size])
biases_2 = tf.get_variable("biases_2", [hidden_layer_size])
outputs_2 = tf.nn.relu(tf.matmul(outputs_1, weights_2)+biases_2);

weights_3 = tf.get_variable("weights_3", [hidden_layer_size, hidden_layer_size])
biases_3 = tf.get_variable("biases_3", [hidden_layer_size])
outputs_3 = tf.nn.relu(tf.matmul(outputs_2, weights_3)+biases_3);

weights_4 = tf.get_variable("weights_4", [hidden_layer_size, output_size])
biases_4 = tf.get_variable("biases_4", [output_size])
outputs = tf.nn.relu(tf.matmul(outputs_3, weights_4)+biases_4);

np.set_printoptions(threshold='nan')
tfr=tf.python_io.TFRecordWriter('/output')


outputs = tf.Print(outputs, [tf.shape(outputs), outputs], "OUPUTS: ", 80)
targets = tf.Print(targets, [tf.shape(targets), targets], "TARGETS: ", 80)





    
#tfr.write(outputs)
tfr.close;

#loss = tf.nn.softmax_cross_entropy_with_logits_v2(logits=outputs, labels=targets);
final_tensor = tf.nn.sigmoid(outputs, name="outputs")
final_tesor = tf.Print(final_tensor, [tf.shape(final_tensor), final_tensor], 'Final tensor: ')

#final_tensor = tf.Print(final_tensor, [final_tensor], "final tensor: ")
cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(logits=outputs,labels=targets)
cross_entropy = tf.Print(cross_entropy, [tf.shape(cross_entropy), cross_entropy], 'CROSS ENTROPY: ')


mean_loss = tf.reduce_mean(cross_entropy) ###### CHECK IF CROSS ENTROPY is the LOSS

optimizer=tf.train.AdamOptimizer(learning_rate=0.001).minimize(mean_loss);

def pr_ok():
    print("OKAY");
    
def pr_no():
    print("NO")

def calc_accuracy(sess, output, target):
    match_20=10
    output_sorted, indices = tf.nn.top_k(output)
    output_sorted = tf.Print(output_sorted, [output_sorted, indices], "OUPUT_SORTED: ")
    #print(sess.run(target))
# #     sorted_indexes_asc = np.argsort(output)
# #     "Accuracy is calculated"\\
#     i=0; end=20; # i stops at 79
#     while (i < end):
#         tf.cond(tf.equal(target.get_variable(indices[i]), 1.0), pr_ok, pr_no);
#     i+=1;
            
    return ((match_20/20))
    
    
##### PLA WITH THIS FOR ACCURACY    
#out_equals_target = tf.equal(tf.arg_max(outputs,1), tf.arg_max(targets,1))



sess = tf.InteractiveSession();
initializer = tf.global_variables_initializer();
sess.run(initializer)


accuracy=tf.reduce_mean(tf.cast(calc_accuracy(sess, outputs, targets), tf.float32))


batch_size = 100;
max_epochs =  5000;
prev_validation_loss = 9999999.



train_data = np.load(data_folder+'train_1.npz')
val_data = np.load(data_folder+'val_1.npz')
test_data=np.load(data_folder+'test_1.npz')

for epoch_counter in range(max_epochs):
    cur_epoch_loss = 0;
    
#     for train in train_data:
#         
#         try:
#             _, batch_loss = sess.run([optimizer, mean_loss], feed_dict={inputs: train['train'], targets: train['target']});
#             cur_epoch_loss += batch_loss;
#         except ValueError:
#             print("value error")
#         
#     for train in train_data:
    with np.load(data_folder+'train_75k.npz') as data:
        
        try:
            #print(sess.run([outputs]), feed_dict={inputs: data['train'], targets: data['target']});
            _, batch_loss = sess.run([optimizer, accuracy], feed_dict={inputs: data['train'], targets: data['target']});
  
           
        except ValueError:
            print("value error")   
        
    #cur_epoch_loss /= train_data.batch_count
    
