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


def get_manwha_title(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    return soup.find('h1').text


get_manwha_title("https://chapmanganato.com/manga-pp992650")

for page in get_all_pages(2):
    start_time = time.perf_counter()
    time.sleep(3)
    for manwhaUrl in get_manwhas_url(page):
        print(get_manwha_title(manwhaUrl))
    end_time = time.perf_counter()
    print(f"Temps d'exécution : {end_time - start_time : .2f} seconde(s)")

