# -*- coding: utf-8 -*-
import MeCab
import dill
import subprocess
from urllib.request import urlopen
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer


class Corpus:
    """Class that creates corpora."""
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

    def corpus(self, rows, mode):
        """Return X, y.

        Parameters
        ----------
        rows : list
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
            for row in rows:
                X.append(self.get_main_words(row["text"]))
                y.append(row["category"])

            return X, y

        elif mode == "Logistic":
            words = []
            labels = []
            tokenizer = RegexpTokenizer(r"\w+")
            vectorizer = TfidfVectorizer(tokenizer=tokenizer.tokenize,
                                         stop_words=self.stopwords,
                                         max_df=0.2,
                                         min_df=2)
            for row in rows:
                words.append(" ".join(self.get_main_words(row["text"])))
                labels.append(row["category"])

            X = vectorizer.fit_transform(words)
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
        res = urlopen(slothlib_path)
        stopwords = {line.decode("utf-8").strip() for line in res} - {""}
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
