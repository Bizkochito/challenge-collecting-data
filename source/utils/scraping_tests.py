import requests
import json
from bs4 import BeautifulSoup

""" immo_url = "https://www.immoweb.be/fr/annonce/immeuble-mixte/a-vendre/alost/9300/10557403"
cookie_url="https://www.immoweb.be/cookie"

user_cookie = requests.get(cookie_url).cookies

response = requests.get(immo_url, cookies = user_cookie, params = {})
soup = BeautifulSoup(response.text, 'html.parser')

with open('single_building_info.json', 'w') as f:
    json.dump(response.json(), f)
 """
immo_base_url = "https://www.immoweb.be/fr/recherche/maison/a-vendre?countries=BE&page="
immo_end_url = "&orderBy=relevance"
for index in range(1,334):
    full_url = immo_base_url + str(index) + immo_end_url
    print(full_url)