# -*- coding: utf-8 -*-
import MeCab
import subprocess
from enum import Enum


class MethodEnum(Enum):
    NaiveBayes = "NaiveBayes"
    FastText = "FastText"


class Corpus:
    def __init__(self):
        self.pos = {"名詞", "形容詞"}
        cmd = ["mecab-config --dicdir", "'/mecab-ipadic-neologd'"]
        dir_path = subprocess.run(cmd,
                                  stdout=subprocess.PIPE,
                                  shell=True).stdout.decode("utf-8").strip()

        dic_path = dir_path + "/mecab-ipadic-neologd"

        self.tagger_path = "-d " + dic_path
        self.wakati_tagger_path = "-Owakati -d " + dic_path

    def corpus(self, records, mode):
        corpus = []
        if mode == MethodEnum.NaiveBayes.value:
            for record in records:
                data = {}
                data["category"] = record["category"]
                data["vocab"] = self.get_main_words(record["text"])
                corpus.append(data)

        elif mode == MethodEnum.FastText.value:
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
        tagger = MeCab.Tagger(self.tagger_path)
        tagger.parse("")
        node = tagger.parseToNode(text)

        while node:
            word_type = node.feature.split(",")[0]
            if word_type in self.pos:
                out_words.append(node.surface)
            node = node.next

        return out_words

    def split_words(self, text):
        tagger = MeCab.Tagger(self.wakati_tagger_path)
        splitted_sent = tagger.parse(text)
        return splitted_sent
