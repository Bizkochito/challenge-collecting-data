

import requests
import json


immo_url = "https://www.immoweb.be/fr/annonce/immeuble-mixte/a-vendre/alost/9300/10557403"


cookie_url="https://www.immoweb.be/cookie"

user_cookie = requests.get(cookie_url).cookies


response = requests.get(immo_url, cookies = user_cookie, params = {})
 
with open('single_building_info.json', 'w') as f:
    json.dump(response.text, f)

