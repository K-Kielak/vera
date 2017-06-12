import pickle

import numpy as np
from data_processing.news_processor import NewsProcessor

from data_processing.lexicon_creator import LexiconCreator

# TODO optimize by making sure data is scraped only one time for both lexicon and training set

#parameters
raw_path = '../raw_data/'
prepared_path = '../prepared_data/'
legit_news = raw_path + 'legit.raw'
fake_news = raw_path + 'fake.raw'
lexicon_path = prepared_path + 'lexicon.data'
training_set = prepared_path + "trainingset.data"
test_size = 0.2

# creating lexicon
lc = LexiconCreator(50)
lc.extract_features([legit_news, fake_news])
lc.save_features(lexicon_path)
print('Lexicon length:', len(lc.features))

#creating training set
processor = NewsProcessor(lexicon_path)
processor.process_newsset([legit_news], [fake_news])
print(processor.featureset)
features = np.asarray(processor.featureset)
training_size = int(test_size*len(features))
train_x = list(features[:,0][:-training_size])
train_y = list(features[:,1][:-training_size])
test_x = list(features[:,0][-training_size:])
test_y = list(features[:,1][-training_size:])
with open(training_set, 'wb') as f:
    pickle.dump([train_x, train_y, test_x, test_y], f)