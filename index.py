import time

import requests
from bs4 import BeautifulSoup


def get_all_pages(number=1):
    urls = []
    page_number = 1

    for i in range(number):
        i = f"https://mangakakalot.com/manga_list?type=latest&category=all&state=all&page={page_number}"
        page_number += 1
        urls.append(i)

    return urls


def get_manwhas_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    manwhas = soup.find_all('div', class_='list-truyen-item-wrap')

    urls = []
    for manwha in manwhas:
        link = manwha.find('a', href=True, title=True).get('href')
        urls.append(link)

    return urls


for page in get_all_pages(2):
    time.sleep(3)
    print(get_manwhas_url(page))
