Binance Trading Bot

## Objective
CLI-based trading bot for Binance USDT-M Futures. Supports Market, Limit, OCO, TWAP, and Grid orders with logging and testnet integration.  

---

## Demo (Recruiter Testing)

The bot is deployed on Render in **demo mode**. No real trades are executed.  

**Render URL:**  
[https://janvi-binance-bot.onrender.com](https://janvi-binance-bot.onrender.com)

**Endpoints to try:**

| Endpoint | Description |
|----------|-------------|
| `/` | Project info & status |
| `/status` | Check if bot is live |
| `/price/<symbol>` | Simulated cryptocurrency price (e.g., `/price/BTC`) |
| `/account` | Demo account balances |
| `/simulate` | Simulated trade execution |

**Example usage (browser or terminal):**
```bash
curl https://janvi-binance-bot.onrender.com/status
curl https://janvi-binance-bot.onrender.com/price/BTC
curl https://janvi-binance-bot.onrender.com/account
curl https://janvi-binance-bot.onrender.com/simulate
All endpoints return simulated/demo data. Local testing with .env API keys can still connect to Binance Testnet.

Local Setup (Optional)
Install dependencies:

pip install requests python-dotenv
Create .env with Testnet API keys:

BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
