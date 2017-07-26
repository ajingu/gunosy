# -*- coding: utf-8 -*-
import math
import sys
import dill
from collections import defaultdict
from sklearn.metrics import classification_report


class NaiveBayesClassifier:
    """
    Naive Bayes classifier for multinomial models.
    """

    def __init__(self):
        """Initialize the classifier."""
        self.categories = set()
        self.vocabularies = set()
        self.wordcount = defaultdict(lambda: defaultdict(int))
        self.catcount = defaultdict(int)
        self.denominator = {}

    def fit(self, X_train, y_train):
        """Fit Logistic Regression classifier according to X, y.

        Parameters
        ----------
        X_train : array-like, shape [n_samples, n_features]
            Training vectors, where n_samples is the number of samples
            and n_features is the number of features.

        y_train : array-like, shape [n_samples]
            Training Labels, where n_samples is the number of labels.

        Returns
        -------
        self : object
            Returns self.
        """
        self.categories = set(y_train)
        self.n_samples = len(y_train)

        for vocab, cat in zip(X_train, y_train):
            self.catcount[cat] += 1
            for word in vocab:
                self.vocabularies.add(word)
                self.wordcount[cat][word] += 1

        # Laplace Smoothing
        wordcount_all = len(self.vocabularies)
        for cat in self.categories:
            wordcount_in_cat = sum(self.wordcount[cat].values())
            self.denominator[cat] = wordcount_in_cat + wordcount_all

        return self

    def predict(self, vocab):
        """Return a predicted category."""
        best = None
        max_prob = -sys.maxsize
        for cat in self.catcount.keys():
            p = self._catProb(vocab, cat)
            if p > max_prob:
                max_prob = p
                best = cat
        return best

    def _catProb(self, vocab, cat):
        """Return the logarithmic conditional probability, log(P(cat|vocab))."""
        score = math.log(float(self.catcount[cat]) / self.n_samples)
        for word in vocab:
            score += math.log(self._wordProb(word, cat))
        return score

    def _wordProb(self, word, cat):
        """Return the conditional probability, P(word|cat)."""
        numerator = float(self.wordcount[cat][word] + 1)
        denominator = self.denominator[cat]
        wordProb = numerator / denominator
        return wordProb

    def score(self, X_test, y_test):
        """Return the score of accuracy.

        Parameters
        ----------
        X_test : array-like, shape [n_samples, n_features]
            Test vectors, where n_samples is the number of samples
            and n_features is the number of features.

        y_test : array-like, shape [n_samples]
            Test labels, where n_samples is the number of labels.

        Returns
        -------
        score : float
            Returns score of accuracy.
        """
        bool_matched = [
            self.predict(vocab) == cat
            for vocab, cat in zip(X_test, y_test)
        ]
        num_matched = sum(bool_matched)
        score = float(num_matched) / len(y_test)
        return score

    def report(self, X_test, y_test):
        """Return a text report showing the classification metrics.

        Parameters
        ----------
        X_test : {array-like, sparse matrix}, shape [n_samples, n_features]
            Test vectors, where n_samples is the number of samples
            and n_features is the number of features.

        y_test : array-like, shape [n_samples]
            Test labels, where n_samples is the number of labels.

        Returns
        -------
        report : string
            Returns a classification report.
        """
        y_pred = [self.predict(vocab) for vocab in X_test]
        report = classification_report(y_test, y_pred)
        return report

    def save(self):
        """Serialize this classifier by pickling."""
        with open("m_clf.pickle", "wb") as f:
            dill.dump(self, f)
