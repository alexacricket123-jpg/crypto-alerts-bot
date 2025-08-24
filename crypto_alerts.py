import asyncio
from binance.client import Client
import requests
from telegram import Bot

# ----------------------------
# API Keys & Telegram Info
# ----------------------------
BINANCE_API_KEY = '2YffaDksp0dyclpc5H5EVc46fOWzR35XW73wYRZ1IjGX6FdmsqYcfTntlp03FK4T'
BINANCE_API_SECRET = 'YgL7XZNsJr3UqdEVhlTrWwsms5qYgWa3oOKxfQkrPZmgtED1LhM9gfF37rm63sbo'
TELEGRAM_BOT_TOKEN = '8009747355:AAGYatUtTVNTM9F62Av6BF6snUV_sm26EnQ'
TELEGRAM_GROUP_ID = -1002817409395  # private group ID

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
bot = Bot(token=TELEGRAM_BOT_TOKEN)

coins = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT"]
coingecko_ids = {
    "BTCUSDT": "bitcoin",
    "ETHUSDT": "ethereum",
    "BNBUSDT": "binancecoin",
    "ADAUSDT": "cardano",
    "XRPUSDT": "ripple"
}

# ----------------------------
# Function to send alerts
# ----------------------------
async def send_alerts():
    for coin in coins:
        bin_data = client.get_symbol_ticker(symbol=coin)
        bin_price = float(bin_data['price'])

        cg_response = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_ids[coin]}&vs_currencies=usd"
        ).json()
        cg_price = float(cg_response[coingecko_ids[coin]]['usd'])

        diff = abs(bin_price - cg_price)/bin_price * 100
        status = "✅ Verified" if diff < 1 else "⚠️ Check"

        message = f"{coin.replace('USDT','')} Price Alert {status}\n" \
                  f"Binance: ${bin_price:,.2f}\n" \
                  f"CoinGecko: ${cg_price:,.2f}\n" \
                  f"Trade Smart! 🚀"

        await bot.send_message(chat_id=TELEGRAM_GROUP_ID, text=message)
        print(message)
        print("-"*40)

# ----------------------------
# Run async
# ----------------------------
asyncio.run(send_alerts())
