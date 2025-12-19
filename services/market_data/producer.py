import os
import json
import asyncio
from alpaca.data.live import CryptoDataStream
from confluent_kafka import Producer

# 1. Config
ALPACA_KEY = os.getenv('ALPACA_KEY')
ALPACA_SECRET = os.getenv('ALPACA_SECRET')
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'redpanda:9092')

# 2. Initialize Kafka Producer
print(f"🔌 Connecting to Kafka at: {KAFKA_BROKER}")
producer = Producer({'bootstrap.servers': KAFKA_BROKER})

def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed: {err}")

# This MUST remain async because Alpaca calls it internally
async def handle_quote(data):
    msg = {
        "symbol": data.symbol,
        "price": data.bid_price,
        "time": str(data.timestamp),
        "type": "quote"
    }
    
    # Send to Kafka
    producer.produce(
        'market_trades', 
        key=msg['symbol'], 
        value=json.dumps(msg), 
        callback=delivery_report
    )
    producer.poll(0)

# CHANGE 1: Remove 'async' keyword
def main():
    print("🚀 Starting Production Crypto Stream...")
    
    wss_client = CryptoDataStream(ALPACA_KEY, ALPACA_SECRET)
    
    print("✅ Subscribing to BTC/USD Quotes...")
    wss_client.subscribe_quotes(handle_quote, "BTC/USD")

    # CHANGE 2: Remove 'await'. This is now a blocking call.
    wss_client.run()

if __name__ == "__main__":
    # CHANGE 3: Remove 'asyncio.run()'. Just call main().
    main()