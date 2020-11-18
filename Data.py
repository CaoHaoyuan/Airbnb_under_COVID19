# Created by Haoyuan Cao, Nov 6 2020
# This script is used as data loader the COVID dataset and Airbnb dataset.

import numpy as np
import pandas as pd


class AirbnbDataset:
    def __init__(self):
        # us related class attributes
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
                                          "San Francisco","San Mateo County","Santa Clara County","Santa Cruz County"],
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
            self.us_cities.extend(self.us_state_city_mapper[key])

        # all countries related class attributes
        self.country_to_city_map = {"Germany": "Munich",
                                   "Spain": "Madrid",
                                   "Greece": "Athens",
                                   "Sweden": "Stockholm",
                                   "United Kingdom": "Edinburgh",
                                   "China": "Shanghai",
                                   "Singapore": "Singapore",
                                   "Japan": "Tokyo",
                                   "South Africa": "Cape Town",
                                   "Australia": "Sydney",
                                   "Canada": "Ottawa",
                                   "United States": "Washington D.C.",
                                   "Mexico": "Mexico City",
                                   "Brazil": "Rio de Janeiro",
                                   "Argentina": "Buenos Aires"}
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

        df = pd.read_csv(f"Data/{city}/reviews.csv")
        if "listing_id" in df.columns and "date" in df.columns and df.shape[1] == 2:
            pass
        else:
            print(f"Data/{city}/reviews.csv is not the correct file. Please double check. ")

        # preprocess the reviews
        df.date = pd.to_datetime(df.date)
        df['month'] = df.date.dt.month
        df['year'] = df.date.dt.year
        df['week'] = df.date.dt.isocalendar().week

        if per_month:
            num_reviews = df.groupby(['year', 'month']).size().to_frame('size')
        else:
            num_reviews = df.groupby(['year', 'week']).size().to_frame('size')

        return num_reviews

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


class CovidDataset:
    def __init__(self):
        self.wordwide = pd.read_csv("CovidData/worldwide_history.csv").filter(items=["continent","location",'date','total_cases',
                                                                           'new_cases','total_deaths','new_deaths'])
        self.statelevel = pd.read_csv("CovidData/us_all_states_history.csv").filter(items=['date','state','death','deathIncrease',
                                                                                 'positive', 'positiveIncrease',
                                                                                 'totalTestResults', 'totalTestResultsIncrease'])
        self.citylevel = pd.read_csv("CovidData/california_statewide_cases.csv")

        # rename columns, with names death, death_increase, total_cases, new_cases, total_test_results(if available), total_test_results_increase(if available)
        self.wordwide = self.wordwide.rename(columns={'total_deaths':'death', 'new_deaths':'death_increase',
                                              'total_cases':'total_cases', 'new_cases':'new_cases'})
        self.statelevel = self.statelevel.rename(columns={'death':'death', 'deathIncrease':'death_increase',
                                                  'positive':'total_cases', 'positiveIncrease':'new_cases',
                                                  'totalTestResults':'total_test_results', 'totalTestResultsIncrease':'total_test_results_increase'})
        self.citylevel = self.citylevel.rename(columns={'totalcountdeaths':'death', 'newcountdeaths':'death_increase',
                                                'totalcountconfirmed':'total_cases', 'newcountconfirmed':'new_cases'})

        # change all date column to pd.datetime
        self.wordwide.date = pd.to_datetime(self.wordwide.date)
        self.statelevel.date = pd.to_datetime(self.statelevel.date)
        self.citylevel.date = pd.to_datetime(self.citylevel.date)

        print("All data loaded and preprocessed.")

    def get_available_countries(self):
        """
        Get a set of countries where data is available.
        """
        return set(self.wordwide.location.unique())

    def get_data_wordwide(self):
        """
        Get the wordwide data in one data frame
        """
        return self.wordwide

    def get_data_statelevel(self):
        """
        Get all us states' data in one data frame
        """
        return self.wordwide

    def get_data_citylevel(self):
        """
        Get California's all counties' data in one data frame
        """
        return self.citylevel

    def get_data_for_country(self, country, per_day=True, per_week=False):
        """
        Get the historical covid data per day/month for the country.
        """
        assert isinstance(country, str)
        assert (per_day and not per_week) or (per_week and not per_day)

        is_country = self.wordwide.location == country
        df_country = self.wordwide[is_country].copy().reset_index(drop=True)  # deep copy
        if per_day:
            return df_country.set_index('date')
        else:
            df_country['year'] = df_country.date.dt.year
            df_country['week'] = df_country.date.dt.isocalendar().week
            return df_country.groupby(['year', 'week']).sum()

    def get_data_for_state(self, state, per_day=True, per_week=False):
        """
        Get the historical covid data per day/month for the state.
        """
        assert isinstance(state, str)
        assert (per_day and not per_week) or (per_week and not per_day)

        is_state = self.statelevel.state == state
        df_state = self.statelevel[is_state].copy().reset_index(drop=True)  # deep copy
        if per_day:
            return df_state.set_index('date')
        else:
            df_state['year'] = df_state.date.dt.year
            df_state['week'] = df_state.date.dt.isocalendar().week
            return df_state.groupby(['year', 'week']).sum()

    def get_data_for_city(self, city, per_day=True, per_week=False):
        """
        Get the historical covid data per day/month for the state.
        """
        assert isinstance(city, str)
        assert (per_day and not per_week) or (per_week and not per_day)

        is_city = self.citylevel.county == city
        df_city = self.citylevel[is_city].copy().reset_index(drop=True)  # deep copy
        if per_day:
            return df_city.set_index('date')
        else:
            df_city['year'] = df_city.date.dt.year
            df_city['week'] = df_city.date.dt.isocalendar().week
            return df_city.groupby(['year', 'week']).sum()



























