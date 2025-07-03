class Order:
    def __init__(self, ticker, quantity, order_type, price=None):
        self.ticker = ticker
        self.quantity = quantity
        self.order_type = order_type  # 'market' or 'limit'
        self.price = price


class Position:
    def __init__(self):
        self.quantity = 0
        self.avg_price = 0.0

    def update(self, qty, price):
        if self.quantity + qty == 0:
            self.quantity = 0
            self.avg_price = 0
        else:
            new_qty = self.quantity + qty
            self.avg_price = (self.avg_price * self.quantity + price * qty) / new_qty
            self.quantity = new_qty


class Portfolio:
    def __init__(self, cash=100000):
        self.cash = cash
        self.positions = {}
        self.equity_curve = []

    def update(self, order, close_price):
        cost = order.quantity * close_price
        self.cash -= cost
        if order.ticker not in self.positions:
            self.positions[order.ticker] = Position()
        self.positions[order.ticker].update(order.quantity, close_price)

    def total_value(self, market_prices):
        value = self.cash
        for ticker, pos in self.positions.items():
            value += pos.quantity * market_prices.get(ticker, 0)
        return value
    