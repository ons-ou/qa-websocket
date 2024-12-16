import requests
from html2text import HTML2Text


def get_html(url):
    response = requests.get(url)
    return response.text


async def html_to_text(html):
    h = HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_mailto_links = True
    return h.handle(html)
