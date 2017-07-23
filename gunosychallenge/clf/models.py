from django.db import models


class Article(models.Model):
    text = models.TextField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title
