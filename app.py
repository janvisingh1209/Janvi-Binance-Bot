from flask import Flask, jsonify
import os
from binance.client import Client

app = Flask(__name__)

# Load API keys from Render environment variables
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Initialize Binance client (testnet=True for safety)
client = Client(API_KEY, API_SECRET, testnet=True)


@app.route("/")
def home():
    return jsonify({
        "project": "Janvi Binance Bot",
        "status": "running",
        "mode": "testnet"
    })


@app.route("/status")
def status():
    return jsonify({"status": "Bot is live"})


@app.route("/price/<symbol>")
def get_price(symbol):
    try:
        price = client.get_symbol_ticker(symbol=symbol.upper())
        return jsonify({
            "symbol": symbol.upper(),
            "price": price["price"]
        })
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/account")
def account_info():
    try:
        info = client.get_account()
        return jsonify({"account_status": "connected"})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/simulate")
def simulate():
    return jsonify({
        "strategy": "Market Order",
        "mode": "simulation",
        "message": "Simulation executed successfully"
    })


if __name__ == "__main__":
    app.run()
