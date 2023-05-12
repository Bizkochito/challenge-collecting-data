import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import re


immo_url = "https://www.immoweb.be/en/classified/penthouse/for-sale/bruxelles/1130/10560964"
cookie_url = "https://www.immoweb.be/cookie"
user_cookie = requests.get(cookie_url).cookies

response = requests.get(immo_url, cookies = user_cookie, params = {})
soup = BeautifulSoup(response.content,"html.parser")

# for elem in soup.find_all("script"):
#     for articles in elem:
#         print(elem.get_text())

# for elem in soup.find_all("p", attrs={"class": "classified__price"}):
#     print(elem.get_text())

# for elem in soup.find_all("h1", attrs={"class": "classified__title"}):
#     print(elem.get_text())

# for elem in soup.find_all("div", attrs={"class": "overview__item"}):
#     print(elem.get_text())

# for elem in soup.find_all("p", attrs={"class": "classified__information--property"}):
#     data = re.sub(r"\<.*?\>", '',str(elem))
#     data = data.replace('|', '')
#     words = [word.strip() for word in data.split()]
#     result = ' '.join(words)
#     print(result)
   
# for elem in soup.find_all("tr", attrs={"class": "classified-table__row"}):
#     print(elem.prettify())

# key_list=[]

# for elem in soup.find_all("th", attrs={"class": "classified-table__header"}):
#     for article in elem:
#         key_list.append(article.strip())
# print(key_list)

# value_list=[]
# for elem in soup.find_all('td', class_='classified-table__data'):
#     for article in elem:
#         value_list.append(article)
# print(value_list)

# my_dict = {key:value for key, value in zip(key_list, value_list)}
# print(my_dict)
# list_of_key_values=[]

# tables = soup.find_all('tr', class_='classified-table__row')
# for table in tables:
#     try:
#         th_tag = table.find('th', class_='classified-table__header').text.strip()
#     except AttributeError:
#         th_tag = 'error'
#     try:
#         td_tag = table.find('td', class_='classified-table__data').text.strip()
#     except AttributeError:
#         td_tag = 'error'

#     dict={"th":th_tag, "td":td_tag}
#     list_of_key_values.append(dict)
# print(list_of_key_values)
# df=pd.DataFrame(list_of_key_values)
# print(df)
# print(dict)
