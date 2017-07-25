from django import forms


class ArticleForm(forms.Form):
    """Base class for all forms."""
    url = forms.URLField()
