from django.conf.urls import url
from .views import form

urlpatterns = [
    url(r'^$', form),
]
