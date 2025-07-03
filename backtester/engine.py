import pandas as pd

class BacktestEngine:
    def __init__(self, strategy, data, portfolio):
        self.strategy = strategy
        self.data = data
        self.portfolio = portfolio

    def run(self):
        for date, row in self.data.iterrows():
            orders = self.strategy.generate_signals(date, row)
            for order in orders:
                price = row['Close']  # Simulate Market Price
                self.portfolio.update(order, price)
            equity = self.portfolio.total_value({order.ticker: row['Close']})
            self.portfolio.equity_curve.append(equity)
            