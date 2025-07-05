from backtester.core import Order


class SampleStrategy:
    def __init__(self):
        self.last_price = None
        self.position = False

    def generate_signals(self, ticker, data, row):
        price = row['Close']
        orders = []

        if not self.position and price > row['Open']:
            orders.append(Order(ticker=ticker, quantity=100, order_type='market'))
            self.position = True
        elif self.position and price < row['Open']:
            orders.append(Order(ticker=ticker, quantity=100, order_type='market'))
            self.position = False
        return orders
    