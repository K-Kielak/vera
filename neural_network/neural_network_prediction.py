import numpy as np
import tensorflow as tf
from data_processing.news_processor import NewsProcessor

class Prediction:
    news_proc = NewsProcessor('../prepared_data/lexicon.data')
    input_size = len(news_proc.lexicon)
    # nn = NeuralNetwork(input_size, int(input_size/2),  2)
    # x = tf.placeholder('float', [None, input_size])
    # y = tf.placeholder('float')

    @staticmethod
    def is_fake(url):
        features = Prediction.news_proc.get_features(url)
        features = np.asarray(features)
        with tf.Session() as sess:
            # session initialization
            saver = tf.train.import_meta_graph('../model/first_model.ckpt.meta')
            saver.restore(sess,tf.train.latest_checkpoint('../model'))
            sess.run(tf.global_variables_initializer())
            graph = tf.get_default_graph()
            x = graph.get_tensor_by_name("x:0")
            prediction = graph.get_tensor_by_name("prediction:0")
            classification = tf.argmax(prediction, 1)
            classification = classification.eval({x: np.array(features).reshape(1, Prediction.input_size)})
            if classification[0] < 0.5:
                print("This news is legit", classification)
                return False
            else:
                print("This is probably fake news", classification)
                return True

     # url = '' # TODO delete all of this
     #        classification = tf.argmax(prediction, 1)
     #        classification = classification.eval({x: np.array(feats).reshape(1, 363)})
     #        if classification[0] < 0.5:
     #            print("This news is legit")
     #        else:
     #            print("This is probably fake news")
     #
     #        print(classification)
     #        # TODO up to this point
