from features_creator import FeaturesCreator
from news_processor import NewsProcessor
import numpy as np
import pickle

#parameters
legit_news_files = ['raw_data/legit.raw']
fake_news_files = ['raw_data/fake.raw']

# creating lexicon
fc = FeaturesCreator(10)
fc.extract_features(['raw_data/legit.raw', 'raw_data/fake.raw'])
fc.save_features("prepared_data/lexicon.data")
print('Lexicon length:', len(fc.features))


processor = NewsProcessor('prepared_data/lexicon.data')
processor.process_newsset(['raw_data/legit.raw'], ['raw_data/fake.raw'])
print(processor.featureset)

features = np.asarray(processor.featureset)
train_x = list(features[:,0])
train_y = list(features[:,1])
with open('prepared_data/trainingset.data', 'wb') as f:
    pickle.dump([train_x, train_y], f)