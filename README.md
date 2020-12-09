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

    - COVID-19Data    : Dataset for COVID-19Data

    - datasplit
        - $DatasetName$_images.csv              : Name index of images
        - $DatasetName$_reports.csv             : Name index of reports
        - $DatasetName$_report_$subset$.csv :Data-split for openi and MIMIC-CXR dataset

    - models
        - AttnGAN.py    : Reimplementation of AttnGAN
        - StackGAN.py   : Reimplementation of StackGAN
        - Encoder.py
        - Decoder.py
        - Discriminator.py
        - HALSTM.py     : Implementation of Word Attntion/Sentence Attntion
        - Siamese.py    : View Consistency Network

    - utils
        - $Evaluation metrics$.py        : Compute evaluation metrics
        - $DatasetName$DataSet.py        : Data loader
        - create_csv_for$DatasetName$.py : Create Namelist for dataset
        - proprcessing.py

    - Data User Manual.ipynb  : Demo of how to use the dataset API
    - predict.ipynb : Demo of prediction
    - scrape_insideairbnb.py : scraping script for airbnbdata, refactored data classes



