# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_text(url):
    resp = urlopen(url)
    bsObj = BeautifulSoup(resp, "html.parser")

    tags = bsObj.find("div", {"class": "article gtm-click"}).contents

    text = "".join([tag.text for tag in tags if tag.name == "p"])

    return text



