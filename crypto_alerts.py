import requests
import asyncio
from telegram import Bot

# Apna Telegram Bot Token aur Group ID yaha daalo
TELEGRAM_TOKEN = "8009747355:AAGYatUtTVNTM9F62Av6BF6snUV_sm26EnQ"
TELEGRAM_GROUP_ID = "1002817409395"

bot = Bot(token=TELEGRAM_TOKEN)

# CoinGecko IDs
COINS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "binancecoin": "BNB",
    "cardano": "ADA",
    "ripple": "XRP"
}

async def send_alerts():
    message = ""
    for coin, symbol in COINS.items():
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
            response = requests.get(url, timeout=10)
            data = response.json()
            price = data[coin]["usd"]

            message += (
                f"{symbol} Price Alert ✅\n"
                f"Price: ${price}\n"
                "Trade Smart! 🚀\n"
                "----------------------------------------\n"
            )
        except Exception as e:
            message += f"{symbol} ❌ Error fetching price: {e}\n"

    # Telegram group me bhejna
    await bot.send_message(chat_id=TELEGRAM_GROUP_ID, text=message)

if __name__ == "__main__":
    asyncio.run(send_alerts())
