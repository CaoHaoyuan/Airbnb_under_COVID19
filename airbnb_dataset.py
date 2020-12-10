# Created by Haoyuan Cao, Nov 6 2020
# Modified by Apoorva Gokhale, Nov 25 2020
# This script is used as data loader the Airbnb dataset.

import numpy as np
import pandas as pd
import os

import config_data

class AirbnbDataset:
    def __init__(self):
        
        self.us_state_city_mapper = config_data.US_state_to_city
        
        self.us_states = list(self.us_state_city_mapper.keys())
        self.us_cities = []
        
        for key in self.us_states:
            self.us_cities.extend(self.us_state_city_mapper[key])

        # all countries related class attributes
        self.country_to_city_map = config_data.country_to_city
        self.countries = list(self.country_to_city_map.keys())
        self.global_cities = [self.country_to_city_map[_] for _ in self.countries]
        self.city_to_country_map = dict(zip(self.global_cities, self.countries))


    ################## helper functions ################
    def get_num_us_states(self):
        """
        Get number of us states where data is available
        :return: int
        """
        return len(self.us_state_city_mapper.keys())

    def get_num_countries(self):
        """
        Get number of countries where data is available
        :return: int
        """
        return len(self.countries)


    ################## General functions ################
    def get_reviews_for_city(self, city, per_month = True, per_week = False):
        """
        Get historical total reviews per month(week) for the city specified. All months(weeks) with data available will be returned.

        Assumed that occupancy rate is proportional to the revierws per month(week). The result returned by this function would
        indicate the Airbnb activity for this city.
        :param city: string
        :return: pd.dataframe, size = number of months * 3
        """
        assert isinstance(city, str)
        assert not (per_month and per_week)
        assert per_month or per_week

        if city in self.us_cities:
            print(f"City {city} is in country United States .")
        elif city in self.global_cities:
            print(f"City {city} is in country {self.city_to_country_map[city]}")
        else:
            print(f"City {city}'s data is not available. Please double check.")
            return None
        
        review_file_path = os.path.join(config_data.AIRBNB_DATA_DIR,f"{city}/reviews.csv")
        assert(os.path.isfile(review_file_path)),f"file not found at {review_file_path}!"
        
        df = pd.read_csv(review_file_path)
        if "listing_id" in df.columns and "date" in df.columns and df.shape[1] == 2:
            pass
        else:
            print(f"{review_file_path} is not the correct file. Please double check. ")

        # preprocess the reviews
           
        df.date = pd.to_datetime(df.date)
        df['month'] = df.date.dt.month
        df['year'] = df.date.dt.year
        df['week'] = df.date.dt.isocalendar().week

        if per_month:
            num_reviews = df.groupby(['year', 'month']).size().to_frame('size')
        else:
            num_reviews = df.groupby(['year', 'week']).size().to_frame('size')
        return num_reviews, df['date']

    def get_total_reviews_for_cities(self, cities, per_month=True, per_week=False):
        """
        Get total historical reviews per month(week) for the cities specified. All months with date available (for all cities in this state) will be returned.
        Value is computed by summing all cities reviews in this state.
        """
        assert isinstance(cities, list) and len(cities) >= 1 and isinstance(cities[0], str)
        assert not (per_month and per_week)
        assert per_month or per_week

        num_reviews = self.get_reviews_for_city(cities[0], per_month, per_week)
        for city in cities[1:]:
            df = self.get_reviews_for_city(city, per_month, per_week)
            num_reviews = pd.merge(num_reviews, df, on=["year", "month"]) if per_month else pd.merge(num_reviews, df, on=["year", "week"])
            num_reviews["size"] = num_reviews["size_x"] + num_reviews["size_y"]
            num_reviews = num_reviews.drop(['size_y', "size_x"], axis=1)

        return num_reviews

    def get_reviews_for_us_state(self, state, per_month=True, per_week=False):
        """
        Get historical reviews per month(week) for the United States specified.

        Simply use the get_total_reviews_per_month_for_cities() function.
        """
        assert isinstance(state, str) and state in self.us_states
        assert not (per_month and per_week)
        assert per_month or per_week

        return self.get_total_reviews_for_cities(self.us_state_city_mapper[state], per_month, per_week)

    def get_reviews_for_country(self, country, per_month=True, per_week=False):
        """
        Get historical reviews per month(week) for the country. The representative city's data will be returned.
        """
        assert isinstance(country, str) and country in self.countries
        assert not (per_month and per_week)
        assert per_month or per_week

        return self.get_reviews_for_city(self.country_to_city_map[country], per_month, per_week)