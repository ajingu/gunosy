from django.core.management.base import BaseCommand
from sklearn.model_selection import train_test_split
from .corpus import Corpus
from .NaiveBayesClassifier import NaiveBayesClassifier
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
            data_train, data_test = train_test_split(corpus, test_size=0.2, random_state=42)
            nb = NaiveBayesClassifier()
            nb.train(data_train)
            nb.save()
            print("accuracy:", nb.score(data_test))

            self.stdout.write(self.style.SUCCESS("Succesfully made classfier"))

        if options["method"] == ["doc2vec"]:
            self.stdout.write(self.style.SUCCESS("doc2vec"))
            self.stdout.write(self.style.SUCCESS("Succesfully made classfier"))
