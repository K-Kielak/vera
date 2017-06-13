import threading
from collections import Counter
from data_processing.tokens_extractor import TokensExtractor


class LexiconCreator:
    def __init__(self, frequency_threshold):
        self.features = []
        self.frequency_threshold = frequency_threshold

    def extract_features(self, files):
        tokensset = []
        lock = threading.Lock()
        extractors = []
        for file in files:
            extr = TokensExtractor(file, tokensset, lock)
            extr.start()
            extractors.append(extr)

        for extr in extractors:
            extr.join()

        tokens = []
        for tks in tokensset:
            tokens += tks

        self.features = self._get_frequent_tokens(tokens)

    def save_features(self, file):
        with open(file, 'w') as fi:
            for feat in self.features:
                fi.write(feat + "\n")

    def _get_frequent_tokens(self, tokens):
        frequent_tokens = []
        tokens_count = Counter(tokens)
        for t in tokens_count:
            if tokens_count[t] > self.frequency_threshold:
                frequent_tokens.append(t)

        return frequent_tokens
