import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

url = 'https://www.amazon.in/s?k=dslr+camera'

s = HTMLSession()
amazon_data=[]

for i in range(3,15):
    print('page is extracting = ',i)
    bas_url = 'https://www.amazon.in/s?k=dslr+camera&page={i}'
    req = requests.get(bas_url,headers=headers)
    name = BeautifulSoup(req.content,'html.parser')
    
    for link in name.find_all('a',class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal", href=True):
        pro_link = 'https://www.amazon.in'+str(link['href'])
        pro_req = requests.get(pro_link,headers=headers)
        pro_soup = BeautifulSoup(pro_req.content,'html.parser')

        try:
            pro_title = pro_soup.find('span',id='productTitle').text.strip()
        except:
            pro_title='None'
        try:
            pro_price = pro_soup.find('span',class_='a-price-whole').text.strip()
        except:
            pro_price='None'
        try:
            pro_brand = pro_soup.find('tr',class_='a-spacing-small po-brand').text
        except:
            pro_brand='None'
        try:
            pro_model = pro_soup.find('tr',class_='a-spacing-small po-model_name').text
        except:
            pro_model='None'
        try:
            pro_form_factor = pro_soup.find('tr',class_='a-spacing-small po-form_factor').text
        except:
            pro_form_factor='None'
        try:
            pro_resolutaion = pro_soup.find('tr',class_='a-spacing-small po-effective_still_resolution').text
        except:
            pro_resolutaion='None'

        items_m = {
            'Title':pro_title,
            'Price':pro_price,
            'Branf':pro_brand,
            'Model':pro_model,
            'Form Factor':pro_form_factor,
            'Resolution':pro_resolutaion,
        }
        amazon_data.append(items_m)
        
with open('amazon_extract_data.csv','a') as f:
    df = pd.DataFrame(amazon_data)
    df.to_csv('Fair_price_data_5.csv')
