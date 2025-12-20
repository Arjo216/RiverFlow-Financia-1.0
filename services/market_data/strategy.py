import os
import time
import requests
import psycopg2
import pandas as pd
import numpy as np
from alpaca_trade_api.rest import REST
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
DB_HOST = "timescaledb"
DB_NAME = "sentient_alpha"
DB_USER = "admin"
DB_PASS = os.getenv("DB_PASSWORD", "secretpassword")

ALPACA_KEY = os.getenv("ALPACA_KEY")
ALPACA_SECRET = os.getenv("ALPACA_SECRET")
BASE_URL = "https://paper-api.alpaca.markets"
CRYPTOPANIC_KEY = os.getenv("CRYPTOPANIC_KEY") # New Key

api = REST(ALPACA_KEY, ALPACA_SECRET, BASE_URL, api_version='v2')

# --- RISK & STRATEGY PARAMS ---
MAX_POSITION_SIZE = 0.05
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
STOP_LOSS_PCT = -0.02
TAKE_PROFIT_PCT = 0.04

class NewsEngine:
    """
    📰 THE VISION: Fetches live news from CryptoPanic.
    Returns a 'Sentiment Score' (Simple version: Negative news = Caution)
    """
    def __init__(self):
        self.api_url = "https://cryptopanic.com/api/v1/posts/"
        self.api_key = CRYPTOPANIC_KEY
    
    def get_latest_sentiment(self):
        if not self.api_key:
            print("⚠️ NEWS WARNING: No CryptoPanic Key found.")
            return "NEUTRAL"

        try:
            # Fetch 'Hot' news for Bitcoin
            response = requests.get(
                self.api_url, 
                params={
                    "auth_token": self.api_key, 
                    "currencies": "BTC", 
                    "filter": "hot",   # Only important news
                    "public": "true"
                },
                timeout=5
            )
            data = response.json()
            
            if "results" in data and len(data["results"]) > 0:
                top_news = data["results"][0]
                title = top_news["title"]
                
                # Basic Keyword Sentiment (We will upgrade this to LLM later)
                # If news mentions 'ban', 'crash', 'SEC', 'lawsuit' -> DANGER
                bearish_keywords = ['ban', 'crash', 'plunge', 'lawsuit', 'sec', 'hacked']
                if any(word in title.lower() for word in bearish_keywords):
                    print(f"📰 BREAKING NEWS (BEARISH): {title[:60]}...")
                    return "BEARISH"
                
                print(f"📰 NEWS: {title[:60]}...")
                return "NEUTRAL"
                
            return "NEUTRAL"

        except Exception as e:
            print(f"❌ NEWS ERROR: {e}")
            return "NEUTRAL"

# Initialize Engines
news_bot = NewsEngine()

def get_market_data(cursor, symbol="BTC/USD", limit=100):
    query = "SELECT time, price FROM market_candles WHERE symbol = %s ORDER BY time DESC LIMIT %s;"
    cursor.execute(query, (symbol, limit))
    data = cursor.fetchall()
    if not data: return None
    df = pd.DataFrame(data, columns=['time', 'close'])
    df['close'] = df['close'].astype(float)
    df = df.sort_values('time')
    return df

def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.ewm(com=period-1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period-1, min_periods=period).mean()
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))
    return df.iloc[-1]['rsi']

def manage_risk():
    try:
        positions = api.list_positions()
        for p in positions:
            symbol = p.symbol
            qty = p.qty
            entry = float(p.avg_entry_price)
            curr = float(p.current_price)
            pl_pct = (curr - entry) / entry
            
            print(f"   🛡️ AUDIT {symbol}: P/L {pl_pct:.2%}")

            if pl_pct <= STOP_LOSS_PCT:
                print(f"🛑 STOP LOSS: Selling {symbol} ({pl_pct:.2%})")
                api.submit_order(symbol=symbol, qty=qty, side='sell', type='market', time_in_force='gtc')
            elif pl_pct >= TAKE_PROFIT_PCT:
                print(f"💰 TAKE PROFIT: Selling {symbol} ({pl_pct:.2%})")
                api.submit_order(symbol=symbol, qty=qty, side='sell', type='market', time_in_force='gtc')
    except Exception as e:
        print(f"❌ RISK ERROR: {e}")

def execute_strategy():
    print("🚀 RIVERFLOW 2.0: VISION UPGRADE (NEWS + RSI + SHIELD)...")
    
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
    except Exception as e:
        print(f"❌ DB Connection Failed: {e}")
        return

    while True:
        try:
            manage_risk()
            
            # 1. CHECK NEWS SENTIMENT
            sentiment = news_bot.get_latest_sentiment()

            # 2. GET DATA
            df = get_market_data(cur, "BTC/USD")
            if df is None or len(df) < 20:
                print("⏳ Collecting Data...")
                time.sleep(5)
                continue

            current_price = df.iloc[-1]['close']
            current_rsi = calculate_rsi(df, RSI_PERIOD)

            if np.isnan(current_rsi):
                time.sleep(5)
                continue

            print(f"📊 SCAN | BTC: ${current_price:,.2f} | RSI: {current_rsi:.2f} | News: {sentiment}")

            # 3. EXECUTE STRATEGY
            # BUY IF: RSI < 30 AND News is NOT Bearish
            if current_rsi < RSI_OVERSOLD:
                if sentiment == "BEARISH":
                    print("🛑 SIGNAL REJECTED: RSI is good, but News is Bad!")
                else:
                    print(f"💎 GREEN LIGHT: Oversold + News Neutral/Good")
                    account = api.get_account()
                    cash = float(account.cash)
                    
                    positions = [p.symbol for p in api.list_positions()]
                    if "BTC/USD" not in positions and cash > 1000:
                        qty = (cash * MAX_POSITION_SIZE) / current_price
                        print(f"⚡ BUYING {qty:.4f} BTC")
                        api.submit_order(symbol="BTC/USD", qty=qty, side="buy", type="market", time_in_force="gtc")
                        time.sleep(10)

            time.sleep(10)

        except Exception as e:
            print(f"❌ SYSTEM ERROR: {e}")
            time.sleep(5)

if __name__ == "__main__":
    time.sleep(5)
    execute_strategy()