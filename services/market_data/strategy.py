import os
import time
import psycopg2
from alpaca_trade_api.rest import REST, TimeFrame
from dotenv import load_dotenv

# Load Environment Variables (for local testing)
load_dotenv()

# --- CONFIGURATION ---
DB_HOST = "timescaledb"
DB_NAME = "sentient_alpha"
DB_USER = "admin"
DB_PASS = os.getenv("DB_PASSWORD", "secretpassword") # Fallback for safety

ALPACA_KEY = os.getenv("ALPACA_KEY")
ALPACA_SECRET = os.getenv("ALPACA_SECRET")
BASE_URL = "https://paper-api.alpaca.markets"

# Connect to Alpaca
api = REST(ALPACA_KEY, ALPACA_SECRET, BASE_URL, api_version='v2')

def get_latest_price(cursor, symbol="BTC/USD"):
    """Fetches the most recent price from TimescaleDB"""
    query = "SELECT price FROM market_candles WHERE symbol = %s ORDER BY time DESC LIMIT 1;"
    cursor.execute(query, (symbol,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_ai_memory_count(cursor):
    """Checks if the AI has ingested any knowledge (Simple heuristic)"""
    query = "SELECT COUNT(*) FROM langchain_pg_embedding;"
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result else 0

def place_trade(symbol, qty, side):
    """Executes a Market Order on Alpaca"""
    try:
        print(f"⚡ EXECUTING {side.upper()} ORDER for {qty} {symbol}...")
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc'
        )
        print(f"✅ ORDER PLACED: ID {order.id}")
        return True
    except Exception as e:
        print(f"❌ ORDER FAILED: {e}")
        return False

def execute_strategy():
    print("🚀 QUANT ENGINE: LIVE EXECUTION MODE ENABLED")
    
    # Connect to DB
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        print("✅ Connected to Strategy Database")
    except Exception as e:
        print(f"❌ DB Connection Failed: {e}")
        return

    # Tracking to prevent spamming trades
    has_bought = False 

    while True:
        try:
            # 1. Get Market State
            price = get_latest_price(cur, "BTC/USD")
            memories = get_ai_memory_count(cur)

            if price is None:
                print("⏳ Waiting for price data...")
                time.sleep(5)
                continue

            print(f"📊 CHECK | BTC: ${price:,.2f} | AI Memories: {memories}")

            # 2. THE ALPHA LOGIC
            # Condition: Price > $50k AND AI has data AND we haven't bought yet
            if price > 50000 and memories > 0 and not has_bought:
                print("🟢 SIGNAL TRIGGERED: BUY AGGRESSIVE")
                
                # EXECUTE THE TRADE (0.01 BTC)
                success = place_trade("BTC/USD", 0.01, "buy")
                
                if success:
                    has_bought = True # Stop buying so we don't drain the account
            
            elif has_bought:
                print("💤 HOLDING POSITION (Trade already active)")
            else:
                print("💤 WAITING for signal alignment...")

            time.sleep(10)

        except Exception as e:
            print(f"❌ ERROR: {e}")
            time.sleep(5)

if __name__ == "__main__":
    time.sleep(5)
    execute_strategy()