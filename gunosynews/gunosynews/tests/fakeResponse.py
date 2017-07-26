import os
from scrapy.http import TextResponse, Request


def fake_response(file_name, url=None):
    if not url:
        url = "https://www.gunosy.com/tags/2"

    request = Request(url=url)
    if file_name:
        if not file_name[0] == '/':
            responses_dir = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(responses_dir, file_name)
        else:
            file_path = file_name

        with open(file_path, 'r') as f:
            file_content = f.read()
    else:
        file_content = ''

    response = TextResponse(url=url, request=request, body=file_content,
                            encoding='utf-8')
    return response
