import os
import sys
import logging
from dotenv import load_dotenv

# Load .env
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Logging setup
logging.basicConfig(
    filename='../bot.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def log_info(msg):
    print(msg)
    logging.info(msg)

def log_error(msg):
    print(f"ERROR: {msg}")
    logging.error(msg)

# --- Validation ---
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

# SIMULATED MARKET ORDER 
def place_market_order(symbol, side, quantity):
    order = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": "MARKET",
        "quantity": float(quantity),
        "status": "SIMULATED"
    }
    log_info(f"[SIMULATION] Market order executed: {order}")
    return order

#  CLI 
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python src/market_order.py SYMBOL BUY/SELL QUANTITY")
        sys.exit(1)

    symbol, side, quantity = sys.argv[1], sys.argv[2], sys.argv[3]

    if validate_symbol(symbol) and validate_quantity(quantity):
        place_market_order(symbol, side, quantity)
