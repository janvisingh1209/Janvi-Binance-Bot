from flask import Flask, jsonify
import os

# import your bot functions
from src.market_order import log_info  # example
# import other strategies as needed

app = Flask(__name__)

@app.route("/")
def home():
    return "Janvi Binance Bot API is running!"

@app.route("/status")
def status():
    return jsonify({"status": "Bot is live"})

# Example simulation endpoint
@app.route("/simulate")
def simulate():
    # call your strategy logic here
    return jsonify({
        "strategy": "Market Order",
        "mode": "simulation",
        "message": "Simulation executed successfully"
    })

if __name__ == "__main__":
    app.run()
