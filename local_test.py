import os
from dotenv import load_dotenv
from alpaca.data.live import CryptoDataStream

load_dotenv()

API_KEY = os.getenv('ALPACA_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET')

async def quote_handler(data):
    # This will print FAST (every time the price changes by 1 cent)
    print(f"🌊 Quote: {data.symbol} | Bid: {data.bid_price} | Ask: {data.ask_price}")

def main():
    print("🚀 Connecting to Crypto Stream...")
    crypto_client = CryptoDataStream(API_KEY, SECRET_KEY)
    
    # Subscribe to Quotes (updates wildly fast) instead of Trades
    print("✅ Subscribing to BTC/USD Quotes...")
    crypto_client.subscribe_quotes(quote_handler, "BTC/USD")

    crypto_client.run()

if __name__ == "__main__":
    main()