import tensorflow as tf


class NeuralNetwork:

    def __init__(self, input_size, classes, *hidden_sizes):
        self.input_size = input_size
        self.classes = classes
        self.hidden_sizes = hidden_sizes

    def neural_network_model(self, data):
        hiddens = [{'weights': tf.Variable(tf.random_normal([self.input_size, self.hidden_sizes[0]])),
                    'biases': tf.Variable(tf.random_normal([self.hidden_sizes[0]]))}]

        for i in range(1, len(self.hidden_sizes)):
            hiddens.append({'weights': tf.Variable(tf.random_normal([self.hidden_sizes[i-1], self.hidden_sizes[i]])),
                            'biases': tf.Variable(tf.random_normal([self.hidden_sizes[i]]))})

        # hidden2 = {'weights': tf.Variable(tf.random_normal([hidden1_size, hidden2_size])),
        #            'biases': tf.Variable(tf.random_normal([hidden2_size]))}
        #
        # hidden3 = {'weights': tf.Variable(tf.random_normal([hidden2_size, hidden3_size])),
        #            'biases': tf.Variable(tf.random_normal([hidden3_size]))}
        #
        # hidden4 = {'weights': tf.Variable(tf.random_normal([hidden3_size, hidden4_size])),
        #            'biases': tf.Variable(tf.random_normal([hidden4_size]))}

        output = {'weights': tf.Variable(tf.random_normal([self.hidden_sizes[-1], self.classes])),
                  'biases': tf.Variable(tf.random_normal([self.classes]))}

        weighted_sums = [tf.add(tf.matmul(data, hiddens[0]['weights']), hiddens[0]['biases'])]
        activations = [tf.nn.relu(weighted_sums[0])]

        for i in range(1, len(hiddens)):
            weighted_sums.append(tf.add(tf.matmul(activations[i-1], hiddens[i]['weights']), hiddens[i]['biases']))
            activations.append(tf.nn.relu(weighted_sums[i]))

        # weighted_sum2 = tf.add(tf.matmul(activation1, hidden2['weights']), hidden2['biases'])
        # activation2 = tf.nn.relu(weighted_sum2)
        #
        # weighted_sum3 = tf.add(tf.matmul(activation2, hidden3['weights']), hidden3['biases'])
        # activation3 = tf.nn.relu(weighted_sum3)

        # weighted_sum4 = tf.add(tf.matmul(activation3, hidden4['weights']), hidden4['biases'])
        # activation4 = tf.nn.relu(weighted_sum4)

        output_sum = tf.add(tf.matmul(activations[-1], output['weights']), output['biases'], name="prediction")
        return output_sum
