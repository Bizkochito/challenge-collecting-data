import requests
import json, re
from bs4 import BeautifulSoup
import pandas as pd


url = "https://www.immoweb.be/en/classified/villa/for-sale/andenne/5300/10561076"
response = requests.get(url)

window_data = re.findall("window.dataLayer =(.+?);\n", response.text, re.S)
property_info_dict={}

property_info_dict['Type of Propoerty']=json.loads(window_data[0])[0]['classified']['type']
property_info_dict['Subtype of Propoerty']=json.loads(window_data[0])[0]['classified']['subtype']
property_info_dict['Type of Sale']=json.loads(window_data[0])[0]['classified']['transactionType']

df_dict=pd.DataFrame([property_info_dict])
print(df_dict)