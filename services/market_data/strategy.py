import os
import time
import psycopg2
from datetime import datetime

# Configuration
DB_HOST = "timescaledb"
DB_NAME = "sentient_alpha"
DB_USER = "admin"
DB_PASS = "secretpassword"

def get_latest_price(cursor, symbol="BTC/USD"):
    """Fetches the most recent price from TimescaleDB"""
    query = """
    SELECT price FROM market_candles 
    WHERE symbol = %s 
    ORDER BY time DESC LIMIT 1;
    """
    cursor.execute(query, (symbol,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_ai_sentiment(cursor):
    """
    Checks the Vector DB for 'Risk' signals.
    In a real fund, we would classify the text. 
    Here, we measure how 'close' our documents are to the concept of 'Risk'.
    """
    # 1. We check if there are any documents close to our embeddings 
    # (This is a simplified check for the existence of memory)
    query = "SELECT COUNT(*) FROM langchain_pg_embedding;"
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result else 0

def execute_strategy():
    print("🚀 Quant Strategy Engine Starting...")
    
    # Connect to DB
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cur = conn.cursor()
        print("✅ Connected to Strategy Database")
    except Exception as e:
        print(f"❌ DB Connection Failed: {e}")
        return

    while True:
        try:
            # 1. Get Data
            price = get_latest_price(cur, "BTC/USD")
            memory_count = get_ai_sentiment(cur)

            if price is None:
                print("⏳ Waiting for market data...")
                time.sleep(5)
                continue

            # 2. The Alpha Logic (The Strategy)
            print(f"📊 Market Check | Price: ${price:,.2f} | AI Memories: {memory_count}")

            # TRADING RULE: 
            # If Price is above $50k AND the AI has read documents (memories > 0)
            if price > 50000 and memory_count > 0:
                print("✅ SIGNAL: BUY BTC (Market Strong + AI Active)")
                # In the future, we add: alpaca.submit_order(...)
            else:
                print("💤 SIGNAL: HOLD (Waiting for alignment)")

            time.sleep(10) # Run every 10 seconds

        except Exception as e:
            print(f"❌ Error: {e}")
            # Try to reconnect
            try:
                conn = psycopg2.connect(
                    host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
                )
                cur = conn.cursor()
            except:
                pass
            time.sleep(5)

if __name__ == "__main__":
    time.sleep(5) # Allow DB to settle
    execute_strategy()