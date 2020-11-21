import os
# import datetime
from urllib.request import urlopen

# from dateutil.parser import parse
# import threading

assert 'QUANDL_KEY' in os.environ
quandl_api_key = os.environ['QUANDL_KEY']


class nasdaq():
    def __init__(self):
        self.output = './stock_data'
        self.company_list = './companylist.csv'

    def build_url(self, symbol):
        url = 'https://www.quandl.com/api/v3/datasets/WIKI/{}.csv?api_key={}'.format(symbol, quandl_api_key)
        return url

    def symbols(self):
        symbols = []
        with open(self.company_list, 'r') as f:
            next(f)
            for line in f:
                symbols.append(line.split(',')[0].strip())
        return symbols


def download(i, symbol, url, output):
    data_file = os.path.join(output, symbol)
    if os.path.exists(data_file):
        return
    else:
        try:
            print('Downloading {} {}'.format(symbol, i))
            response = urlopen(url)
            quotes = response.read()
            lines = quotes.decode().strip().split('\n')
            with open(data_file, 'w') as f:
                for i, line in enumerate(lines):
                    f.write(line + '\n')
        except Exception as e:
            print('Failed to download {}'.format(symbol))
            print(e)


def download_all():
    if not os.path.exists('./stock_data'):
        os.makedirs('./stock_data')

    nas = nasdaq()
    for i, symbol in enumerate(nas.symbols()):
        url = nas.build_url(symbol)
        download(i, symbol, url, nas.output)


if __name__ == '__main__':
    download_all()
