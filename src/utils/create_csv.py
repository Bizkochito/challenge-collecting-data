import requests
import json
from bs4 import BeautifulSoup
from typing import List
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import time
import re
import numpy as np
from tqdm import tqdm



def extract_urls_lists(search_page_url: str) -> List[str]:
    """
    Extracts 30 urls from an immoweb browsing search page.
    Scans the page for specific tags and urls under href references.

    :param search_page_url: A string url from which to extract urls.
    :return: List of properties urls.
    """
    try:    
        response = requests.get(search_page_url, params = {})
    except Exception as e:
        print(e)
        return []
    soup = BeautifulSoup(response.text, 'html.parser')

    list_of_urls=[]

    for article in soup.find_all('iw-search-card-rendered'):
        for link in article.find_all('a'):
            list_of_urls.append(link.get('href'))
    return list_of_urls

def extract_x_urls(number_of_urls: int=30) -> List[str]:
    """
    Extracts houses urls from immoweb. 
    Scans the search pages for specific tags and urls under href references.
    Depending on how many urls are asked, scans through up to 333 pages (the easiest available ones).
    If the argument is > 10000, adds appartments urls to the data.

    :param number_of_urls: The int number of urls you want to get.
    :return: List of properties urls.
    """
    immo_base_url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page="
    immo_end_url = "&orderBy=relevance"
    searchpages_urls_list =[]

    for index in range(1,round(min(334,number_of_urls/30 + 1))):
        full_url = immo_base_url + str(index) + immo_end_url
        searchpages_urls_list.append(full_url)
    
    full_urls_list =[]

    with ThreadPoolExecutor() as pool:
        full_urls_list=list(pool.map(extract_urls_lists, searchpages_urls_list))    

    if number_of_urls>9990:
        immo_base_url = "https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page="
        immo_end_url = "&orderBy=relevance"
        searchpages_urls_list =[]

        for index in range(1,round(min(334,(number_of_urls-9990)/30 + 1))):
            full_url = immo_base_url + str(index) + immo_end_url
            searchpages_urls_list.append(full_url)

        with ThreadPoolExecutor() as pool:
            full_urls_list+=list(pool.map(extract_urls_lists, searchpages_urls_list))  
            
    return list(set(sum(full_urls_list,[])))
    
def missing_data(url):
    """
    When scanning a url for data, some info is missed by pandas' read_html method.
    This function looks specifically for this data.

    :param url: A url string to fetch data from.
    :return: A pandas DataFrame.
    """
    response = requests.get(url)

    window_data = re.findall("window.dataLayer =(.+?);\n", response.text, re.S)
    property_info_dict={}

    property_info_dict['Type of Property']=json.loads(window_data[0])[0]['classified']['type']
    property_info_dict['Subtype of Property']=json.loads(window_data[0])[0]['classified']['subtype']
    property_info_dict['Type of Sale']=json.loads(window_data[0])[0]['classified']['transactionType']

    df_dict=pd.DataFrame([property_info_dict])
    return df_dict

def make_one_data_frame(url):
    
    try:
        response = requests.get(url)
        test_page = response.text

        dfs = pd.read_html(test_page)

        full_df = pd.concat(dfs).dropna(thresh=2).T
        full_df.columns = full_df.iloc[0]
        full_df = full_df[1:]
        full_df = full_df.loc[:, full_df.columns.isin(['Neighbourhood or locality','Building condition','Number of frontages','Living area','Kitchen type','Bedrooms','Bathrooms','Furnished','Surface of the plot','Garden surface','Swimming pool','Price','Terrace'])]
        full_df = pd.concat([full_df.iloc[0], missing_data(url).iloc[0]], axis=0).to_frame().T 
        return full_df
    except Exception as e:
        print(f'Couldnt extract from this url: {url}')
        return e
    
def data_clean(df):
    numerical_cols = ['Number of frontages', 'Living area', 'Bedrooms', 'Bathrooms', 'Surface of the plot', 'Garden surface']
    threshold = len(df.columns)-5
    df = df.dropna(thresh=threshold)
    for col in numerical_cols:
        df[col] = df[col].str.extract(r'(\d+)')
    df = df.replace({'Yes': 1, 'No': 0})
    df=df.replace(np.nan,'None',regex=True)
    return df

def extract_clean_data(no_of_urls):
    start=time.time()
    print('Starting the extraction...')
    list_of_urls = extract_x_urls(no_of_urls)
    print(f'Prepared {no_of_urls} urls to scan.')

    with ThreadPoolExecutor() as pool:
        dataframes_list = list(tqdm(pool.map(make_one_data_frame, list_of_urls), total = len(list_of_urls)))
    index = 0
    for item in dataframes_list:
        if type(item) != pd.core.frame.DataFrame:
            dataframes_list.pop(index)
        index += 1

    full_df = pd.concat(dataframes_list).reset_index(drop=True)

    cleaned_data = data_clean(full_df)
    cleaned_data.to_csv(f"real_estate_data_{no_of_urls}.csv")
    print('done extracting')
    end=time.time()
    processing_time = end - start
    print(f'Extraction finished in {processing_time} seconds')

if __name__ == "__main__":
    extract_clean_data(18000)