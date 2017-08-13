import os

from scrapy.http import Request, TextResponse


def fake_response(file_name, url=None):
    """Create a fake HTTP response from a HTML file.

    Parameters
    ----------
    file_name : string
        The relative or absolute filename from the 'utils' directory.

    url : string
        The URL of the response.

    Returns
    -------
    response : TextResponse
        A fake HTTP response which is used for the unittest.
    """
    if not url:
        url = 'https://www.gunosy.com/tags/2'

    request = Request(url=url)

    if file_name:
        if not file_name[0] == '/':
            utils_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(utils_dir, file_name)
        else:
            file_path = file_name

        with open(file_path, 'r') as f:
            file_content = f.read()
    else:
        file_content = ''

    response = TextResponse(url=url,
                            request=request,
                            body=file_content,
                            encoding='utf-8')

    return response
