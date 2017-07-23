# -*- coding: utf-8 -*-
import pickle
import scipy.sparse as sp
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer


class Logistic:
    def __init__(self):
        self.clf = OneVsRestClassifier(LogisticRegression())
        with open("vocab.pickle", "rb") as f:
            self.vocabulary = pickle.load(f)

        with open("idfs.pickle", "rb") as f:
            idfs = pickle.load(f)

        self.vectorizer = MyVectorizer()
        self.vectorizer._tfidf._idf_diag = sp.spdiags(idfs,
                                                      diags=0,
                                                      m=len(idfs),
                                                      n=len(idfs))
        self.vectorizer.vocabulary_ = self.vocabulary

    def train(self, X_train, y_train):
        self.clf.fit(X_train, y_train)

    def score(self, X_test, y_test):
        score = self.clf.score(X_test, y_test)
        return score

    def predict(self, words):
        text = " ".join(words)
        X = self.vectorizer.transform([text])
        cat = self.clf.predict(X)[0]
        return cat

    def validate(self, X, y):
        kf = KFold(n_splits=5, shuffle=True)

        scores = cross_val_score(self.clf, X, y, cv=kf)

        return scores

    def report(self, X_test, y_test):
        y_pred = self.clf.predict(X_test)
        report = classification_report(y_test, y_pred)
        return report

    def save(self):
        with open("m_clf.pickle", "wb") as f:
            pickle.dump(self, f)


class MyVectorizer(TfidfVectorizer):
    with open("idfs.pickle", "rb") as f:
        idfs = pickle.load(f)

    TfidfVectorizer.idf_ = idfs
