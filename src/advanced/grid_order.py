import os
import sys
import time
import hmac
import hashlib
import requests
import logging
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load API keys
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
BASE_URL = "https://testnet.binance.vision"

# Logging setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, '..', '..', 'bot.log')
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def log_info(msg):
    print(msg)
    logging.info(msg)

def log_error(msg):
    print(f"ERROR: {msg}")
    logging.error(msg)

# Sign request
def sign(params):
    query = urlencode(params)
    signature = hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    return f"{query}&signature={signature}"

# Get current market price
def get_current_price(symbol):
    url = f"{BASE_URL}/api/v3/ticker/price?symbol={symbol}"
    res = requests.get(url).json()
    return float(res['price'])

# Place limit order
def place_limit_order(symbol, side, quantity, price):
    side = side.upper()
    symbol = symbol.upper()
    log_info(f"Placing grid LIMIT order: {side} {quantity} {symbol} at {price}")

    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "quantity": quantity,
        "price": price,
        "timeInForce": "GTC",
        "timestamp": int(time.time() * 1000),
        "recvWindow": 5000
    }
    signed = sign(params)
    url = f"{BASE_URL}/api/v3/order?{signed}"
    headers = {"X-MBX-APIKEY": API_KEY}

    try:
        response = requests.post(url, headers=headers)
        log_info(f"Response: {response.status_code} | {response.json()}")
    except Exception as e:
        log_error(f"Error placing order: {e}")

# Place grid orders automatically around current price
def place_grid_orders(symbol, side, quantity, steps=5, lower_pct=0.98, upper_pct=1.02):
    current_price = get_current_price(symbol)
    log_info(f"Current price of {symbol}: {current_price}")

    lower_price = round(current_price * lower_pct, 2)
    upper_price = round(current_price * upper_pct, 2)
    price_gap = (upper_price - lower_price) / max(steps - 1, 1)

    log_info(f"Placing {steps} {side.upper()} grid orders from {lower_price} to {upper_price}")

    for i in range(steps):
        price = round(lower_price + i * price_gap, 2)
        place_limit_order(symbol, side, quantity, price)
        time.sleep(0.5)  # small delay to avoid rate limits

# CLI
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python grid_order.py SYMBOL BUY/SELL QUANTITY [STEPS LOWER_PCT UPPER_PCT]")
        sys.exit(1)

    symbol = sys.argv[1]
    side = sys.argv[2].upper()
    quantity = float(sys.argv[3])
    steps = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    lower_pct = float(sys.argv[5]) if len(sys.argv) > 5 else 0.98
    upper_pct = float(sys.argv[6]) if len(sys.argv) > 6 else 1.02

    place_grid_orders(symbol, side, quantity, steps, lower_pct, upper_pct)
