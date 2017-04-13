import pandas as pd
import pickle

def get_ewma_RSI(ticker, period):
    df = pickle.load( open('{}.pickle'.format(ticker), 'rb'))
    df = df[['Adj Close']]

    diff = df.diff()[1:]

    gains, losses = diff.copy(), diff.copy()

    gains[gains < 0] = 0
    losses[losses > 0] = 0

    rolling_gains = gains.ewm(ignore_na=False, min_periods=0, adjust=True, com=14).mean()
    rolling_losses = losses.abs().ewm(ignore_na=False, min_periods=0, adjust=True, com=14).mean()

    rs = rolling_gains / rolling_losses
    rsi = 100 - (100 / (1 + rs))

    rsi.rename(columns = {'Adj Close' : 'RSI'}, inplace=True)

    return rsi

def get_MACD(ticker):
    df = pickle.load( open('{}.pickle'.format(ticker), 'rb'))
    df = df[['Adj Close']]
    
    twelve_day_ema = df.ewm(ignore_na=False, min_periods=0, adjust=True, com=12).mean()
    twentysix_day_ema = df.ewm(ignore_na=False, min_periods=0, adjust=True, com=26).mean()

    macd_base = twelve_day_ema - twentysix_day_ema
    macd_base.rename(columns = {'Adj Close' : 'MACD'}, inplace=True)    
    
    macd_nine_day_ema = macd_base.ewm(ignore_na=False, min_periods=0, adjust=True, com=9).mean()
    macd_nine_day_ema.rename(columns = {'MACD' : 'Signal Line'}, inplace=True)
        
    macd = pd.concat([macd_base, macd_nine_day_ema], 1)

    return macd

def get_OBV(ticker):
    df = pickle.load( open('{}.pickle'.format(ticker), 'rb'))
    close = df[['Adj Close']]
    diff = close.diff()[1:]
    volumes = [0]
    obv = [0]
    cumsum = 0
    
    i = 1
    for row in diff.itertuples(index=False):
        if row[0] > 0:
            volumes.append(df.ix[i,4])
        elif row[0] < 0:
            volumes.append((-1) * df.ix[i,4])
        else:
            volumes.append(0)
        obv.append(obv[i-1] + volumes[i])
        i += 1

    return pd.Series(obv)
