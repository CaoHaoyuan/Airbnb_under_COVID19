# Created by Haoyuan Cao, Nov 6 2020
# Modified by Apoorva Gokhale, Nov 25 2020
# This script is used as data loader the COVID dataset.

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



























