import pickle

import numpy as np
from data_processing.news_processor import NewsProcessor

from data_processing.lexicon_creator import LexiconCreator

# TODO optimize by making sure data is scraped only one time for both lexicon and training set

#parameters
raw_path = '../raw_data/'
prepared_path = '../prepared_data/'
legit_news1 = raw_path + 'legit1.raw'
fake_news1 = raw_path + 'fake1.raw'
legit_news2 = raw_path + 'legit2.raw'
fake_news2 = raw_path + 'fake2.raw'
lexicon_path = prepared_path + 'lexicon.data'
training_set = prepared_path + "trainingset.data"
test_size = 0.2

# # creating lexicon
# lc = LexiconCreator(80)
#
# lc.extract_features([legit_news1, fake_news1, legit_news2, fake_news2])
# lc.save_features(lexicon_path)
# print('Lexicon length:', len(lc.features))

#creating training set
processor = NewsProcessor(lexicon_path)
processor.process_newsset([legit_news1, legit_news2], [fake_news1, fake_news2])
print(processor.featureset)

features = np.asarray(processor.featureset)
ys = features[:,1]
real_news = 0
fake_news = 0
for y in ys:
    if y[0] is 1 and y[1] is 0:
        real_news += 1
    elif y[0] is 0 and y[1] is 1:
        fake_news += 1
    else:
        print(y[1])

print("real news in the featureset:", real_news)
print("fake news in the featureset:", fake_news)
training_size = int(test_size*len(features))
train_x = list(features[:,0][:-training_size])
train_y = list(features[:,1][:-training_size])
test_x = list(features[:,0][-training_size:])
test_y = list(features[:,1][-training_size:])
with open(training_set, 'wb') as f:
    pickle.dump([train_x, train_y, test_x, test_y], f)