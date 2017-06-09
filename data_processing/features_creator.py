import threading
from collections import Counter

from news_scraper import Scraper

from data_processing.tokenizer import Tokenizer


class FeaturesCreator:
    def __init__(self, frequency_threshold):
        self.features = []
        self.frequency_threshold = frequency_threshold

    def extract_features(self, files):
        tokens = []
        lock = threading.Lock()
        extractors = []
        for file in files:
            extr = TokensExtractor(file, tokens, lock)
            extr.start()
            extractors.append(extr)

        for e in extractors:
            e.join()

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


class TokensExtractor(threading.Thread):
    def __init__(self, f, tokens, lock):
        super(TokensExtractor, self).__init__()
        self.file = f
        self.tokens = tokens
        self.lock = lock

    def run(self):
        urls = open(self.file).read().splitlines()
        paragraphs = self._extract_paragraphs(urls)
        tks = Tokenizer.tokenize(paragraphs)

        with self.lock:
            self.tokens += tks

    @staticmethod
    def _extract_paragraphs(urls):
        paragraphs = []
        for url in urls:
            try:
                _, _, p = Scraper.scrap_data(url)
                paragraphs += p
            except ConnectionError:
                print("Cannot scrap data for:", url)

        return paragraphs