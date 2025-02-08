import time
import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://sm.agiki.ru"

link_pool = ["/index.php"]
proceeded_links = []
pages = []
ignore_list = ["http://joomla3x.ru", "http://joomla3x.ru/", "/images/yakutianbook.pdf", "http://nachodki.ru/"]
skipped_links = []

def add_links(tag_collection):
    """Добавляет в пулл ссылок новые ссылки после фильтрации"""
    for tag in tag_collection:
        link = tag.get("href")
        if link not in ignore_list and link not in link_pool and "http" not in link and "https" not in link:
            link_pool.append(link)

def get_link_to_proceed():
    """Возвращает не обработанную ссылку, если нет ссылки, то False"""
    for link in link_pool:
        if link not in proceeded_links:
            return link
    return False

def get_content(soup: BeautifulSoup):
    """Возвращает содержимое страницы, если его нет, то False"""
    content = soup.find(id="content")
    if content is None:
        content = soup.find(id="content-w2")
    if content is None:
        return False
    return content


while True:
    link = get_link_to_proceed()
    print("Обрабатывается страница:", link)
    if link is False:
        break
    html = requests.get(BASE_URL + link).content
    soup = BeautifulSoup(html, "html.parser")
    page_content = get_content(soup)
    if page_content is not False:
        page = {
            "url": BASE_URL + link,
            "content": str(page_content.contents),
        }
        proceeded_links.append(link)
        add_links(soup.find_all('a'))
        time.sleep(1)
        pages.append(page)
    else:
        print("Пропущена страница")
        skipped_links.append(link)
        proceeded_links.append(link)

file = open("data.json", "w", encoding="utf-8")
file.write(json.dumps(pages, ensure_ascii=False))
file.close()
file = open("skipped links.txt", "w", encoding="utf-8")
file.write(str(skipped_links))
file.close()