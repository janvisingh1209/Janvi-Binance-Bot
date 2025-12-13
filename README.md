# Binance Trading Bot

## Objective
This project is a CLI-based trading bot for Binance USDT-M Futures. It supports multiple order types with robust logging, input validation, and testnet integration. The bot allows you to execute both core and advanced trading strategies.

---

## File Structure
BinanceBot
│
├── src/
│ ├── market_orders.py # Market order logic
│ ├── limit_orders.py # Limit order logic
│ ├── advanced/
│ │ ├── oco.py # One-Cancels-the-Other orders
│ │ ├── twap.py # Time-Weighted Average Price orders
│ │ └── grid_order.py # Grid orders
│
├── bot.log # Logs of API calls, errors, and executions
├── .env # API keys (BINANCE_API_KEY, BINANCE_API_SECRET)
├── README.md # Project documentation
└── report.pdf # Assignment report with screenshots & explanations
---

## Setup

1. **Clone the repository** or extract the zip file.

2. **Install dependencies**:

```bash
pip install requests python-dotenv

3. Create a .env file in the project root with your Binance Testnet API keys:

BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret 

4. Logs are automatically written to bot.log in the project root.

 5.Usage

All scripts are CLI-based. Below are examples for each type of order:

6.Market Orders
Execute a market order:

python src/market_orders.py SYMBOL BUY/SELL QUANTITY


Example:

python src/market_orders.py BTCUSDT BUY 0.01

7.Limit Orders

Execute a limit order:
python src/limit_orders.py SYMBOL BUY/SELL QUANTITY PRICE
Example:
python src/limit_orders.py BTCUSDT SELL 0.01 95000

8.OCO Orders
Place a One-Cancels-the-Other order with optional offsets:
python src/advanced/oco.py SYMBOL BUY/SELL QUANTITY [TP_OFFSET STOP_OFFSET]
Example:
python src/advanced/oco.py BTCUSDT BUY 0.01 1000 1000

9.TWAP Orders
Place a Time-Weighted Average Price order:
python src/advanced/twap.py SYMBOL BUY/SELL TOTAL_QTY CHUNKS INTERVAL
Example:
python src/advanced/twap.py BTCUSDT BUY 0.01 5 10

10.Grid Orders
Place a grid order between two prices, split into steps:
python src/advanced/grid_order.py SYMBOL BUY/SELL START_PRICE END_PRICE STEPS QUANTITY
Example:
python src/advanced/grid_order.py BTCUSDT BUY 90000 85000 5 0.001

Features:
Core Orders
Market Orders
Limit Orders
Advanced Orders
Stop-Limit Orders
OCO Orders
TWAP Orders
Grid Orders
Validation
Symbol format (must end with USDT)
Positive quantities and prices
Side validation (BUY/SELL)
Logging
Structured logging of orders, errors, and responses
Logs saved to bot.log
Testnet Integration
All orders executed on Binance Testnet
Safe for testing without real funds

Notes:

used Testnet API keys for testing.

Adjust offsets and intervals according to your strategy for TWAP, OCO, and Grid orders.

Review bot.log for detailed execution and error tracking.

Submission guidelines:

Include the following in a single zip named [your_name]_binance_bot.zip:

[project_root]/
│
├── src/           # All source code
├── bot.log        # Log file
├── README.md      # Documentation
└── report.pdf     # Analysis with screenshots & explanations