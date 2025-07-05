import requests
import pandas as pd
from pathlib import Path


def get_crypto_ohlcv(coin_id, days=365):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
    res = requests.get(url)

    if res.status_code != 200 or "error" in res.text.lower():
        raise Exception(f"Failed to fetch data: {res.text}")
    
    data = res.json()

    prices = pd.DataFrame(data['prices'], columns=['timestamp', 'close'])
    volumes = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'volume'])

    df = prices.merge(volumes, on='timestamp')
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    df = df.resample('1D').agg({'close': 'ohlc', 'volume': 'mean'})
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    df.dropna(inplace=True)

    df = df.sort_index()
    Path("data").mkdir(exist_ok=True)
    df.to_csv(f"data/{coin_id.upper()}.csv")

    return df
