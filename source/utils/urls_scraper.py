import requests
import json
from bs4 import BeautifulSoup

immo_url = "https://www.immoweb.be/fr/recherche/maison/a-vendre?countries=BE&page=1&orderBy=relevance"
cookie_url="https://www.immoweb.be/cookie"

user_cookie = requests.get(cookie_url).cookies

response = requests.get(immo_url, cookies = user_cookie, params = {})
soup = BeautifulSoup(response.text, 'html.parser')

stuff=[]
# retrieve all of the paragraph tags
for article in soup.find_all('iw-search-card-rendered'):
    for link in article.find_all('a'):
        print(link.get('href'))
        stuff.append(link)

#with open('prettysoup.txt', 'w') as f:
#    f.write(soup.prettify())
with open('deepersoup.txt', 'w') as f:
    f.write(str(stuff))

#with open('immoweb_urls.json', 'w') as f:
#   json.dump(stuff, f)

