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


def get_manwha_title(soup):
    return soup.find('h1').text


def get_manwhas_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    manwhas = soup.find_all('div', class_='list-truyen-item-wrap')

    urls = []
    for manwha in manwhas:
        link = manwha.find('a', href=True, title=True).get('href')
        urls.append(link)

    return urls


def get_manwha_status(soup):
    status = soup.select("tbody tr:nth-child(3) td.table-value")

    try:
        status = status[0].text
        if status not in ['Ongoing', 'Completed']:
            status = "Fail"
    except IndexError:
        status = "Fail"

    if status == "Fail":
        try:
            status = soup.select("tbody tr:nth-child(2) td.table-value")[0].text
        except IndexError:
            status = soup.select("div.manga-info-top > ul > li:nth-child(3)")[0].text

    if status.startswith('Status : '):
        status = status.replace('Status : ', '')

    return status


def get_manwha_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    return get_manwha_title(soup), get_manwha_status(soup)


for page in get_all_pages(2):
    start_time = time.perf_counter()
    for manwhaUrl in get_manwhas_url(page):
        print(get_manwha_data(manwhaUrl))
    end_time = time.perf_counter()
    print(f"Temps d'exécution : {end_time - start_time : .2f} seconde(s)")
