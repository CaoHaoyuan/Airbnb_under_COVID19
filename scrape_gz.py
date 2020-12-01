"""
script to scrape insideairbnb/get-the-data.html for retrieving the Full CSV GZ files
for every location based on the desired filename, filtering the desired columns and saving only those as CSV

typical format of link to file on the page is used for scraping and filtering the desired link:
http://data.insideairbnb.com/spain/catalonia/girona/2020-10-28/visualisations/listings.csv.gz

created by Apoorva Gokhale on Nov 25,2020.
"""
from bs4 import BeautifulSoup as bs
import requests
import os
import pandas as pd

#where the filtered CSV files will be stored
TARGET_DIR = './Airbnb_Listings_Gz'	

if not os.path.isdir(TARGET_DIR):
    os.makedirs(TARGET_DIR)

DOMAIN = ''
URL = 'http://insideairbnb.com/get-the-data.html'
FILENAME = 'listings.csv.gz'

#the columns that are desirable out of the ones in the original CSV GZ
COLUMNS_OF_INTEREST = ["host_id", "number_of_reviews_ltm", "price", "amenities"]

extension = ""
for ext in FILENAME.split('.')[1:]:
    extension+="."+ext
def get_soup(url):
    return bs(requests.get(url).text, 'html.parser')

for link in get_soup(URL).find_all('a'):
    file_link = link.get('href')
    if file_link is None:
        continue
    if FILENAME in file_link:
        fname_parts = file_link.split('/')[3:-2]
        fname = ''
        dirname = ''
        for part in fname_parts:
            fname += (part+'-')
        for part in fname_parts[:3]:
            dirname += (part+'-')
        fname = fname[:-1] + extension
        dirname = os.path.join(TARGET_DIR, dirname[:-1])
        
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        with open(os.path.join(dirname,fname), 'wb') as file:
            response = requests.get(file_link)
            file.write(response.content)
            
        print(f"downloaded: {os.path.join(dirname,fname)}")
        
        df = []
        new_fname = fname
        if ".gz" in extension:
            df = pd.read_csv(os.path.join(dirname,fname), compression="gzip", index_col=0)
            new_fname = fname[:fname.find(".gz")]
        else:
            df = pd.read_csv(os.path.join(dirname,fname),index_col=0)
            
        #delete the large file to allow for saving the 
        if os.path.exists(os.path.join(dirname,fname)):
            os.remove(os.path.join(dirname,fname))
        #select the columns of interest
        df = df[COLUMNS_OF_INTEREST]
        #write out the df with columns of interest as .CSV to same location with same name
        df.to_csv(os.path.join(dirname,new_fname))
        break
        