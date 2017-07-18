# -*- coding: utf-8 -*-
import math
import sys
import pickle
from collections import defaultdict


class NaiveBayesClassifier:
    def __init__(self):
        self.categories = set()
        self.vocabularies = set()
        self.wordcount = {}
        self.catcount = {}
        self.denominator = {}

    def train(self, data):
        for d in data:
            cat = d["category"]
            self.categories.add(cat)

        for cat in self.categories:
            self.wordcount[cat] = defaultdict(int)
            self.catcount[cat] = 0

        for d in data:
            cat, doc = d["category"], d["vocab"]
            self.catcount[cat] += 1
            for word in doc:
                self.vocabularies.add(word)
                self.wordcount[cat][word] += 1

        # Laplace Smoothing
        for cat in self.categories:
            wordcount_in_cat = sum(self.wordcount[cat].values())
            wordcount_all = len(self.vocabularies)
            self.denominator[cat] = wordcount_in_cat + wordcount_all

    def classify(self, vocab):
        best = None
        max_prob = -sys.maxsize
        for cat in self.catcount.keys():
            p = self._catProb(vocab, cat)
            if p > max_prob:
                max_prob = p
                best = cat
        return best

    def _catProb(self, vocab, cat):
        total = sum(self.catcount.values())
        score = math.log(float(self.catcount[cat]) / total)
        for word in vocab:
            score += math.log(self._wordProb(word, cat))
        return score

    def _wordProb(self, word, cat):
        return float(self.wordcount[cat][word] + 1) / float(self.denominator[cat])

    def score(self, data):
        correct = sum([self.classify(d["vocab"]) == d["category"] for d in data])
        return float(correct) / len(data)

    def save(self):
        with open("m_clf.pickle", "wb") as f:
            pickle.dump(self, f)

    def validate(self):
        pass
