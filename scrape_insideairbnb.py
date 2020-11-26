"""
script to scrape insideairbnb/get-the-data.html for retrieving the CSV files
for every location based on the desired filename

typical format of link to file on the page is used for scraping and filtering the desired link:
http://data.insideairbnb.com/spain/catalonia/girona/2020-10-28/visualisations/listings.csv

created by Apoorva Gokhale on Nov 25,2020.
"""
from bs4 import BeautifulSoup as bs
import requests
import os

TARGET_DIR = './Airbnb_Listings'

if not os.path.isdir(TARGET_DIR):
    os.makedirs(TARGET_DIR)

DOMAIN = ''
URL = 'http://insideairbnb.com/get-the-data.html'
FILETYPE = 'listings.csv'
NOTFILETYPE = 'listings.csv.gz'
def get_soup(url):
    return bs(requests.get(url).text, 'html.parser')

for link in get_soup(URL).find_all('a'):
    file_link = link.get('href')
    if file_link is None:
        continue
    if FILETYPE in file_link and not NOTFILETYPE in file_link:
        fname_parts = file_link.split('/')[3:-2]
        fname = ''
        dirname = ''
        for part in fname_parts:
            fname += (part+'-')
        for part in fname_parts[:3]:
            dirname += (part+'-')
        fname = fname[:-1] + '.csv'
        dirname = os.path.join(TARGET_DIR, dirname[:-1])
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        with open(os.path.join(dirname,fname), 'wb') as file:
            response = requests.get(file_link)
            file.write(response.content)
        print(f"downloaded: {os.path.join(dirname,fname)}")