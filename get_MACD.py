import pandas as pd
import matplotlib.pyplot as plt
import pickle

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

##    macd.plot()
##    plt.show()

    return macd
    
##get_MACD('AAAP')
