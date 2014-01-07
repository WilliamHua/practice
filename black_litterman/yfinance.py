#Sets up data for the black_litterman model

import pandas as pd 
import numpy as np
import math


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

def add_returns(data, returns, asset_name):
    """
    Takes a DataFrame and adds another column of returns to it

    data:       the DataFrame
    returns:    list of returns 
    asset_name: index of returns
    """
    data[asset_name] = pd.Series(returns, index=data.index)

#FIXME:CALCULATE RISK FREE RETURNS
def calc_returns(price_series):
    """
    Calculates a return given a list of prices

    price_series:       list of prices
    output:             list of returns
    """
    returns = []
    for x in range(len(price_series) - 1):
        returns.append((price_series[x + 1] - price_series[x]) /\
                price_series[x]) 
    return returns

def calc_mean(data):
    return sum(data)/len(data)

def stddev(data):
    mean = calc_mean(data)
    summation = 0
    for x in data:
        summation += (x - mean) ** 2
    return math.sqrt(summation/len(data))

def correl_matrix(assets):
    corr_matrix = np.zeroes(len(assets), len(assets))
    for i in range(len(assets)):
        for j in range(len(assets)):
            corr_matrix[i][j] = numpy.correlate(assets[i], assets[j])
            corr_matrix[j][i] = numpy.correlate(assets[i], assets[j])

    return corr_matrix 

def stddev_matrix(assets):
    #assumes len(assets) = num of assets
    #len(assets[0]) = length of time series
    dev_matrx = np.zeros(len(assets), len(assets))
    for x in range(len(assets)):
        dev_matrix[x][x] = stddev(assets[x] * 16) #annualized, 256 days in a year

    return dev_matrix

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


        
tickers = ["aapl", "cly", "dbb", "eem", "emb", "fxe", "gld", "goog", "gs", 
    "hyg", "ibm", "iyr", "tlt", "ung", "uso", "vxx", "wmt", "x", "xiv", "xom"]
prefix = "data/"
postfix = ".csv"
weights = np.array([.25147, .00014, .00013, .02181, .00186, .00011, .01745,
        .19181, .04226, .00826, .10378, .00206, .00123, .00047, .00048, .00054, 
        .13004, .00220, .00018, .22372])

returns = {}
for x in tickers:
    stock = parse_yfin(prefix + x + postfix)
    print(x + " " + str(len(stock)))
    returns.update({x:stock})

returns = pd.DataFrame(returns, columns=tickers)

print(returns["xiv"][0])
print(calc_mean(returns["aapl"])*250)
print(calc_mean(returns["cly"])*250)

