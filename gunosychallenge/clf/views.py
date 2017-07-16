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
                text = get_text(request.POST.get("url", "It's error. Please submit the form with 'url'."))
                vocab = Corpus().get_main_words(text)
            
                with open("m_clf.pickle", "rb") as f:
                    nb = pickle.load(f)
                    cat = nb.classify(vocab)
                    return render(request,
                                  'clf/analysis.html',
                                  {'result': cat})
                
            except:
                    return render(request,
                                  'clf/analysis.html',
                                  {'result': "It's error. Please submit a gunosy article"})
            
    else:
        form = ArticleForm()
        return render(request,
                      'clf/form.html',
                      {'form': form})