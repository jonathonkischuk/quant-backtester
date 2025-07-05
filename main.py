import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import math

from backtester.core import Portfolio
from backtester.engine import BacktestEngine
from backtester.performance import calculate_cagr, calculate_sharpe, calculate_max_drawdown
from strategies.sample_strategy import SampleStrategy
from utils.data_fetcher import download_stock_data
from utils.crypto_fetcher import get_crypto_ohlcv
from utils.data_cleaner import clean_price_data

# -------------------------
# Configuration
# -------------------------

stock_tickers = ["AMZN", "EPD", "ET", "GOOGL", "IBM", "META", "MSFT", "PG", "RGTI", "RITM", "TSM"]
crypto_ids = {
    "JASMY": "jasmycoin",
    "RENDER": "render-token",
    "BTC": "bitcoin",
    "ADA": "cardano",
    "ALGO": "algorand",
    "XLM": "stellar",
    "XRP": "ripple"
}

os.makedirs("data", exist_ok=True)

# -------------------------
# Download Stock Data
# -------------------------

for ticker in stock_tickers:
    file_path = f"data/{ticker}.csv"
    if not os.path.exists(file_path):
        print(f"Downloading stock data for {ticker}...")
        df_raw = download_stock_data(ticker, start="2015-01-01", end="2025-07-01", save=False)
        df_cleaned = clean_price_data(df_raw, is_df=True)
        df_cleaned.to_csv(file_path)
    else:
        print(f"Stock data for {ticker} already exists. Skipping download.")

# -------------------------
# Download Crypto Data
# -------------------------

import time
for ticker, coin_id in crypto_ids.items():
    file_path = f"data/{ticker}.csv"
    if not os.path.exists(file_path):
        try:
            print(f"Fetching crypto data for {ticker}...")
            df = get_crypto_ohlcv(coin_id, days=365)
            df_cleaned = clean_price_data(df, is_df=True)
            df_cleaned.to_csv(file_path)
            time.sleep(2)
        except Exception as e:
            print(f"Failed to fetch crypto data for {ticker} ({coin_id}): {e}")
    else:
        print(f"Crypto data for {ticker} already exists. Skipping download.")

# -------------------------
# Run Backtests
# -------------------------

results = []

all_files = [f for f in os.listdir("data") if f.endswith(".csv")]
for cleaned_file in all_files:
    ticker = cleaned_file.replace(".csv", "")
    print(f"\n--- Backtesting {ticker} ---")

    try:
        df = pd.read_csv(os.path.join("data", cleaned_file), index_col="Date", parse_dates=True)

        if df.shape[0] < 100 or 'Close' not in df.columns:
            print(f"Not enough data or missing 'Close' column for {ticker}. Skipping.")
            continue

        portfolio = Portfolio()
        strategy = SampleStrategy()
        engine = BacktestEngine(ticker, strategy, df, portfolio)
        engine.run()

        equity = pd.Series(portfolio.equity_curve, index=df.index[:len(portfolio.equity_curve)])
        returns = equity.pct_change().dropna()

        print(f"CAGR: {calculate_cagr(equity):.2%}")
        print(f"Sharpe: {calculate_sharpe(returns):.2f}")
        print(f"Max Drawdown: {calculate_max_drawdown(equity):.2%}")

        results.append((ticker, equity))

    except Exception as e:
        print(f"Failed to backtest {ticker}: {e}")

# -------------------------
# Plot All Results Together
# -------------------------

cols = 3
rows = math.ceil(len(results) / cols)
fig, axes = plt.subplots(rows, cols, figsize=(20, 5 * rows))
axes = axes.flatten()

for i, (ticker, equity) in enumerate(results):
    axes[i].plot(equity)
    axes[i].set_title(f"Equity Curve: {ticker}")
    axes[i].set_xlabel("Date")
    axes[i].set_ylabel("Portfolio Value")
    axes[i].grid(True)

# Hide unused axes
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()
