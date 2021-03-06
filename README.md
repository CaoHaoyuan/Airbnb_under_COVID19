# ECE143Project
ECE 143 project in UCSD. 

## Requirments

- Pandas 1.15
- matplotlib
- fbprophet
- numpy

visualization requirements
- colorcet
- holoview
- plotly


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
    
    - prediction_result : Results plots
    
    - csv_result : Results in CSV files of different cities
        - Asheville_prediction_data.csv
        - Asheville_real_data.csv
        ...
    
    - csv_result_country : Results in CSV files of different countries
        - Australia_prediction_data.csv
        - Australia_real_data.csv
        ...
    
    
    - config_data.py : Map for country and city
    - Data User Manual.ipynb  : Demo of how to use the dataset API
    - predict.ipynb : Demo of prediction
    - heatmap.ipynb : Demo of heatmap
    - scrape_insideairbnb.py : scraping script for airbnbdata, refactored data classes
    - predict.py : script for figure prediction
    - predict_dataframe.py : script for save prediction as csv files 
    - main.sh : bash file for get all the prediction results
    - get_difference.sh : bash file for get all the difference of prediction with the real value
```

## Usage
1. Get the prediction result
```
     bash main.sh
```
    
2. Get the difference between the prediction and the real data
```
     bash get_difference.sh
```
