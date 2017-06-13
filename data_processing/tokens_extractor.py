import threading
from data_processing.tokenizer import Tokenizer
from data_processing.news_scraper import Scraper


class TokensExtractor(threading.Thread):
    def __init__(self, file, tokens, lock):
        super(TokensExtractor, self).__init__()
        self.file = file
        self.tokens = tokens
        self.lock = lock

    def run(self):
        urls = open(self.file).read().splitlines()
        tokens = []
        for url in urls:
            try:
                print(self.name, "Scraping:", url)
                _, _, p = Scraper.scrap_data(url)  # TODO implement extracting other features (name, format, title)
                # print(self.name, "Scraped:", url)
                tks = Tokenizer.tokenize(p)
                tokens.append(tks)
            except TimeoutError:
                print("time out for:", url)
            except Exception:
                print("Cannot scrap data for:", url)

        # print(self.name, "want to lock the lock")
        with self.lock:
            # print(self.name, "locked the lock")
            self.tokens += tokens
            # print(self.name, "unlocked the lock")

    # @staticmethod
    # def get_tokens(url):
    #     urls = open(file).read().splitlines()
    #     tokens = []
    #     lock = threading.Lock()
    #     extractors = []
    #     for url in urls:
    #         extr = TokensExtractor(url, tokens, lock)
    #         extr.start()
    #         extractors.append(extr)
    #
    #     for extr in extractors:
    #         extr.join()
    #
    #     return tokens



