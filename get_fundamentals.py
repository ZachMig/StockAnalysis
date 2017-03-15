from bs4 import BeautifulSoup as bs
import urllib.request as ur
import pandas as pd

def get_fundamentals(ticker):
    html = ur.urlopen('http://finviz.com/quote.ashx?t={}'.format(ticker)).read()
    soup = bs(html, 'lxml')

    fundamentals = []
    indices = ['Market Cap', 'PEG', 'P/FCF', 'P/C', 'P/B', 'P/E', 'EPS (ttm)', 'EPS Q/Q', \
               'Debt/Eq', 'LT Debt/Eq', 'Cash/sh', 'Income', 'Sales', 'Avg Volume', \
               'Short Ratio', 'Beta', 'Book/sh', 'Cash/sh', 'Volatility']

    for fundamental in indices:
        cursor = soup.find(text = fundamental)
        fundamentals.append(cursor.find_next(class_='snapshot-td2').text)

    df = pd.DataFrame({'Stat':indices, 'Value':fundamentals})
    df.set_index(['Stat'], inplace=True)
    
    return df

#print(get_fundamentals('AAPL'))
