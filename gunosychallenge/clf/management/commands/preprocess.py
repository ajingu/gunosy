# -*- coding: utf-8 -*-
import MeCab
import dill
import subprocess
from urllib.request import urlopen
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer


class Preprocess:
    """Class that preprocesses data."""
    def __init__(self):
        """Setup pos, stopwords and the path for the tagger."""
        self.pos = {"名詞", "形容詞"}
        self.stopwords = self._get_stopwords()
        cmd = ["mecab-config --dicdir", "'/mecab-ipadic-neologd'"]
        process = subprocess.run(cmd,
                                 stdout=subprocess.PIPE,
                                 shell=True)

        dir_path = process.stdout.decode("utf-8").strip()

        dic_path = dir_path + "/mecab-ipadic-neologd"

        self.tagger_path = "-d " + dic_path

    def preprocess(self, records, mode):
        """Return X, y.

        Parameters
        ----------
        records : list
            A list of the article items.

        mode : string
            The classifier type, either 'NaiveBayes' or 'Logistic'.

        Returns
        -------
        X : list
            Returns a list of characteristic words of each text.

        y : list
            Returns a list of labels.
        """
        if mode == "NaiveBayes":
            X = []
            y = []
            for record in records:
                X.append(self.get_main_words(record["text"]))
                y.append(record["category"])

            return X, y

        elif mode == "Logistic":
            texts = []
            labels = []
            tokenizer = RegexpTokenizer(r"\w+")
            vectorizer = TfidfVectorizer(tokenizer=tokenizer.tokenize,
                                         stop_words=self.stopwords,
                                         max_df=0.2,
                                         min_df=2)
            for record in records:
                texts.append(" ".join(self.get_main_words(record["text"])))
                labels.append(record["category"])

            X = vectorizer.fit_transform(texts)
            y = labels

            with open("vocab.pickle", "wb") as f:
                dill.dump(vectorizer.vocabulary_, f)

            with open("idfs.pickle", "wb") as f:
                dill.dump(vectorizer.idf_, f)

            return X, y

    def _get_stopwords(self):
        """Return a list of stopwords."""
        slothlib_path = ("http://svn.sourceforge.jp/svnroot/slothlib/CSharp/"
                         "Version1/SlothLib/NLP/Filter/StopWord/word/"
                         "Japanese.txt")
        response = urlopen(slothlib_path)
        stopwords = {line.decode("utf-8").strip() for line in response} - {""}
        return stopwords

    def get_main_words(self, text):
        """Return a list of characteristic words of the text.

        Parameters
        ----------
        text : string
            A text.

        Returns
        -------
        main_words : list
            Returns a list of characteristic words of each text.
        """
        main_words = []
        tagger = MeCab.Tagger(self.tagger_path)
        tagger.parse("")
        node = tagger.parseToNode(text)

        while node:
            word_type = node.feature.split(",")[0]
            word = node.surface
            if word_type in self.pos and word not in self.stopwords:
                main_words.append(word)
            node = node.next

        return main_words
