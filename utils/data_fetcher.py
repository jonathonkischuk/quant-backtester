import yfinance as yf
import pandas as pd
from pathlib import Path


def download_stock_data(ticker, start='2010-01-01', end=None, save=True):
    df = yf.download(ticker, start=start, end=end)
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() for col in df.columns]
    else:
        df.columns = [col.capitalize().strip() for col in df.columns]

    df = df.dropna()
    df = df.sort_index()

    if save:
        Path("data").mkdir(exist_ok=True)
        df.to_csv(f"data/{ticker}.csv")

    return df
