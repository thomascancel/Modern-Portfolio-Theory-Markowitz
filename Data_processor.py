import os
import yfinance as yf
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta


class DataLoader:
    """A class for loading the data from yahoo finance"""

    def __init__(self, tickers, benchmark, col, dir):
        self.tickers = tickers
        self.benchmark = benchmark
        self.column = col
        self.dir = dir

    def get_data(self):
        start_date = dt.datetime.now() - relativedelta(years=1) + relativedelta(days=1)
        end_date = dt.datetime.now()
        data = yf.download(self.tickers, start_date, end_date)[self.column]
        data = self.return_data(data)
        benchmark = pd.DataFrame(yf.download(self.benchmark, start_date, end_date)[self.column])
        benchmark = self.return_data(benchmark)
        benchmark.columns = [self.benchmark]
        data.to_excel(os.path.join(self.dir, 'CAC40_stocks.xlsx'))
        benchmark.to_excel(os.path.join(self.dir, 'CAC40_index.xlsx'))

    def return_data(self, data):
        ret = data.pct_change(1)
        ret.dropna(how='any', inplace=True)
        return ret
