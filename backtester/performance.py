# Key Financial Metrics

def calculate_cagr(equity_curve, periods_per_year=252):
    total_return = equity_curve[-1] / equity_curve[0]
    num_years = len(equity_curve) / periods_per_year
    return (total_return ** (1 / num_years)) - 1


def calculate_sharpe(returns, risk_free_rate=0.01):
    excess = returns - risk_free_rate / 252
    return (excess.mean() / excess.std()) * (252 ** 0.5)


def calculate_max_drawdown(equity_curve):
    peak = equity_curve.cummax()
    drawdown = (equity_curve - peak) / peak
    return drawdown.min()

