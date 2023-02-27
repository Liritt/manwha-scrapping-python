import time
import re

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
    return soup.find('h1').text.replace("\\", "")


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


def get_manwha_genres(soup):
    genres = soup.select("div.manga-info-top > ul > li:nth-child(7)")

    try:
        genres = genres[0].text
    except IndexError:
        genres = "Fail"

    if genres == "Fail":
        try:
            genres = soup.select("tbody > tr:nth-child(4) > td.table-value")[0].text
        except IndexError:
            genres = soup.select("tbody > tr:nth-child(3) > td.table-value")[0].text

    if genres.startswith('Genres :'):
        genres = genres.replace('Genres :', '')

    genres = re.sub(r'\n', '', genres)

    if "," in genres:
        genres = [genre.strip() for genre in genres.split(',') if genre.strip()]
    elif "-" in genres:
        genres = [genre.strip() for genre in genres.split('-') if genre.strip()]
    elif "/" in genres:
        genres = [genre.strip() for genre in genres.split('/') if genre.strip()]
    if type(genres) != list:
        genres = genres.split()

    return genres


def get_manwha_views(soup):
    views = soup.select("div.story-info-right div.story-info-right-extent p:nth-child(2) span.stre-value")

    try:
        views = views[0].text
    except IndexError:
        views = "Fail"

    if views == "Fail":
        try:
            views = soup.select("div.manga-info-top ul.manga-info-text li:nth-child(6)")[0].text
        except IndexError:
            views = "Fail"

    if views.startswith("View : "):
        views = views.replace("View : ", "")

    return views


def get_manwha_description(soup):
    try:
        description = soup.select("#panel-story-info-description")[0].text.replace("Description :\n", "")
    except IndexError:
        description = "Fail"

    if description == "Fail":
        try:
            description = soup.select("#noidungm")[0].text
        except IndexError:
            description = "Fail"

    return description.replace('\n', '').replace('\\', '')


def get_manwha_pic(soup):
    try:
        pic = soup.find_all("img")[1].get("src")
    except IndexError:
        pic = "Fail"

    return pic


def get_manwha_rating(soup):
    try:
        rating = soup.select_one("#rate_row_cmd > em > em:nth-child(2) > em > em:nth-child(1)").text
    except AttributeError:
        rating = "Fail"

    if rating == "Fail":
        try:
            rating = soup.select_one("#rate_row > input").text
        except AttributeError:
            rating = "Fail"

    return rating


def get_manwha_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    return get_manwha_title(soup), get_manwha_status(soup), get_manwha_genres(soup), get_manwha_views(
        soup), get_manwha_pic(soup), get_manwha_rating(soup)


for page in get_all_pages(2):
    start_time = time.perf_counter()
    for manwhaUrl in get_manwhas_url(page):
        print(get_manwha_data(manwhaUrl))
    end_time = time.perf_counter()
    print(f"Temps d'exécution : {end_time - start_time : .2f} seconde(s)")
