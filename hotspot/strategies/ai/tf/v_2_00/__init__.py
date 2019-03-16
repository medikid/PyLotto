from hotspot.models import iresult, idraw, idepth;
import tensorflow as tf
import tensorboard as tb
import numpy as np
import matplotlib as plt
import os 

'''
multi-label classification

check https://github.com/tensorflow/skflow/issues/113
https://towardsdatascience.com/multi-label-image-classification-with-inception-net-cbb2ee538e30


1. 0,1,0,0,0,1,1,0 change to 0,0.05,0,0,0,0..05,   1/20=0.05 prob for each positive label

'''
model_name="tf_v_2_00"
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

weights_3 = tf.get_variable("weights_3", [hidden_layer_size, output_size])
biases_3 = tf.get_variable("biases_3", [output_size])
outputs = tf.nn.relu(tf.matmul(outputs_2, weights_3)+biases_3);

#loss = tf.nn.softmax_cross_entropy_with_logits_v2(logits=outputs, labels=targets);
final_tensor = tf.nn.sigmoid(outputs, name="outputs")
cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(logits=outputs,labels=targets)

mean_loss = tf.reduce_mean(cross_entropy) ###### CHECK IF CROSS ENTROPY is the LOSS

optimizer=tf.train.AdamOptimizer(learning_rate=0.001).minimize(mean_loss);

##### PLA WITH THIS FOR ACCURACY    
#out_equals_target = tf.equal(tf.arg_max(outputs,1), tf.arg_max(targets,1))
out_equals_target = tf.equal(tf.round(outputs), targets)

accuracy=tf.reduce_mean(tf.cast(out_equals_target, tf.float32))

sess = tf.InteractiveSession();

initializer = tf.global_variables_initializer();
sess.run(initializer)

batch_size = 100;
max_epochs =  50000;
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
            _, batch_loss = sess.run([optimizer, mean_loss], feed_dict={inputs: data['train'], targets: data['target']});
            cur_epoch_loss += batch_loss;
        except ValueError:
            print("value error")   
        
    #cur_epoch_loss /= train_data.batch_count
    
    validation_loss = 0.
    validation_accuracy = 0.
    
    with np.load(data_folder+'val_75k.npz') as val:
        validation_loss, validation_accuracy = sess.run([mean_loss, accuracy], feed_dict={ inputs: val['val'], targets: val['target']});
    
    
    print('Epoch '+ str(epoch_counter+1)+
            '. Training Loss: '+'{0:.3f}'.format(cur_epoch_loss)+
            '. validation Loss: '+'{0:.3f}'.format(validation_loss)+
            '. validation Accuracy: '+'{0:.2f}'.format(validation_accuracy *100.)+'%')
            
    if validation_loss >= prev_validation_loss:
        break;
    
    prev_validation_loss = validation_loss;
    
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
    test_loss, test_accuracy = sess.run([mean_loss, accuracy], feed_dict={ inputs: test['test'], targets: test['target']});
     
    print('. test Loss: '+'{0:.3f}'.format(test_loss)+
            '. test Accuracy: '+'{0:.2f}'.format(test_accuracy *100.)+'%')
    
