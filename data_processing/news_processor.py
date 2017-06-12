import random

import numpy as np
from data_processing.news_scraper import Scraper

from data_processing.tokenizer import Tokenizer


# classification:
# [legit, fake] - e.g. [1, 0] means legit


class NewsProcessor:
    def __init__(self, lexicon_file):
        self.lexicon = list(open(lexicon_file).read().splitlines())
        self.featureset = []

    def process_newsset(self, legits, fakes):
        for leg in legits:
            for url in open(leg).read().splitlines():
                try:
                    self.process_news(url, [1.0, 0.0])
                except Exception:
                    print('Connection error:', url)

        for fak in fakes:
            for url in open(fak).read().splitlines():
                try:
                    self.process_news(url, [0.0, 1.0])
                except Exception:
                    print('Cannot scrap:', url)

        random.shuffle(self.featureset)

    def process_news(self, news_url, classification):
        _, _, p = Scraper.scrap_data(news_url)
        words = Tokenizer.tokenize(p)
        features = np.zeros(len(self.lexicon))
        for w in words:
            if w in self.lexicon:
                index = self.lexicon.index(w)
                features[index] += 1

        features = list(features)
        self.featureset.append([features, classification])

    def get_features(self, url): # rename later and make it better with this class
        _, _, p = Scraper.scrap_data(url)
        words = Tokenizer.tokenize(p)
        features = np.zeros(len(self.lexicon))
        for w in words:
            if w in self.lexicon:
                index = self.lexicon.index(w)
                features[index] += 1

        features = list(features)
        features = np.asarray(features)
        return list(features)
