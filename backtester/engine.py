import pandas as pd

class BacktestEngine:
    def __init__(self, ticker, strategy, data, portfolio):
        self.ticker = ticker
        self.strategy = strategy
        self.data = data
        self.portfolio = portfolio

    def run(self):
        for date, row in self.data.iterrows():
            orders = self.strategy.generate_signals(self.ticker, self.data, row)
            for order in orders:
                price = row['Close']  # Simulate Market Price
                self.portfolio.update(order, price)

            market_prices = {}
            for ticker in self.portfolio.positions:
                market_prices[ticker] = row['Close']
            equity = self.portfolio.total_value({order.ticker: row['Close']})
            self.portfolio.equity_curve.append(equity)
