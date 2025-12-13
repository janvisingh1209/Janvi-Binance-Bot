import os
import sys
import time
import hmac
import hashlib
import requests
import logging
from urllib.parse import urlencode
from dotenv import load_dotenv

#  Load API Keys 
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
BASE_URL = "https://testnet.binance.vision"

#  Logging Setup 
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

#  Validation 
def validate_symbol(symbol):
    if symbol.isalnum() and symbol.upper().endswith("USDT"):
        return True
    log_error(f"Invalid symbol format: {symbol}")
    return False

def validate_quantity(quantity):
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError
        return True
    except:
        log_error(f"Invalid quantity: {quantity}")
        return False

def validate_price(price):
    try:
        p = float(price)
        if p <= 0:
            raise ValueError
        return True
    except:
        log_error(f"Invalid price: {price}")
        return False

# Binance API Helpers
def sign(params):
    """Sign the parameters using HMAC SHA256"""
    query = urlencode(params)
    signature = hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    return f"{query}&signature={signature}"

# Place Limit Order 
def place_limit_order(symbol, side, quantity, price):
    side = side.upper()
    symbol = symbol.upper()

    log_info(f"Placing LIMIT order: {side} {quantity} {symbol} at {price} USDT")

    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "quantity": float(quantity),
        "price": float(price),
        "timeInForce": "GTC",
        "timestamp": int(time.time() * 1000),
        "recvWindow": 5000
    }

    signed = sign(params)
    url = f"{BASE_URL}/api/v3/order?{signed}"
    headers = {"X-MBX-APIKEY": API_KEY}

    try:
        response = requests.post(url, headers=headers)
        log_info(f"Response Status: {response.status_code}")
        log_info(response.json())
    except Exception as e:
        log_error(f"Error placing order: {e}")

#  CLI Interface
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python limit_order.py SYMBOL BUY/SELL QUANTITY PRICE")
        sys.exit(1)

    symbol, side, quantity, price = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

    # Validate inputs
    if not validate_symbol(symbol):
        sys.exit(1)
    if not validate_quantity(quantity):
        sys.exit(1)
    if not validate_price(price):
        sys.exit(1)

    # Place order
    place_limit_order(symbol, side, quantity, price)
