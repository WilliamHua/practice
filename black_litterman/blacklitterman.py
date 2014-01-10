# Black Litterman based off of http://corporate.morningstar.com/ib/documents/MethodologyDocuments/IBBAssociates/BlackLitterman.pdf

import yfinance
from numpy import dot
from numpy.linalg import inv
import numpy as np
import pandas as pd
import math
from scipy.stats.stats import pearsonr

def returns(tickers, rate):
    rets = {}
    for x in tickers:
        stock = yfinance.parse_yfin(prefix + x + postfix)
        rets.update({x:risk_free_rate(stock, rate)})
    return rets;

def risk_free_rate(stock, rate):
    daily_rate = math.pow(1 + rate, 1/250.0) - 1
    for x in range(len(stock)):
        stock[x] = stock[x] - daily_rate
    return stock

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

def cov_matrix(assets, tickers):
    corr_matrix = correl_matrix(assets, tickers)
    dev_matrix = stddev_matrix(assets, tickers)
    return np.dot(np.dot(dev_matrix, corr_matrix), dev_matrix)

def diagonalize(data):
    for x in range(len(data)):
        for y in range(len(data)):
            if x != y:
                data[x][y] = 0
    return data

def risk_profile(sharpe, weights, covar_matrix):
    return sharpe/math.sqrt(dot(dot(weights.T, covar_matrix), weights))

def excess(covar_matrix, weights, risk):
    return dot(covar_matrix, weights) * risk

def error(covar_matrix, tau):
    return inv(covar_matrix * tau)

def omega_inverse(views, covar_matrix, tau):
    return inv(diagonalize(dot(dot((views * tau), covar_matrix), views.T)))

def first_multiplier(return_error, views, omega_inv):
    return return_error + dot(dot(views.T, omega_inv), views) 

def second_multiplier(return_error, equal_excess, views, omega_inv, return_views):
    return dot(return_error, equal_excess) + dot(dot(views.T, omega_inv), return_views)

def post_exp_ret(first_mult, second_mult):
    return dot(inv(first_mult), second_mult)

def post_cov(return_error, views, omega_inv):
        return inv(return_error + dot(dot(views.T, omega_inv.T), views))

def new_weights(risk, covar_matrix, post_ret):
        return 1/risk * dot(inv(covar_matrix), post_ret)

def new_weights_all(excess_return, weights, rets, tickers, views, return_views):
        tau = 1/len(rets[tickers[0]])
        covar_matrix = cov_matrix(rets, tickers)
        risk = risk_profile(excess_return, weights, covar_matrix)
        equal_excess = excess(covar_matrix, weights, risk)
        return_error = error(covar_matrix, tau)
        omega_inv = omega_inverse(views, covar_matrix, tau)
        first_mult = first_multiplier(return_error, views, omega_inv)
        second_mult = second_multiplier(return_error, equal_excess, views, omega_inv, return_views)
        post_ret = post_exp_ret(first_mult, second_mult)
        return 1/risk * dot(inv(covar_matrix), post_ret)
        

tickers = ["aapl", "cly", "dbb", "eem", "emb", "fxe", "gld", "goog", "gs", 
    "hyg", "ibm", "iyr", "tlt", "ung", "uso", "vxx", "wmt", "x", "xiv", "xom"]
prefix = "data/"
postfix = ".csv"
weights = np.array([.25147, .00014, .00013, .02181, .00186, .00011, .01745,
        .19181, .04226, .00826, .10378, .00206, .00123, .00047, .00048, .00054, 
        .13004, .00220, .00018, .22372])

###### prior equilibrium distribution

rets = returns(tickers, .001)
tau = 1/len(rets[tickers[0]])
rets = pd.DataFrame(rets, columns=tickers)
covar_matrix = cov_matrix(rets, tickers)
risk = risk_profile(.5, weights, covar_matrix)
equal_excess = excess(covar_matrix, weights, risk)

#what = map(calc_mean, returns)

#weights = dot(inv((cov_matrix(rets, tickers) * risk)), equal_excess) --- just to check work
return_error = error(covar_matrix, tau)

######views
views = np.array([
    [1, 0, 0, 0, 0, 0 ,-1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
    [0, 0, 0, 0, 0, 0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]])#,
#    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
return_views = np.array([.10, .07])#, .05])
omega_inv = omega_inverse(views, covar_matrix, tau)

###### combining
first_mult = first_multiplier(return_error, views, omega_inv)
second_mult = second_multiplier(return_error, equal_excess, views, omega_inv, return_views)
post_ret = post_exp_ret(first_mult, second_mult)
post_covar = post_cov(return_error, views, omega_inv)
new_weight = new_weights(risk, covar_matrix, post_ret)
###testing

#dev_matrix = np.array([[.07, 0, 0, 0],
#    [0, .12, 0, 0],
#    [0, 0, .3, 0],
#    [0, 0, 0, .6]])
#weights = np.array([.05, .40, .45, .1])
#corr_matrix = np.array([[1, .8, .5, .4],
#    [.8, 1, .7, .5],
#    [.5, .7, 1, .8],
#    [.4, .5, .8, 1]])
#
#risk = 2.24
#covar_matrix = dot(dot(dev_matrix, corr_matrix), dev_matrix)
#omega_inv = omega_inverse(views, covar_matrix, .0083)
#return_error = error(covar_matrix, .0083)
#equal_excess = excess(covar_matrix, weights, risk)
#first_mult = first_multiplier(return_error, views, omega_inv)
#second_mult = second_multiplier(return_error, equal_excess, views, omega_inv, return_views)
#post_ret = post_exp_ret(first_mult, second_mult)
##posterior = inv(equal_return_error2 + dot(dot(views.T, omega_inverse2.T), views))
#new_weight = new_weights(risk, covar_matrix, post_ret)
