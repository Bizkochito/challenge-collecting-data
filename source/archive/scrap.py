import requests
from bs4 import BeautifulSoup
import json

test_url = "https://www.immoweb.be/en/classified/villa/for-sale/andenne/5300/10561076"
#cookie_url = "https://www.immoweb.be/cookie"

#cookie = requests.get(cookie_url)
response = requests.get(test_url)
test_page = response.text
soup = BeautifulSoup(test_page, "html.parser")
table = soup.find_all('table', class_='classified-table')
data_dict = {}
key_list = []
value_list = []

for tables in table:
    rows = tables.find_all('tr')
    
    for row in rows:
        
        try:
            th_tag = row.find('th', class_="classified-table__header")
            td_tag = row.find('td', class_="classified-table__data")
            if th_tag and td_tag:
                key = th_tag.string.strip()
                span_tag = td_tag.find('span', attrs={'aria-hidden': 'true'})
                if span_tag:
                    value = span_tag.string.strip()
                    
                else:
                    value = td_tag.string.strip()
                key_list.append(key)
                value_list.append(value)
                data_dict[key] = value
        except Exception as e:
            print(f"Error occurred while scraping row: {e}")
print(data_dict)
print(len(key_list))
with open("immodata", "w") as f:
        json.dump(data_dict, f,indent=4)

