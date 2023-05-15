import requests
import json
from bs4 import BeautifulSoup
from typing import List
import time
from multiprocessing import Pool

def extract_urls_lists(search_page_url: str) -> List[str]:
    response = requests.get(search_page_url, params = {})
    soup = BeautifulSoup(response.text, 'html.parser')

    list_of_urls=[]

    for article in soup.find_all('iw-search-card-rendered'):
        for link in article.find_all('a'):
            list_of_urls.append(link.get('href'))
    return list_of_urls

def extract_x_urls(number_of_urls: int=30) -> List[str]:
    immo_base_url = "https://www.immoweb.be/fr/recherche/maison/a-vendre?countries=BE&page="
    immo_end_url = "&orderBy=relevance"
    searchpages_urls_list =[]

    for index in range(1,round(min(334,number_of_urls/30 + 1))):
        full_url = immo_base_url + str(index) + immo_end_url
        searchpages_urls_list.append(full_url)
    
    full_urls_list =[]

    with Pool() as pool:
        full_urls_list=list(pool.map(extract_urls_lists, searchpages_urls_list))    
    return sum(full_urls_list,[])

if __name__ == "__main__" :
    print("Running an extraction timed test with target: 9990 urls")
    start = time.perf_counter()

    print(len(extract_x_urls(9990)))

    end = time.perf_counter()

    execution_time = round((end - start), 2)
    print(f'extract_all_urls took {execution_time} sec')


