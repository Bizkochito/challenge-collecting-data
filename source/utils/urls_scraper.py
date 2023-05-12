import requests
import json
from bs4 import BeautifulSoup
from typing import List


"""
This code can be used later on to loop through pages. Generates URLS with page number 1->333
immo_base_url = "https://www.immoweb.be/fr/recherche/maison/a-vendre?countries=BE&page=""
immo_end_url = "&orderBy=relevance"
for index in range(1,333):
    full_url = immo_base_url + str(index) + immo_end_url
    print(full_url)
user_cookie = requests.get(cookie_url).cookies
"""
def extract_urls_lists(search_page_url: str) -> List(str):
    response = requests.get(search_page_url, params = {})
    soup = BeautifulSoup(response.text, 'html.parser')

    list_of_urls=[]

    for article in soup.find_all('iw-search-card-rendered'):
        for link in article.find_all('a'):
            list_of_urls.append(link.get('href'))
    return list_of_urls

