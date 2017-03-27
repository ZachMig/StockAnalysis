from ftplib import FTP
import pickle
import datetime as dt
import requests
import os
import pandas as pd
import pandas_datareader.data as web

def get_nasdaq_tickers():
    nasdaq_ftp = '206.200.251.105'
    nasdaq_path = '/symboldirectory/'
    filename = 'nasdaqlisted.txt'

    with open(filename, 'wb') as localfile:
        ftp = FTP(nasdaq_ftp)
        ftp.login('anonymous')
        ftp.cwd(nasdaq_path)
        ftp.retrbinary('RETR {}'.format(filename), localfile.write, 1024)
        ftp.quit()


    tickers = []
    badtickers = ['ADXSW', 'AGFSW', 'AHPAU', 'AHPAW', 'APOPW', 'AXARW', 'BVXVW', 'CATYW', 'CBMXW', 'CDEVW', 'CETXW', 'CFCOW', 'CHEKW', 'CLIRW', 'CLRBZ', 'COWNL', 'CPAAU', 'CPAAW', 'CYHHZ', 'CYRXW', 'CYTXW', 'DELTW', 'DRIOW', 'ELECU', 'ELECW', 'EYEGW', 'FNTEU', 'GFNSL', 'GPACU', 'GPACW', 'GPIAW', 'GSHTU', 'GTYHW', 'HBANN', 'HCACU', 'HCACW', 'HCAPL', 'HUNTU', 'HUNTW', 'INSEW', 'JASNW', 'JSYNR', 'JSYNW', 'KLREW', 'KTOVW', 'LCAHW', 'LINDW', 'LMFAW', 'MACQW', 'MIIIW', 'MOGLC', 'MRDNW', 'MSDIW', 'MTFBW', 'NHLDW', 'NUROW', 'NXEOW', 'NXTDW', 'OACQR', 'OACQU', 'OACQW', 'ONSIW', 'ONTXW', 'OPGNW', 'OPXAW', 'OXBRW', 'PAACR', 'PAACW', 'RXIIW', 'SCACW', 'SGLBW', 'SHIPW', 'SHLDW', 'SNFCA', 'SNGXW', 'SNHNL', 'SNOAW', 'SOHOM', 'SRTSW', 'STLRU', 'STLRW', 'TACOW', 'TALL', 'TWNKW', 'VKTXW', 'WHLRD', 'WVVIP', 'WYIGW', 'ZIONZ', 'ZNWAA']
    with open(filename, 'r') as f:
        for line in f:
            tickerdata = line.split('|')
            if tickerdata[3] == 'Y' or tickerdata[4] != 'N' or tickerdata[6] == 'Y' or tickerdata[0] in badtickers:
                continue
            tickers.append(tickerdata[0])
    with open('nasdaqtickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)


def pull_data():
    with open('nasdaqtickers.pickle', 'rb') as f:
        tickers = pickle.load(f)
    
    today = dt.datetime.today()
    start = dt.datetime(today.year-1, today.month, today.day)
    finish = dt.datetime(today.year, today.month, today.day)
    
    for ticker in tickers[:100]:
        print(ticker)
        if not os.path.exists('stock_dfs/past_five_years'):
            os.makedirs('stock_dfs/past_five_years')
##        if os.path.exists('stock_dfs/past_year/{}.csv'.format(ticker)):
##            print("Already have, skipping {}".format(ticker))
##            continue
        df = web.DataReader(ticker, 'yahoo', start, finish)
        df.to_csv('stock_dfs/past_year/{}.csv'.format(ticker))



    
#get_nasdaq_tickers()    
pull_data()
