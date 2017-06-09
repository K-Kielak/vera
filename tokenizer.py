import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


class Tokenizer:
    lemmatizer = WordNetLemmatizer()

    @staticmethod
    def tokenize(paragraphs):
        tokens = []
        for p in paragraphs:
            words = word_tokenize(p)
            tokens += list(words)

        tokens = list(map(Tokenizer._clean, tokens))  # delete every non alphabetical symbol
        tokens = list(Tokenizer.lemmatizer.lemmatize(t) for t in tokens)
        tokens = list(filter(lambda x: len(x) > 1, tokens))
        return tokens

    @staticmethod
    def _clean(word):
        messy_symbols = r"~!@#$%^&*()_+1234567890-=|}{[]\":;'/.,<>?’`"
        for symbol in messy_symbols:
            word = word.replace(symbol, "")

        return word
