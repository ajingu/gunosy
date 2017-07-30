"""
Register Article Models into django app.
"""
from django.contrib import admin
from .models import Article

admin.site.register(Article)
