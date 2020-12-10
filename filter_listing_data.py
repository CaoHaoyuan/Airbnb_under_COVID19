"""
script to filter out desirable columns from the scraped airbnb listings data

created by Apoorva Gokhale, Nov 25, 2020.
"""

import os
import pandas as pd

LISTINGS_PATH=  './Airbnb_Listings'
LISTINGS_TARGET_DIR = './Airbnb_FilteredListings'

TARGET_COLUMNS= ['host_id', 'room_type', 'price',
       'minimum_nights', 'number_of_reviews', 'last_review',
       'reviews_per_month', 'availability_365']

#state level arima
#script for filtering full csv

if not os.path.exists(LISTINGS_TARGET_DIR):
    os.makedirs(LISTINGS_TARGET_DIR)
    
    #using : id, host_id, price, availability
    for loc_dir in os.listdir(LISTINGS_PATH):
        full_loc_dir = os.path.join(LISTINGS_PATH, loc_dir)
        full_target_loc_dir = os.path.join(LISTINGS_TARGET_DIR,loc_dir)
        if not os.path.exists(full_target_loc_dir):
            os.makedirs(full_target_loc_dir)
        for fname in os.listdir(full_loc_dir):
            full_fname = os.path.join(full_loc_dir, fname)
            if(os.path.isfile(full_fname) and fname.split('.')[-1] == 'csv'):
                full_target_fname = os.path.join(full_target_loc_dir, fname)
                print(full_target_fname)
                df = pd.read_csv(full_fname, index_col=0)
                df_cols = df.columns
                #take the intersection of column headers between what we have in a csv
                # and our target columns, to prevent error-out
                final_target_cols = [colname for colname in TARGET_COLUMNS if colname in df.columns]
                df = df[final_target_cols]
                df.to_csv(full_target_fname)