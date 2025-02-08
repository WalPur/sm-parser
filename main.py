import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "sm.agiki.ru/"

link_pool = ["/"]
proceeded_links = []
pages = []


def get_link_to_proceed():
    """Возвращает не обработанную ссылку, если нет ссылки, то False"""
    for link in link_pool:
        if link not in proceeded_links:
            return link
    return False


while True:
    link = get_link_to_proceed()
    if link is False:
        break
    html = requests.get(BASE_URL + link).content
    soup = BeautifulSoup(html, "html.parser")

    page = {
        "url": BASE_URL + link,
        "content": str(soup),
    }
    proceeded_links.append(link)
    time.sleep(1)
