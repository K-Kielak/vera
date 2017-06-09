import tensorflow as tf
import numpy as np
import pickle
from neural_network_model import NeuralNetwork
from news_processor import NewsProcessor


# initialization
train_x, train_y = pickle.load(open("prepared_data/trainingset.data", "rb"))
# print(train_x)
# print(train_y)
input_data_size = len(train_x[0])
nn = NeuralNetwork(input_data_size, 2, int(input_data_size/2))
# batch_size = 10 # uncomment when data set is large enough
epochs = 100
x = tf.placeholder('float', [None, input_data_size], name='x')
y = tf.placeholder('float', name='y')
print('Data initialized')


# actual code
def train_neural_network(x):
    prediction = nn.neural_network_model(x)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
    optimizer = tf.train.AdamOptimizer().minimize(cost)
    print("Neural network set up")

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print("Variables initialized")
        for e in range(epochs):
            batch_x = np.array(train_x)
            batch_y = np.array(train_y)
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_x, y: batch_y})
            # print('Epoch', e+1, '/', epochs, 'completed')
            correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
            accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
            print('Accuracy:', accuracy.eval({x: train_x, y: train_y}))

        # url = 'http://thugify.com/trump-offering-free-flights-to-mexico-and-africa/' # TODO delete all of this
        # news_proc = NewsProcessor("prepared_data/lexicon.data")
        # feats = news_proc.get_features(url)
        # classification = tf.argmax(prediction, 1)
        # classification = classification.eval({x: np.array(feats).reshape(1, 363)})
        # if classification[0] < 0.5:
        #     print("This news is legit")
        # else:
        #     print("This is probably fake news")
        #
        # print(classification)
        # # TODO up to this point
        saver = tf.train.Saver()
        save_path = saver.save(sess, 'model/first_model.ckpt')
        print(save_path)


train_neural_network(x)