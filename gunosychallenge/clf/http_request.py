from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_text(url):
    """Fetch data of a page and Return an integrated text.

    Parameters
    ----------
    url : string
        An url of an article page.

    Returns
    -------
    text : string
        Returns an integrated text.
    """
    response = urlopen(url)
    bsObj = BeautifulSoup(response, "html.parser")

    tags = bsObj.find("div", {"class": "article gtm-click"}).contents

    text = "".join([tag.text for tag in tags if tag.name == "p"])

    return text
