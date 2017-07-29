# -*- coding: utf-8 -*-
import math
import dill
import numpy as np
from collections import defaultdict, Counter
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import classification_report


class NaiveBayesClassifier:
    """
    Naive Bayes classifier for multinomial models.
    """

    def __init__(self, l=None):
        """Initialize the classifier."""
        self.categories = None
        self.denominator = None
        self.n_samples = None
        self.catcount = None
        self.wordcount = defaultdict(lambda: Counter())
        self.l = l

    def fit(self, X_train, y_train):
        """Fit Logistic Regression classifier according to X, y.

        Parameters
        ----------
        X_train : list, shape [n_samples, n_features]
            Training vectors, where n_samples is the number of samples
            and n_features is the number of features.

        y_train : list, shape [n_samples]
            Training Labels, where n_samples is the number of labels.

        Returns
        -------
        self : object
            Returns self.
        """
        self.categories = set(y_train)
        self.n_samples = len(y_train)
        self.catcount = Counter(y_train)
        wordcount_all = len(set(np.concatenate(X_train)))

        for vocab, cat in zip(X_train, y_train):
            self.wordcount[cat] += Counter(vocab)

        # Laplace Smoothing
        self.denominator = {
            cat: wordcount_all + sum(self.wordcount[cat].values())
            for cat in self.categories
        }

        return self

    def predict(self, X):
        """
        Return the array of predicted categories, if X is test data.

        Return a predicted category,
        if X is a word list of the submitted article from the form.
        """
        if isinstance(X[0], list):
            predicted_categories = np.array([
                self._predict_category(vocab)
                for vocab in X
            ])

            return predicted_categories

        elif isinstance(X[0], str):
            best = self._predict_category(X)
            return best

    def _predict_category(self, vocab):
        """Return a predicted category."""
        prob_dict = {
            cat: self._catProb(vocab, cat)
            for cat in self.categories
        }
        best_cat = max(prob_dict, key=(lambda x: prob_dict[x]))
        return best_cat

    def _catProb(self, vocab, cat):
        """
        Return the logarithmic conditional probability, log(P(cat|vocab)).
        """
        log_p_cat = math.log(float(self.catcount[cat]) / self.n_samples)
        log_p_each_word_when_cat = [
            math.log(self._wordProb(word, cat))
            for word in vocab
        ]

        log_p_cat_when_vocab = log_p_cat + sum(log_p_each_word_when_cat)
        return log_p_cat_when_vocab

    def _wordProb(self, word, cat):
        """Return the conditional probability, P(word|cat)."""
        numerator = float(self.wordcount[cat][word] + 1)
        denominator = self.denominator[cat]
        p_word_when_cat = numerator / denominator
        return p_word_when_cat

    def score(self, X_test, y_test):
        """Return the score of accuracy.

        Parameters
        ----------
        X_test : list, shape [n_samples, n_features]
            Test vectors, where n_samples is the number of samples
            and n_features is the number of features.

        y_test : list, shape [n_samples]
            Test labels, where n_samples is the number of labels.

        Returns
        -------
        score : float
            Returns score of accuracy.
        """
        y_pred = self.predict(X_test)
        y_test = np.array(y_test)
        matched_count = sum(y_test == y_pred)
        score = float(matched_count) / len(y_test)
        return score

    def cross_validate(self, X, y):
        """Perform 5-fold Cross-vaidation.

        Parameters
        ----------
        X : list, shape [n_samples, n_features]
            Vectors, where n_samples is the number of samples
            and n_features is the number of features.

        y : list, shape [n_samples]
            Labels, where n_samples is the number of labels.

        Returns
        -------
        scores : list [n_splits]
            Returns scores calculated by the cross validation.
        """
        kf = KFold(n_splits=5, shuffle=True)
        scores = cross_val_score(self, X, y, cv=kf, scoring="accuracy")

        return scores

    def get_params(self, deep=False):
        """The method required for cross-validation."""
        return {'l': self.l}

    def report(self, X_test, y_test):
        """Return a text report showing the classification metrics.

        Parameters
        ----------
        X_test : list, shape [n_samples, n_features]
            Test vectors, where n_samples is the number of samples
            and n_features is the number of features.

        y_test : list, shape [n_samples]
            Test labels, where n_samples is the number of labels.

        Returns
        -------
        report : string
            Returns a classification report.
        """
        y_pred = self.predict(X_test)
        report = classification_report(y_test, y_pred)
        return report

    def save(self):
        """Serialize this classifier by pickling."""
        with open("m_clf.pickle", "wb") as f:
            dill.dump(self, f)
