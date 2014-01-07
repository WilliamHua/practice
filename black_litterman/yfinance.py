#Sets up data for the black_litterman model

import pandas as pd 
import numpy as np


def parse_yfin(file_name):
    """
    Parses a CSV file from Yahoo Finance and reutrns the adjusted close

    file_name:          directory (abs or rel) to the file
    output:             list of daily returns
    
    """
    date = []   
    adj_close_price = []

    #i can probably encapsulate this even more
    with open(file_name) as f:
        data = f.readline()
        for x in reversed(list(f)):
            split_data = x.rstrip().split(',')
            date.append(split_data[0])
            adj_close_price.append(float(split_data[6]))

    returns = calc_returns(adj_close_price)

    return returns#, date[1:]

#FIXME:CALCULATE RISK FREE RETURNS
def calc_returns(price_series):
    """
    Helper method to calculate a return given a list of prices

    price_series:       list of prices
    output:             list of returns
    """
    returns = []
    for x in range(len(price_series) - 1):
        returns.append((price_series[x + 1] - price_series[x]) /\
                price_series[x]) 
    return returns

#-------- possible will remove

#calculates mean annual return given
def mean_ann_returns(daily_returns):
    ann_return = 1
    for x in range(len(daily_returns)):
        ann_return *= (daily_returns[x] + 1)
    return ann_return/(len(daily_returns)/250)

def format_returns(date, returns, asset_name):
    """
    Creates DataFrame of the date and the returns indexed by the asset name

    date:           list of dates
    returns:        list of returns
    asset_name:     index of returns
    output:         DataFrame of date and returns indexed by asset name
    """
    return pd.DataFrame({"date":date, asset_name:returns}, 
            columns=["date", asset_name])


        

