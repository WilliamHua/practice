import pandas as pd 


def parse_yfin(file_name):
    date = []   
    adj_close_price = []

    #i can probably encapsulate this
    with open(file_name) as f:
        data = f.readline()
        for x in reversed(list(f)):
            split_data = x.rstrip().split(',')
            date.append(split_data[0])
            adj_close_price.append(float(split_data[6]))

    returns = get_returns(adj_close_price)

    return format_returns(date[1:], returns)

def format_returns(date, returns):
    return pd.DataFrame({"date":date, "return":returns}, 
            columns=["date", "return"])

def get_returns(price_series):
    returns = []
    for x in range(len(price_series) - 1):
        returns.append((price_series[x + 1] - price_series[x]) /\
                price_series[x])
    return returns
        
tickers = ["aapl", "cly", "dbb", "eem", "emb", "fxe", "gld", "goog", "gs", \
    "hyg", "ibm", "iyr", "tlt", "ung", "uso", "vxx", "wmt", "x", "xiv", "xom"]
prefix = "data/"
postfix = ".csv"
weights = []
frame = parse_yfin(prefix + tickers[0] + postfix)
print(frame["return"][0])

