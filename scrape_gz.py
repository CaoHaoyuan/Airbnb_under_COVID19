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
import time
import config_data
#where the filtered CSV files will be stored
TARGET_DIR = config_data.AIRBNB_LISTINGS_DATA_DIR	

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
        fname = fname[:-1]
        fname_ext = fname + extension
        dirname = os.path.join(TARGET_DIR, dirname[:-1])
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        if os.path.isfile(os.path.join(dirname,fname+'.csv')):
            #the filtered file exists, skip this iteration completely and move to next file
            print(f"Skipped {os.path.join(dirname,fname)}.csv. It already exists")
            continue
        #download the large file
        with open(os.path.join(dirname,fname_ext), 'wb') as file:
            while True:
                try:
                    print("trying to establish a connection with the source..")
                    response = requests.get(file_link)
                    break
                except:
                    print("waiting for a while to allow NewConnections again...")
                    time.sleep(5)
                    print("trying again...")
            file.write(response.content)
            print(f"downloaded: {os.path.join(dirname,fname_ext)}")
        df = []
        new_fname = fname_ext + ''
        try:
            if ".gz" in extension:
                df = pd.read_csv(os.path.join(dirname,fname_ext), compression="gzip", index_col=0)
                new_fname = new_fname[:new_fname.find(".gz")]
            else:
                df = pd.read_csv(os.path.join(dirname,fname_ext),index_col=0)
        except:
            print(f"exception occured while parsing {os.path.join(dirname,fname_ext)}. Skipping this file for now.")
            continue
            
        #delete the large file to allow for saving the filtered one at the same location
        if os.path.exists(os.path.join(dirname,fname_ext)):
            os.remove(os.path.join(dirname,fname_ext))
        #select the columns of interest that are actually in the CSV columns
        cols = []
        #handle missing columns
        for c in COLUMNS_OF_INTEREST:
            if c in df.columns:
                cols.append(c)
        df = df[cols]
        #write out the df with columns of interest as .CSV to same location with same name
        df.to_csv(os.path.join(dirname,new_fname))
        print(f"Filtered CSV written out to {os.path.join(dirname,new_fname)}")
        