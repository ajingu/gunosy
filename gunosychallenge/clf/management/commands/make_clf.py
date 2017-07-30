import numpy as np
from django.core.management.base import BaseCommand
from sklearn.model_selection import train_test_split
from .preprocess import Preprocess
from clf.models import Article


class Command(BaseCommand):
    """
    A command which makes a classifier.

    Use this class if you want to make a classifier which type is
    either 'NaiveBayes' or 'LogisticRegression'.

    Several arguments affect behaviour.

    ``help``
        A short description of the command, which will be printed in
        help messages.

    ``@method``
        Specify the type of the classifier.
    """
    help = "Make a classifier."

    def add_arguments(self, parser):
        """
        Add a custom argument 'method', which specifies the type of
        the classifier.
        """
        parser.add_argument("method", nargs="+")

    def handle(self, *args, **options):
        """
        Make a classifier which type is
        either NaiveBayes or LogisticRegression.
        """
        if options["method"] == ["nb"]:
            self.stdout.write(self.style.SUCCESS("NaiveBayes"))

            data = Article.objects.values()
            X, y = Preprocess().preprocess(data, "NaiveBayes")
            X_train, X_test, y_train, y_test = train_test_split(X,
                                                                y,
                                                                test_size=0.2,
                                                                stratify=y,
                                                                random_state=4)

            from .NaiveBayes import NaiveBayesClassifier
            clf = NaiveBayesClassifier()
            clf = clf.fit(X_train, y_train)
            clf.save()

            # scores = clf.cross_validate(X, y)
            # print("scores:", scores)
            # print("average value:", np.mean(scores))

            # print(clf.report(X_test, y_test))

            self.stdout.write(self.style.SUCCESS("Succesfully made classfier"))

        elif options["method"] == ["logistic"]:
            self.stdout.write(self.style.SUCCESS("Logistic"))

            data = Article.objects.values()
            X, y = Preprocess().preprocess(data, "Logistic")
            X_train, X_test, y_train, y_test = train_test_split(X,
                                                                y,
                                                                test_size=0.2,
                                                                stratify=y,
                                                                random_state=4)

            from .Logistic import LogisticRegressionClassifier
            clf = LogisticRegressionClassifier()
            clf = clf.fit(X_train, y_train)
            clf.save()

            # scores = clf.cross_validate(X, y)
            # print("scores:", scores)
            # print("average value:", np.mean(scores))

            # print(clf.report(X_test, y_test))

            self.stdout.write(self.style.SUCCESS("Succesfully made classfier"))

        else:
            print("Error: You can select 'nb' or 'logistic'")
