import requests
import json
from bs4 import BeautifulSoup


house_url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=1&orderBy=relevance"
response = requests.get(house_url, params = {})
soup = BeautifulSoup(response.content,"html.parser")
house_url_list_single_page=[]
paragraphs =soup.find_all("h2", attrs={"class": "card__title card--result__title"})
for paragraph in paragraphs:
    house_url_list_single_page.append(paragraph.get("href"))
print(house_url_list_single_page)
