from clf.utils.consts import Resources
from clf.utils.preprocess import Preprocess

import dill

from django.shortcuts import render

from .forms import ArticleForm
from .http_request import get_text


def form(request):
    """
    Submit an article url, and Return a predicted category or an error message.

    Returned Context
    -------
    ``result``
        A predicted category or an error message.

    Returned Template
    --------
    `clf/analysis.html`
    """
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            try:
                url = request.POST.get("url")
                text = get_text(url)
                words = Preprocess().get_main_words(text)

                with open(Resources.CLF.value, "rb") as f:
                    clf = dill.load(f)

                category = clf.predict(words)
                return render(request,
                              'clf/analysis.html',
                              {'result': category})

            except Exception as e:
                print(e)
                return render(request,
                              'clf/analysis.html',
                              {'result': "Please submit a gunosy article"})

    else:
        form = ArticleForm()
        return render(request,
                      'clf/form.html',
                      {'form': form})
