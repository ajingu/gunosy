from django.core.management.base import BaseCommand
from sklearn.model_selection import train_test_split
from .corpus import Corpus
from .NaiveBayesClassifier import NaiveBayesClassifier
from .svm import SVM
from clf.models import Article


class Command(BaseCommand):
    help = "make classifier"

    def add_arguments(self, parser):
        parser.add_argument("method", nargs="+")

    def handle(self, *args, **options):

        if options["method"] == ["naivebayes"]:
            self.stdout.write(self.style.SUCCESS("naivebayes"))

            data = Article.objects.values()
            corpus = Corpus().corpus(data, "NaiveBayes")
            data_train, data_test = train_test_split(corpus,
                                                     test_size=0.2,
                                                     random_state=42)
            nb = NaiveBayesClassifier()
            nb.train(data_train)
            nb.save()
            print("accuracy:", nb.score(data_test))

            self.stdout.write(self.style.SUCCESS("Succesfully made classfier"))

        if options["method"] == ["svm"]:
            self.stdout.write(self.style.SUCCESS("svm"))
            data = Article.objects.values()
            X_res, y_res = Corpus().corpus(data, "svm")
            X_train, X_test, y_train, y_test = train_test_split(X_res,
                                                                y_res,
                                                                test_size=0.2,
                                                                stratify=y_res,
                                                                random_state=7)

            svm = SVM()
            svm.train(X_train, y_train)

            print(svm.score(X_test, y_test))

            self.stdout.write(self.style.SUCCESS("Succesfully made classfier"))

        if options["method"] == ["logistic"]:
            self.stdout.write(self.style.SUCCESS("logistic"))
            data = Article.objects.values()
            X_res, y_res = Corpus().corpus(data, "logistic")
            X_train, X_test, y_train, y_test = train_test_split(X_res,
                                                                y_res,
                                                                test_size=0.2,
                                                                stratify=y_res,
                                                                random_state=4)
            
            from .LogisticRegression import Logistic

            logistic = Logistic()
            logistic.train(X_train, y_train)
            logistic.save()

            print(logistic.report(X_test, y_test))

            self.stdout.write(self.style.SUCCESS("Succesfully made classfier"))
