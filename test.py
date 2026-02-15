from dotenv import load_dotenv
import os
from binance.client import Client

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")



# Initialize Binance client with testnet=True
client = Client(API_KEY, API_SECRET, testnet=True)



try:
    # Fetch account information
    info = client.get_account()
    
    # Print the full JSON response
    print(info)

    # Optional: print balances only for clarity
    print("\nBalances:")
    for asset in info['balances']:
        print(f"{asset['asset']}: Free={asset['free']}, Locked={asset['locked']}")

except Exception as e:
    print("Error:", e)
