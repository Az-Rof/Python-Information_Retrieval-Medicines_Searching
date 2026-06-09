import string

import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


class PreprocessingText:
    def __init__(self):
        self._ensure_nltk_resources()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def _ensure_nltk_resources(self):
        resources = {
            'punkt': 'tokenizers/punkt',
            'wordnet': 'corpora/wordnet',
            'stopwords': 'corpora/stopwords',
        }

        for name, path in resources.items():
            try:
                nltk.data.find(path)
            except LookupError:
                nltk.download(name)

    def preprocess(self, text):
        text = text.lower()
        tokens = word_tokenize(text)
        processed_tokens = [
            self.lemmatizer.lemmatize(word)
            for word in tokens
            if word not in self.stop_words and word not in string.punctuation
        ]
        return processed_tokens

    def expand_query(self, query_tokens):
        expanded_query = set(query_tokens)
        for word in query_tokens:
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    expanded_query.add(lemma.name())
        return list(expanded_query)
