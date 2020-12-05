import os
#data paths
AIRBNB_DATA_DIR = './AirbnbData/'
AIRBNB_LISTINGS_DATA_DIR = os.path.join(AIRBNB_DATA_DIR,'Listings')
COVID19_COUNTRY_PATH = "./COVID-19Data/worldwide_history.csv"
COVID19_STATE_PATH = "./COVID-19Data/us_all_states_history.csv"
COVID19_CITY_PATH = "./COVID-19Data/california_statewide_cases.csv"

#definitions and mappings

# us related class attributes
US_state_to_city = {"North Carolina":["Asheville"],
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

misc_cities = ["Beijing"]

# mapping country to representative city
country_to_city = {"Germany": "Munich",
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
