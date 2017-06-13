import random
import threading
import numpy as np
from data_processing.news_scraper import Scraper
from data_processing.tokenizer import Tokenizer
from data_processing.tokens_extractor import TokensExtractor


# classification:
# [legit, fake] - e.g. [1, 0] means legit


class NewsProcessor:
    def __init__(self, lexicon_file):
        self.lexicon = list(open(lexicon_file).read().splitlines())
        self.featureset = []

    def process_newsset(self, legit_files, fake_files):
        legit_extractors = []
        legit_tokens = []
        lock = threading.Lock()
        for file in legit_files:
            extr = TokensExtractor(file, legit_tokens, lock)
            extr.start()
            legit_extractors.append(extr)

            # for url in open(leg).read().splitlines():
            #     legit_tokens.append([])
            #     extr = TokensExtractor(url, legit_tokens[-1], lock)
            #     extr.start()
            #     legit_extractors.append(extr)

        fake_extractors = []
        fake_tokens = []
        for file in fake_files:
            extr = TokensExtractor(file, fake_tokens, lock)
            extr.start()
            fake_extractors.append(extr)

        for extr in legit_extractors:
            extr.join()

        self.tokens_to_features(legit_tokens, [1, 0])

        for extr in fake_extractors:
            extr.join()

        self.tokens_to_features(fake_tokens, [0, 1])
        random.shuffle(self.featureset)

    def tokens_to_features(self, tokensset, classification):
        for tokens in tokensset:
            features = self.count_tokens(tokens)
            features = list(features)
            self.featureset.append([features, classification])


        # _, _, p = Scraper.scrap_data(news_url)
        # words = Tokenizer.tokenize(p)
        # features = np.zeros(len(self.lexicon))
        # for w in words:
        #     if w in self.lexicon:
        #         index = self.lexicon.index(w)
        #         features[index] += 1
        #
        # features = list(features)
        # self.featureset.append([features, classification])

    def count_tokens(self, tokens):
        features = np.zeros(len(self.lexicon))
        for tok in tokens:
            if tok in self.lexicon:
                index = self.lexicon.index(tok)
                features[index] += 1

        return features

    def get_features(self, url): # TODO rename later and make it better with this class
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
