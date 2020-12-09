# ECE143Project
ECE 143 project in UCSD. 

## Requirments

- Pandas 1.15
- matplotlib
- fbprophet
- numpy


## Data loader
Please check the Data User Manual.ipynb for details.

## File Orgnization
```
    - AirbnbData   : Dataset for Airbnb
        - Asheville : Airbnb data for Asheville
        - Athens : Airbnb data for Athens
        ...

    - COVID-19Data    : Dataset for COVID-19Data
        - california_statewide_cases.csv
        - us_all_states_history.csv
        - worldwide_history.csv

    - utils
        - $Evaluation metrics$.py        : Compute evaluation metrics
        - $DatasetName$DataSet.py        : Data loader
        - create_csv_for$DatasetName$.py : Create Namelist for dataset
        - proprcessing.py
    
    -- config_data.py : Map for country and city
    - Data User Manual.ipynb  : Demo of how to use the dataset API
    - predict.ipynb : Demo of prediction
    - scrape_insideairbnb.py : scraping script for airbnbdata, refactored data classes



