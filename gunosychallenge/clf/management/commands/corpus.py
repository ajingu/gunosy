# -*- coding: utf-8 -*-
import MeCab
from enum import Enum, auto


class MethodEnum(Enum):
    NaiveBayes = auto()
    FastText = auto()
        

class Corpus:
    def __init__(self):
        self.pos = {"名詞", "形容詞"}
    
    def corpus(self, records, mode):
        corpus = []
        if mode == MethodEnum.NaiveBayes:
            for record in records:
                data = {}
                data["category"] = record["category"]
                data["vocab"] = self.get_main_words(record["text"])
                corpus.append(data)
                
        elif mode == MethodEnum.FastText:
            for record in records:
                data = {}
                data["category"] = record["category"]
                data["text"] = self.split_words(record["text"])
                corpus.append(data)
        
        else:
            return "Error: You can select 'NaiveBayes' or 'fasttext'"
        
        return corpus
        
    def get_main_words(self, text):
        out_words = []
        tagger = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
        tagger.parse("")
        node = tagger.parseToNode(text)
    
        while node:
            word_type = node.feature.split(",")[0]
            if word_type in self.pos:
                out_words.append(node.surface)
            node = node.next    
        
        return out_words
    
    def split_words(self, text):
        tagger = MeCab.Tagger("-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
        splitted_sent = tagger.parse(text)
        return splitted_sent