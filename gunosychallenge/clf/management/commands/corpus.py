# -*- coding: utf-8 -*-
import MeCab
import pickle
import subprocess
from urllib.request import urlopen
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.tokenize import RegexpTokenizer


class Corpus:
    def __init__(self):
        self.pos = {"名詞", "形容詞"}
        self.stopwords = self.get_stopwords()
        cmd = ["mecab-config --dicdir", "'/mecab-ipadic-neologd'"]
        dir_path = subprocess.run(cmd,
                                  stdout=subprocess.PIPE,
                                  shell=True).stdout.decode("utf-8").strip()

        dic_path = dir_path + "/mecab-ipadic-neologd"

        self.tagger_path = "-d " + dic_path
        self.wakati_tagger_path = "-Owakati -d " + dic_path

    def corpus(self, records, mode):

        if mode == "NaiveBayes":
            corpus = []
            for record in records:
                data = {}
                data["category"] = record["category"]
                data["vocab"] = self.get_main_words(record["text"])
                corpus.append(data)

            return corpus

        elif mode == "svm":
            words = []
            labels = []
            for record in records:
                words.append(self.get_main_words(record["text"]))
                labels.append(record["category"])

            return words, labels

        elif mode == "logistic":
            words = []
            labels = []
            tokenizer = RegexpTokenizer(r"\w+")
            vectorizer = TfidfVectorizer(tokenizer=tokenizer.tokenize,
                                         stop_words=self.stopwords)
            for record in records:
                words.append(" ".join(self.get_main_words(record["text"])))
                labels.append(record["category"])
            X = vectorizer.fit_transform(words)
            y = labels

            print(vectorizer.vocabulary_)
            with open("vocab.pickle", "wb") as f:
                pickle.dump(vectorizer.vocabulary_, f)

            with open("idfs.pickle", "wb") as f:
                pickle.dump(vectorizer.idf_, f)

            return X, y

        else:
            print("Error: You can select 'NaiveBayes' or 'svm'")

    def get_stopwords(self):
        slothlib_path = ("http://svn.sourceforge.jp/svnroot/slothlib/CSharp/"
                         "Version1/SlothLib/NLP/Filter/StopWord/word/"
                         "Japanese.txt")
        res = urlopen(slothlib_path)
        stopwords = {line.decode("utf-8").strip() for line in res} - {""}
        return stopwords

    def get_main_words(self, text):
        out_words = []
        tagger = MeCab.Tagger(self.tagger_path)
        tagger.parse("")
        node = tagger.parseToNode(text)

        while node:
            word_type = node.feature.split(",")[0]
            word = node.surface
            if word_type in self.pos and word not in self.stopwords:
                out_words.append(word)
            node = node.next

        return out_words

    def split_words(self, text):
        tagger = MeCab.Tagger(self.wakati_tagger_path)
        splitted_sent = tagger.parse(text)
        return splitted_sent
