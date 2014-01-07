import yfinance
import numpy as np
import pandas as pd
import math
from scipy.stats.stats import pearsonr

def calc_mean(data):
    return sum(data)/len(data)

def stddev(data):
    mean = calc_mean(data)
    summation = 0
    for x in data:
        summation += (x - mean) ** 2
    return math.sqrt(summation/len(data))

def correl_matrix(assets, tickers):
    corr_matrix = np.zeros((len(assets.columns), len(assets.columns)))
    for i in range(len(assets.columns)):
        for j in range(len(assets.columns)):
            corr_matrix[i][j] = pearsonr(assets[tickers[i]], 
                    assets[tickers[j]])[0]
            corr_matrix[j][i] = pearsonr(assets[tickers[i]], 
                    assets[tickers[j]])[0]

    return corr_matrix 

def stddev_matrix(assets, tickers):
    #assumes len(assets) = num of assets
    #len(assets[0]) = length of time series
    dev_matrix = np.zeros((len(assets.columns), len(assets.columns)))
    for x in range(len(assets.columns)):
        dev_matrix[x][x] = stddev(assets[tickers[x]])*16 #annualized, 256 days in a year

    return dev_matrix

tickers = ["aapl", "cly", "dbb", "eem"]#, "emb", "fxe", "gld", "goog", "gs", 
#    "hyg", "ibm", "iyr", "tlt", "ung", "uso", "vxx", "wmt", "x", "xiv", "xom"]
prefix = "data/"
postfix = ".csv"
weights = np.array([.25147, .00014, .00013, .02181, .00186, .00011, .01745,
        .19181, .04226, .00826, .10378, .00206, .00123, .00047, .00048, .00054, 
        .13004, .00220, .00018, .22372])

returns = {}
for x in tickers:
    stock = yfinance.parse_yfin(prefix + x + postfix)
    returns.update({x:stock})

returns = pd.DataFrame(returns, columns=tickers)
dev_matrix = stddev_matrix(returns, tickers)
corr_matrix = correl_matrix(returns, tickers)

#print(returns["xiv"][0])
print(calc_mean(returns["aapl"])*250)
print(calc_mean(returns["cly"])*250)

