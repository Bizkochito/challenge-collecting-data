import requests
import json
from bs4 import BeautifulSoup


immo_url = "https://www.immoweb.be/fr/annonce/immeuble-mixte/a-vendre/alost/9300/10557403"
cookie_url = "https://www.immoweb.be/cookie"
user_cookie = requests.get(cookie_url).cookies

response = requests.get(immo_url, cookies = user_cookie, params = {})
 
print(immo_url, response.status_code)
soup = BeautifulSoup(response.content,"html.parser")
for elem in soup.find_all("script"):
    for articles in elem:
        print(elem.get_text())
# for elem in soup.find_all("p", attrs={"class": "classified__price"}):
#     print(elem.get_text())
# for elem in soup.find_all("h1", attrs={"class": "classified__title"}):
#     print(elem.get_text())
# for elem in soup.find_all("span", attrs={"class": "overview__text"}):
#     print(elem.get_text())
# for elem in soup.find_all("div", attrs={"class": "classified__information--address"}):
#     print(elem.get_text())
# for elem in soup.find_all("div", attrs={"class": "classified__header--immoweb-code"}):
#     print(elem.get_text())



