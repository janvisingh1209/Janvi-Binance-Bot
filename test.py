from binance.client import Client

# Replace with your Spot Testnet keys
API_KEY = "5Vy9d7FIUIaYYKo7d1TOYjsUeJiLHVo5oDD12r7hz3Np862WSJBQ5qAivHcbjVSu"
API_SECRET = "4UM4uZBkiglXq5QbiuD6ZRzzxowmgirpJBdYXr1sVEZVRIyBAiB9fUP4YAFK2NEc"

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
