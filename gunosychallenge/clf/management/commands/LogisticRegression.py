# -*- coding: utf-8 -*-
import dill
import scipy.sparse as sp
from sklearn.model_selection import cross_val_score, KFold, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer


class Logistic:
    """
    Logistic Regression classifier for multiclass.
    """

    def __init__(self):
        """Initialize the classifier and the vectorizer."""
        self.clf = LogisticRegression(class_weight="balanced")

        self.vectorizer = MyVectorizer()
        m_idfs = self.vectorizer.idfs
        self.vectorizer._tfidf._idf_diag = sp.spdiags(m_idfs,
                                                      diags=0,
                                                      m=len(m_idfs),
                                                      n=len(m_idfs))

    def fit(self, X_train, y_train):
        """Fit Logistic Regression classifier according to X, y.

        Use GridSearchCV to search the optimized parameter values for 'C'.

        Parameters
        ----------
        X_train : {array-like, sparse matrix}, shape [n_samples, n_features]
            Training vectors, where n_samples is the number of samples
            and n_features is the number of features.

        y_train : array-like, shape [n_samples]
            Training Labels, where n_samples is the number of labels.

        Returns
        -------
        self : object
            Returns self.
        """
        cs = [0.01, 0.1, 1, 10, 100]

        parameters = {"C": cs}

        self.clf = GridSearchCV(self.clf, parameters)

        self.clf.fit(X_train, y_train)
        print(self.clf.best_estimator_)

        return self

    def score(self, X_test, y_test):
        """Return the score of accuracy.

        Parameters
        ----------
        X_test : {array-like, sparse matrix}, shape [n_samples, n_features]
            Test vectors, where n_samples is the number of samples
            and n_features is the number of features.

        y_test : array-like, shape [n_samples]
            Test labels, where n_samples is the number of labels.

        Returns
        -------
        score : float
            Returns score of accuracy.
        """
        score = self.clf.score(X_test, y_test)
        return score

    def predict(self, words):
        """Return a predicted category."""
        text = " ".join(words)
        X = self.vectorizer.transform([text])
        category = self.clf.predict(X)[0]
        return category

    def validate(self, X, y):
        """Perform 5-fold Cross-vaidation.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape [n_samples, n_features]
            Vectors, where n_samples is the number of samples
            and n_features is the number of features.

        y : array-like, shape [n_samples]
            Labels, where n_samples is the number of labels.

        Returns
        -------
        scores : list [n_splits]
            Returns scores calculated by the cross validation.
        """
        kf = KFold(n_splits=5, shuffle=True)
        scores = cross_val_score(self.clf, X, y, cv=kf)

        return scores

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
        y_pred = self.clf.predict(X_test)
        report = classification_report(y_test, y_pred)
        return report

    def save(self):
        """Serialize this classifier by pickling."""
        with open("m_clf.pickle", "wb") as f:
            dill.dump(self, f)


class MyVectorizer(TfidfVectorizer):
    """Extension of the TfidfVectorizer."""
    with open("idfs.pickle", "rb") as f:
        idfs = dill.load(f)

    with open("vocab.pickle", "rb") as f:
        vocabulary = dill.load(f)

    TfidfVectorizer.idf_ = idfs
    TfidfVectorizer.vocabulary_ = vocabulary
