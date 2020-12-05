#!/bin/bash

for file in `ls ./AirbnbData`
    do
    python predict_dataframe.py --filename $file
    done
# python predict_dataframe.py --filename Denver