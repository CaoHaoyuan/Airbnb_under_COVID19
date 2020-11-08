# Created by Haoyuan Cao, Nov 6 2020
# This script is used as data loader the COVID dataset and Airbnb dataset.

import numpy as np
import pandas as pd

class Airbnb_Dataset():
    def __init__(self):
        self.us_state_city_mapper = {"North Carolina":["Asheville"],
                            "Texas":["Austin"],
                            "Massachusetts":["Boston","Cambridge"],
                            "Florida":["Broward County"],
                            "Illinois":["Chicago"],
                            "Nevada":["Clark County"],
                            "Ohio":["Columbus"],
                            "Colorado":["Denver"],
                            "Hawaii":["Hawaii"],
                            "New Jersey":["Jersey City"],
                            "California":["Los Angeles","Oakland","Pacific Grove","San Diego",
                                          "San Francisco","San Mateo County","Santa Clara County","Santa Cruz"],
                            "Tennessee":["Nashville"],
                            "Louisiana":["New Orleans"],
                            "New York":["New York City"],
                            "Oregon":["Portland","Salem"],
                            "Rhode Island":["Rhode Island"],
                            "Washington":["Seattle"],
                            "Minnesota":["Twin Cities MSA"],
                            "District of Columbia":["Washington D.C."]}
        self.us_states = list(self.us_state_city_mapper.keys())
        self.us_cities = []
        for key in self.us_states:
            self.us_cities.append(self.us_state_city_mapper[key])

    ################## United States Related functions ################
    def get_num_us_states(self):
        """
        Get number of us states where data is available
        :return: int
        """
        return len(self.us_state_city_mapper.keys())

    def get_us_states(self):
        """
        Get list of us states where data is available
        :return: list of strings
        """
        return list(self.us_state_city_mapper.keys())


    ################## General functions ################
    def get_reviews_per_month_for_city(self, city):
        """
        Get historical total reviews per month for the city specified. All months with data available will be returned.

        Assumed that occupancy rate is proportional to the revierws per month. The result returned by this function would
        indicate the Airbnb activity for this city.
        :param city: string
        :return: pd.dataframe, size = number of months * 3
        """
        assert isinstance(city, str)
        if city in self.us_cities:
            print("This is a US city.")
        else:
            print("This is not a US city")

        df = pd.read_csv(f"Data/{city}/reviews.csv")
        if "listing_id" in df.columns and "date" in df.columns and df.shape[1] == 2:
            pass
        else:
            print(f"Data/{city}/reviews.csv is not the correct file. Please double check. ")

        # preprocess the reviews
        df.date = pd.to_datetime(df.date)
        df['month'] = df.date.dt.month
        df['year'] = df.date.dt.year

        num_reviews_per_month = df.groupby(['year', 'month']).size().reset_index()

        return num_reviews_per_month

    def get_reviews_per_month_for_us_state(self, state):
        """
        Get historical reviews per month for the United States specified.

        Simply use the get_total_reviews_per_month_for_cities() function.
        :param state: string
        :return: pd.dataframe, size = number of months * 3
        """
        assert isinstance(state, str) and state in self.us_states
        return self.get_total_reviews_per_month_for_cities(self.us_state_city_mapper[state])

    def get_total_reviews_per_month_for_cities(self, cities):
        """
        Get total historical reviews per month for the cities specified. All months with date available (for all cities in this state) will be returned.
        Value is computed by summing all cities reviews in this state.

        :param cities: list of strings
        :return: pd.dataframe, size = number of months * 3
        """
        assert isinstance(cities, list) and len(cities) >= 1 and isinstance(cities[0], str)

        num_reviews_per_month = self.get_reviews_per_month_for_city(cities[0])
        for city in cities[1:]:
            df = self.get_reviews_per_month_for_city(city)
            num_reviews_per_month = pd.merge(num_reviews_per_month, df, on=["year", "month"])
            num_reviews_per_month["0_x"] = num_reviews_per_month["0_x"] + num_reviews_per_month["0_y"]
            num_reviews_per_month = num_reviews_per_month.drop('0_y', axis=1)

        return num_reviews_per_month



























