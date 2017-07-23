from django.shortcuts import render
from .forms import ArticleForm
from .httpRequest import get_text
from .management.commands.corpus import Corpus
import pickle

clf = None


def form(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            try:
                url = request.POST.get("url")
                text = get_text(url)
                words = Corpus().get_main_words(text)


                with open("m_clf.pickle", "rb") as f:
                    clf = pickle.load(f)

                cat = clf.predict(words)
                return render(request,
                              'clf/analysis.html',
                              {'result': cat})

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
