# 📊 Quant Backtester

A modular, extensible Python-based backtesting engine for evaluating quantitative trading strategies. This tool enables traders, data scientists, and quant researchers to simulate, analyze, and iterate on strategies using historical market data with precision and flexibility.

---

## 🔧 Features

- ✅ Modular architecture for clean strategy plugins
- ✅ Support for market and limit orders
- ✅ Portfolio and order management
- ✅ Performance metrics: Sharpe Ratio, CAGR, Max Drawdown
- ✅ Slippage and commission modeling (coming soon)
- ✅ Docker support for isolated and portable execution

---

## 📁 Project Structure

```bash
quant-backtester/
├── backtester/
│ ├── core.py # Order, Position, Portfolio classes
│ ├── engine.py # BacktestEngine logic
│ └── performance.py # CAGR, Sharpe, Max Drawdown
├── strategies/
│ └── sample_strategy.py # Example strategy logic
├── data/
│ └── SPY.csv # Sample historical data (OHLC)
├── reports/
│ └── performance.csv # Optional output
├── main.py # Entry point to run backtest
├── requirements.txt # Dependencies
└── Dockerfile # Containerization setup

---

## 🚀 How It Works

1. Load OHLC historical data from CSV
2. Use strategy plugin to generate buy/sell signals
3. Orders are executed using simulated prices
4. Portfolio and equity are updated
5. Performance metrics are calculated and displayed

---

## 📈 Performance Metrics

| Metric         | Description                                            |
|----------------|--------------------------------------------------------|
| **CAGR**       | Compound Annual Growth Rate over the backtest period   |
| **Sharpe Ratio** | Risk-adjusted return (higher = better risk/reward)    |
| **Max Drawdown** | Largest peak-to-trough equity decline                |

---

## 🧪 Running Locally

### 1. Clone the Repository

git clone https://github.com/yourusername/quant-backtester.git
cd quant-backtester

---

python -m venv venv
source venv/bin/activate  
### On Windows: venv\Scripts\activate

## Install Dependencies
pip install -r requirements.txt

## Run the Backtest
python main.py

## Output Metric Example
CAGR: 6.82%
Sharpe: 1.35
Max Drawdown: -12.50%


---

## RUNNING WITH DOCKER

### 1) Build the Docker Image
docker build -t quant-backtester .

### 2) Run the Container
docker run --rm quant-backtester

### 3) Export Results (Optional)
docker run --rm -v $(pwd)/reports:/app/reports quant-backtester

