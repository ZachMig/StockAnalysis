import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import pickle

def process_tickers(filename):
    
##  Get last 5 years of data    
    today = dt.datetime.today()
    start = dt.datetime(today.year-5, today.month, today.day)
    
    with open(filename, 'r') as f:
        for ticker in f:
            ticker = ticker.rstrip()
            df = web.DataReader(ticker, 'yahoo', start, today)
            pickle.dump(df, open('{}.pickle'.format(ticker), 'wb'))

process_tickers('nasdaq_top5.txt')
