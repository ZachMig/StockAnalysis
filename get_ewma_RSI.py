import pandas as pd
import pickle
import matplotlib.pyplot as plt

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
    
##    rsi.plot()
##    plt.legend(['RSI'])
##    plt.show()  

#get_ewma_RSI('AAAP', 14)
