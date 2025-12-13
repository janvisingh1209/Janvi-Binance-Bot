import os
import sys
import time
import hmac
import hashlib
import logging
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
BASE_URL = "https://testnet.binance.vision"

# Logging setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, '..', '..', 'bot.log')
logger = logging.getLogger("binance_bot")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_PATH)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(file_handler)

def log_info(msg):
    print(msg)
    logger.info(msg)

def log_error(msg):
    print(f"ERROR: {msg}")
    logger.error(msg)

# Validation
def validate_symbol(symbol):
    if symbol.isalnum() and symbol.upper().endswith("USDT"):
        return True
    log_error(f"Invalid symbol: {symbol}")
    return False

def validate_side(side):
    if side.upper() in ["BUY", "SELL"]:
        return True
    log_error(f"Invalid side: {side}")
    return False

def validate_quantity(qty):
    try:
        q = float(qty)
        if q <= 0:
            raise ValueError
        return True
    except:
        log_error(f"Invalid quantity: {qty}")
        return False

def validate_offset(offset, name):
    try:
        o = float(offset)
        if o <= 0:
            raise ValueError
        return True
    except:
        log_error(f"Invalid {name} offset: {offset}")
        return False

# Binance API 
def sign(params):
    query = urlencode(params)
    signature = hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    return f"{query}&signature={signature}"

def get_current_price(symbol):
    url = f"{BASE_URL}/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    if response.status_code != 200:
        log_error(f"Failed to fetch price: {response.json()}")
        return None
    return float(response.json()['price'])

#  OCO Order 
def place_oco_order(symbol, side, qty, tp_offset=None, stop_offset=None):
    side = side.upper()
    current_price = get_current_price(symbol)
    if current_price is None:
        return

    # Default offsets
    tp_offset = float(tp_offset) if tp_offset else current_price * 0.01
    stop_offset = float(stop_offset) if stop_offset else current_price * 0.01

    if side == "BUY":
        tp_price = round(current_price - tp_offset, 2)
        stop_price = round(current_price + stop_offset, 2)
        if tp_price >= current_price or stop_price <= current_price:
            log_error("For BUY OCO: TP must be below current price, Stop above current price.")
            return
        params = {
            "symbol": symbol,
            "side": side,
            "quantity": qty,
            "aboveType": "STOP_LOSS_LIMIT",
            "abovePrice": str(stop_price),
            "aboveStopPrice": str(stop_price),
            "aboveTimeInForce": "GTC",
            "belowType": "LIMIT_MAKER",
            "belowPrice": str(tp_price),
            "timestamp": int(time.time() * 1000),
            "recvWindow": 5000
        }
    else:  # SELL
        tp_price = round(current_price + tp_offset, 2)
        stop_price = round(current_price - stop_offset, 2)
        if tp_price <= current_price or stop_price >= current_price:
            log_error("For SELL OCO: TP must be above current price, Stop below current price.")
            return
        params = {
            "symbol": symbol,
            "side": side,
            "quantity": qty,
            "aboveType": "LIMIT_MAKER",
            "abovePrice": str(tp_price),
            "belowType": "STOP_LOSS_LIMIT",
            "belowPrice": str(stop_price),
            "belowStopPrice": str(stop_price),
            "belowTimeInForce": "GTC",
            "timestamp": int(time.time() * 1000),
            "recvWindow": 5000
        }

    log_info(f"OCO order called for {symbol}, side={side}, qty={qty}, TP={tp_price}, Stop={stop_price}")
    signed = sign(params)
    url = f"{BASE_URL}/api/v3/orderList/oco?{signed}"
    headers = {"X-MBX-APIKEY": API_KEY}
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        log_info(f"OCO order placed successfully: {response.json()}")
    else:
        # If insufficient balance, simulate the order
        if response.status_code == 400 and response.json().get("code") == -2010:
            log_info("[SIMULATION] Account balance insufficient, simulating OCO order...")
            simulated_order = {
                "symbol": symbol,
                "side": side,
                "quantity": qty,
                "TP": tp_price,
                "Stop": stop_price,
                "status": "SIMULATED"
            }
            log_info(f"[SIMULATION] OCO order: {simulated_order}")
        else:
            log_error(f"Failed to place OCO order: {response.status_code} {response.json()}")

# CLI 
if __name__ == "__main__":
    if len(sys.argv) not in [4, 6]:
        print("Usage: python oco.py SYMBOL SIDE QUANTITY [TP_OFFSET STOP_OFFSET]")
        sys.exit(1)

    symbol = sys.argv[1]
    side = sys.argv[2]
    qty = sys.argv[3]
    tp_offset = sys.argv[4] if len(sys.argv) > 4 else None
    stop_offset = sys.argv[5] if len(sys.argv) > 5 else None

    if not (validate_symbol(symbol) and validate_side(side) and validate_quantity(qty)):
        sys.exit(1)
    if tp_offset and not validate_offset(tp_offset, "TP"):
        sys.exit(1)
    if stop_offset and not validate_offset(stop_offset, "Stop"):
        sys.exit(1)

    place_oco_order(symbol, side, float(qty), tp_offset, stop_offset)
