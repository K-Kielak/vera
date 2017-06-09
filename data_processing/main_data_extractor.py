import pickle

import numpy as np
from news_processor import NewsProcessor

from data_processing.features_creator import FeaturesCreator

# TODO optimize by making sure data is scraped only one time for both lexicon and training set

#parameters
raw_path = '../raw_data/'
prepared_path = '../prepared_data/'
legit_news = raw_path + 'legit.raw'
fake_news = raw_path + 'fake.raw'
lexicon_path = prepared_path + 'lexicon.data'
training_set = prepared_path + "trainingset.data"

# # creating lexicon
# fc = FeaturesCreator(10)
# fc.extract_features([legit_news, fake_news])
# fc.save_features(lexicon_path)
# print('Lexicon length:', len(fc.features))

#creating training set
processor = NewsProcessor(lexicon_path)
processor.process_newsset([legit_news], [fake_news])
print(processor.featureset)
features = np.asarray(processor.featureset)
train_x = list(features[:,0])
train_y = list(features[:,1])
with open(training_set, 'wb') as f:
    pickle.dump([train_x, train_y], f)