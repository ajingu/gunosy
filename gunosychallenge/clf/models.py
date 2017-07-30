from django.db import models


class Article(models.Model):
    """Base Model of all Article Items."""
    text = models.TextField()
    category = models.CharField(max_length=100)

    def __str__(self):
        """Return the article text."""
        return self.text
