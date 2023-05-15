import requests
import json
from bs4 import BeautifulSoup
from typing import List
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import time
import re
start=time.time()


def extract_urls_lists(search_page_url: str) -> List[str]:
    response = requests.get(search_page_url, params = {})
    soup = BeautifulSoup(response.text, 'html.parser')

    list_of_urls=[]

    for article in soup.find_all('iw-search-card-rendered'):
        for link in article.find_all('a'):
            list_of_urls.append(link.get('href'))
    return list_of_urls

def extract_x_urls(number_of_urls: int=30) -> List[str]:
    immo_base_url = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page="
    immo_end_url = "&orderBy=relevance"
    searchpages_urls_list =[]

    for index in range(1,round(min(334,number_of_urls/30 + 1))):
        full_url = immo_base_url + str(index) + immo_end_url
        searchpages_urls_list.append(full_url)
    
    full_urls_list =[]

    with ThreadPoolExecutor() as pool:
        full_urls_list=list(pool.map(extract_urls_lists, searchpages_urls_list))    

    if number_of_urls>9990:
        immo_base_url = "https://www.immoweb.be/en/search/new-real-estate-project-apartments/for-sale?countries=BE&page="
        immo_end_url = "&orderBy=relevance"
        searchpages_urls_list =[]

        for index in range(1,round(min(334,(number_of_urls-9990)/30 + 1))):
            full_url = immo_base_url + str(index) + immo_end_url
            searchpages_urls_list.append(full_url)

        with ThreadPoolExecutor() as pool:
            full_urls_list+=list(pool.map(extract_urls_lists, searchpages_urls_list))  
            
    return list(set(sum(full_urls_list,[])))
    
extract_x_urls(30)


pd.set_option('display.width', None)

def missing_data(url):
    response = requests.get(url)

    window_data = re.findall("window.dataLayer =(.+?);\n", response.text, re.S)
    property_info_dict={}

    property_info_dict['Type of Propoerty']=json.loads(window_data[0])[0]['classified']['type']
    property_info_dict['Subtype of Propoerty']=json.loads(window_data[0])[0]['classified']['subtype']
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
        
    except:
        print("error while getting the data")
    return full_df
make_one_data_frame("https://www.immoweb.be/en/classified/house/for-sale/kortrijk/8500/10564478")



list_of_urls = extract_x_urls(10000)
print(len(list_of_urls))
print('list ready')
dataframes_list = []
with ThreadPoolExecutor() as pool:
    results = list(pool.map(make_one_data_frame, list_of_urls))
    for result in results:
        dataframes_list.append(result)

full_df = pd.concat(dataframes_list).reset_index(drop=True)
full_df.dropna(thresh=2,inplace=True)
print('done extracting')
#full_df.to_csv("df.csv")
full_df


def data_clean(df, numerical_cols):
    # Drop empty rows
    df = df.dropna(how='all')

    # Extract numerical values from all columns
    for col in numerical_cols:
        df[col] = df[col].str.extract(r'(\d+)')

    # Replace 'yes' with 1 and 'no' with 0 in all columns
    df = df.replace({'Yes': 1, 'No': 0})

    return df

numerical_cols = ['Number of frontages', 'Living area', 'Bedrooms', 'Bathrooms', 'Surface of the plot', 'Garden surface', 'Price']

cleaned_data = data_clean(full_df, numerical_cols)
cleaned_data.to_csv("cleaned_data_12000.csv")
end=time.time()
print(end - start)


