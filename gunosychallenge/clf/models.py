from django.db import models


class Article(models.Model):
    """Store a single article."""
    text = models.TextField()
    category = models.CharField(max_length=100)

    def __str__(self):
        """Return the article title."""
        return self.text
