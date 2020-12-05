#!/bin/bash

for file in `ls ./AirbnbData`
    do
    python predict.py --filename $file
    done
# python predict.py --filename Denver