from hotspot.models import iresult, idraw, idepth;

from hotspot.strategies.ai.tf import TFOutput;

import tensorflow as tf
import tensorboard as tb
import numpy as np
import matplotlib as plt
import os 
#from hotspot.strategies.ai.tf.v_1_00 import optimizer
#from hotspot.strategies.ai.tf.v_1_00 import accuracy
#from hotspot.strategies.ai.tf.v_1_00 import accuracy
#from hotspot.strategies.ai.tf.v_3_00 import calc_accuracy

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
targets_int = tf.placeholder(tf.int32, [None, output_size])
# TensorArr = tf.TensorArray(tf.float32, 1, dynamic_size=True, infer_shape=False)
# targets_unpacked = TensorArr.unstack(targets)
#targets_unpacked_2 = tf.unstack(targets, axis=2)
# targets_unpacked_1 = tf.unstack(targets, axis=1)
# targets_unpacked = tf.unstack(targets_unpacked_1, axis=0)

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

outputs = tf.Print(outputs, [tf.shape(outputs), outputs], "OUPUTS: ", 80)

output_sorted_20, os_indices_20 = tf.nn.top_k(outputs, 20) #gives you top_20
target_sorted_20, ts_indices_20 = tf.nn.top_k(targets, 20)
#matches = tf.reduce_sum(tf.equal(targets[indices_20], 1, "MATCHES"))
#threshold_20 = outputs[indices[20]];
output_sorted = tf.Print(output_sorted_20, [tf.shape(output_sorted_20), output_sorted_20, tf.shape(os_indices_20), os_indices_20], "OUPUT_SORTED: ")
target_sorted = tf.Print(target_sorted_20, [tf.shape(target_sorted_20), target_sorted_20, tf.shape(ts_indices_20), ts_indices_20], "TARGET_SORTED: ")
#output_sorted = tf.Print(output_sorted, [tf.nn.top_k(outputs)], "OUPUT_SORTED: ")


# to get the mean accuracy over all labels, prediction_tensor are scaled logits (i.e. with final sigmoid layer)
correct_prediction = tf.equal( tf.round( outputs ), tf.round( targets ) )
accuracy_1 = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
 
# to get the mean accuracy where all labels need to be correct
all_labels_true = tf.reduce_min(tf.cast(correct_prediction, tf.float32), 1)
accuracy_2 = tf.reduce_mean(all_labels_true)
#match_20 = tf.reduce_sum(tf.equal(os_indices_20, ts_indices_20, name="match20"))

#_,top_20_predictions = tf.nn.in_top_k(outputs, targets, k=20)
#_, top_20_picks =  tf.nn.in_top_k(targets, k=20)
#correct = tf.equal(top_20_predictions, top_20_picks)
#accuracy = tf.reduce_mean(tf.greater_equal(outputs, output_sorted, "Threshold20"))
#loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=outputs, labels=targets))#;
#loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=os_indices_20, labels=ts_indices_20))#;




#loss = tf.nn.softmax_cross_entropy_with_logits_v2(logits=outputs, labels=targets);
#final_tensor = tf.nn.sigmoid(outputs, name="outputs")
#final_tesor = tf.Print(final_tensor, [tf.shape(final_tensor), final_tensor], 'Final tensor: ')

#final_tensor = tf.Print(final_tensor, [final_tensor], "final tensor: ")
#cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(logits=outputs,labels=targets)
# cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=outputs,labels=targets)
# cross_entropy = tf.Print(cross_entropy, [tf.shape(cross_entropy), cross_entropy], 'CROSS ENTROPY: ')


# mean_loss = tf.reduce_mean(cross_entropy) ###### CHECK IF CROSS ENTROPY is the LOSS
# 
# optimizer=tf.train.AdamOptimizer(learning_rate=0.001).minimize(mean_loss);

def calc_accuracy(sess, indices_20, target):
    match_20=0;
    accuracy = []
    print(sess.run(indices_20))
#    x=tf.constant(0);
#     c = lambda x: tf.less(x, 75000)
#     i2 = lambda z: tf.less(z, 19)
#     b = lambda x: tf.reduce_sum(tf.equal(target[x][i2], 1.0))
#     tf.while_loop(c,b,[x])
#     accuracy = []
#     for x in range(75000):
#         #for y in range(len(x)):
#     
# #     sorted_indexes_asc = np.argsort(output)
# #     "Accuracy is calculated"
#         i=0; len=20; # i stops at 79
#         while (i < len):
#             if (target[x][indices_20[i]]==1.0): match_20 += 1;
# #         i+=1;
#         accuracy.append(match_20)
   
    return accuracy;
    
    
##### PLA WITH THIS FOR ACCURACY    
#out_equals_target = tf.equal(tf.arg_max(outputs,1), tf.arg_max(targets,1))



sess = tf.InteractiveSession();
initializer = tf.global_variables_initializer();
sess.run(initializer)


loss = tf.reduce_mean(tf.reduce_sum(tf.cast(tf.equal(os_indices_20, ts_indices_20, "match20"), tf.float32)))
#optimizer = tf.train.AdadeltaOptimizer(learning_rate=0.0001).minimize(loss)
optimizer = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(loss)
# 
grads = tf.gradients(loss, tf.trainable_variables())
grads, _ = tf.clip_by_global_norm(grads, 80) # gradient clipping
grads_and_vars = list(zip(grads, tf.trainable_variables()))
train_op = optimizer.apply_gradients(grads_and_vars)



#accuracy=tf.reduce_mean(tf.cast(calc_accuracy(sess, indices_20, targets), tf.float32))
#accuracy = tf.reduce_mean(tf.cast(calc_accuracy(sess, indices_20, targets_unpacked), tf.float32));
# threshold_20 = output_sorted_20[19]
# accuracy = tf.reduce_sum(tf.greater(outputs, ))/20;

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
        
        #for i in data['train']:
        
        try:
            #print(sess.run([outputs]), feed_dict={inputs: data['train'], targets: data['target']});
            _, batch_loss = sess.run([optimizer, loss], feed_dict={inputs: data['train'], targets: data['target']});
            #correct = sess.run(loss, feed_dict={inputs: data['train'], targets: data['target']})
            print("Losss ", batch_loss)
        except ValueError:
            print("value error")   
        

