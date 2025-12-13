import time
import logging
import hmac
import hashlib
import requests
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
import sys

# Load Testnet API Keys
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
BASE_URL = "https://testnet.binance.vision"

# Logging
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, '..', 'bot.log')

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

# Helper Functions
def sign(params):
    query = urlencode(params)
    signature = hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    return f"{query}&signature={signature}"

def validate_symbol(symbol):
    if symbol.isalnum() and symbol.upper().endswith("USDT"):
        return True
    log_error(f"Invalid symbol format: {symbol}")
    return False

def validate_positive_number(name, value):
    try:
        val = float(value)
        if val <= 0:
            raise ValueError
        return val
    except:
        log_error(f"{name} must be a positive number: {value}")
        return None

# Binance Market Order
def place_market_order(symbol, side, quantity):
    side = side.upper()
    params = {
        "symbol": symbol.upper(),
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": int(time.time() * 1000),
        "recvWindow": 5000
    }
    signed = sign(params)
    url = f"{BASE_URL}/api/v3/order?{signed}"
    headers = {"X-MBX-APIKEY": API_KEY}
    response = requests.post(url, headers=headers)
    log_info(f"Market order response (chunk): {response.status_code}")
    try:
        log_info(response.json())
    except Exception as e:
        log_error(f"Failed to parse response JSON: {e}")

# TWAP Order
def twap_order(symbol, side, total_quantity, chunks, interval):
    qty_per_chunk = round(total_quantity / chunks, 6)  # round to 6 decimals for BTC
    log_info(f"TWAP order: {total_quantity} {symbol.upper()} as {chunks} chunks every {interval}s ({qty_per_chunk} per chunk)")

    for i in range(chunks):
        log_info(f"Placing chunk {i+1}/{chunks}")
        place_market_order(symbol, side, qty_per_chunk)
        if i < chunks - 1:
            time.sleep(interval)

# CLI
if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python twap.py SYMBOL SIDE TOTAL_QTY CHUNKS INTERVAL")
        sys.exit(1)

    symbol = sys.argv[1]
    side = sys.argv[2].upper()
    total_quantity = validate_positive_number("Total quantity", sys.argv[3])
    chunks = validate_positive_number("Chunks", sys.argv[4])
    interval = validate_positive_number("Interval", sys.argv[5])

    if not validate_symbol(symbol) or side not in ["BUY", "SELL"]:
        log_error("Invalid symbol or side (must be BUY or SELL)")
        sys.exit(1)

    if None in [total_quantity, chunks, interval]:
        sys.exit(1)

    twap_order(symbol, side, total_quantity, int(chunks), interval)
