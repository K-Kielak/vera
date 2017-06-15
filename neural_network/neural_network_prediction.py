import numpy as np
import tensorflow as tf
from data_processing.news_processor import NewsProcessor

class Prediction:
    news_proc = NewsProcessor('prepared_data/lexicon.data')
    input_size = len(news_proc.lexicon)
    # nn = NeuralNetwork(input_size, int(input_size/2),  2)
    # x = tf.placeholder('float', [None, input_size])
    # y = tf.placeholder('float')

    def is_fake(url):
        features = Prediction.news_proc.get_features(url)
        features = np.asarray(features)
        with tf.Session() as sess:
            # session initialization
            saver = tf.train.import_meta_graph('model/first_model.ckpt.meta')
            saver.restore(sess,tf.train.latest_checkpoint('model'))
            #sess.run(tf.global_variables_initializer()) # THAT WAS HUGE ERROR, LEAVE IT FOR OUR CHILDREN TO SEE WHAT YOU ARE NOT ALLOWED TO DO
            graph = tf.get_default_graph()
            x = graph.get_tensor_by_name("x:0")
            print("x:\n", x)
            prediction = graph.get_tensor_by_name("prediction:0")
            print("prediction:\n", prediction.eval({x: np.array(features).reshape(1, Prediction.input_size)}))
            classification = tf.argmax(prediction, 1)
            classification = classification.eval({x: np.array(features).reshape(1, Prediction.input_size)})
            if classification[0] < 0.5:
                print("This news is legit")
                return False
            else:
                print("This is probably fake news")
                return True
