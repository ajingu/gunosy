from enum import Enum


class Pickles(Enum):
    IDF = "resource/idfs.pickle"
    VOCAB = "resource/vocab.pickle"
    CLF = "resource/m_clf.pickle"


class Params(Enum):
    C = [0.01, 0.1, 1, 10, 100]
    SPLITS = 5
    SHUFFLE = True


class Mode(Enum):
    NB = "NaiveBayes"
    Logistic = "Logistic"


class Morph(Enum):
    POS = {"名詞", "形容詞"}
    CMD = ["mecab-config --dicdir", "'/mecab-ipadic-neologd'"]
    SLOTHLIB = ("http://svn.sourceforge.jp/svnroot/slothlib/CSharp/"
                "Version1/SlothLib/NLP/Filter/StopWord/word/"
                "Japanese.txt")
