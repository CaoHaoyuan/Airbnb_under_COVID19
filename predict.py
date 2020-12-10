import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mpl_toolkits
import airbnb_dataset as ad
from fbprophet import Prophet
import argparse

def main(args):
    AD = ad.AirbnbDataset()
    city = args.filename
    df = AD.get_reviews_for_city(city, per_month = True, per_week = False)
    df = df.reset_index(drop = False)
    df['index'] = df.index
    df['date'] = df['year'].map(str) + '-' + df['month'].map(str) + '-1'
    r = df[df.year == 2020].index.tolist()[0] 
    train = df[:r]

    train = train[["date","size"]]
    train = train.rename(columns = {"date":"ds","size":"y"})
    m = Prophet()
    m.fit(train)
    future = m.make_future_dataframe(periods=12, freq='MS')
    # future.tail()
    prediction = m.predict(future)
    m.plot(prediction)
    plt.title("Prediction of number of reviews using the Prophet", fontsize=20)
    plt.xlabel("Date", fontsize=18)
    plt.ylabel("Number of reviews", fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.savefig(f'./prediction_result/{city}.png', bbox_inches='tight')
    plt.show()


    df = df[["date","size"]]
    df = df.rename(columns = {"date":"ds","size":"y"})
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=0, freq='MS')
    # future.tail()
    prediction = m.predict(future)
    m.plot(prediction)
    plt.title("Real number of reviews", fontsize=20)
    plt.xlabel("Date", fontsize=18)
    plt.ylabel("Number of reviews", fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend()
    plt.savefig(f'./prediction_result/{city}_original.png', bbox_inches='tight')
    plt.show()

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--filename', type=str, default = None)
args = parser.parse_args()
main(args)