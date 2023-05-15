import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

test_url = "https://www.immoweb.be/en/classified/villa/for-sale/andenne/5300/10561076"
#cookie_url = "https://www.immoweb.be/cookie"

#cookie = requests.get(cookie_url)
response = requests.get(test_url)
test_page = response.text

dfs = pd.read_html(test_page)
  # pd.read_html reads in all tables and returns a list of DataFrames
print(pd.concat(dfs), )

