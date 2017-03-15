from ftplib import FTP
import pickle

def get_nasdaq_tickers():
    ftp = FTP('206.200.251.105')
    ftp.login('anonymous')
    ftp.cwd('SymbolDirectory')

    with open ('nasdaqlisted.txt', 'wb') as f:
        ftp.retrbinary("RETR {}".format('nasdaqlisted.txt'), f.write)

    tickers = []
    
    with open ('nasdaqlisted.txt', 'r') as tickers_data:
        with open ('nasdaq_tickers.txt', 'w') as tickers:
            for line in tickers_data:
                tokens = line.split('|')
                if quality_stock(tokens):
                    tickers.write('{}\n'.format(tokens[0]))

                    
def quality_stock(tokens):
    if tokens[0] == 'File' or tokens[3] != 'N' or tokens[4] != 'N':
        return False
    return True

get_nasdaq_tickers()
