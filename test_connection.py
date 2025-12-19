import os
from dotenv import load_dotenv
from alpaca.data.live import CryptoDataStream # Using Crypto so it works on weekends
from alpaca.data.enums import DataFeed

load_dotenv()
API_KEY = os.getenv('ALPACA_KEY')
SECRET = os.getenv('ALPACA_SECRET')

async def print_trade(t):
    print(f"🌊 RiverFlow Received: {t.symbol} @ ${t.price}")

async def main():
    print("🔗 Connecting to Market Data Stream...")
    # We use Crypto (BTC/USD) because it trades 24/7. 
    # If we used Stocks (AAPL), this script would fail on weekends/nights.
    stream = CryptoDataStream(API_KEY, SECRET, feed=DataFeed.US)
    stream.subscribe_trades(print_trade, "BTC/USD")
    await stream.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())