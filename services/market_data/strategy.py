import os
import time
import psycopg2
import pandas as pd
import numpy as np
import requests
from groq import Groq
from alpaca_trade_api.rest import REST
from dotenv import load_dotenv

load_dotenv()

# --- SYSTEM SETTINGS ---
DB_CONFIG = {
    "host": "timescaledb",
    "database": "sentient_alpha",
    "user": "admin",
    "password": os.getenv("DB_PASSWORD", "secretpassword")
}

# --- BROKER & BRAIN ---
api = REST(os.getenv("ALPACA_KEY"), os.getenv("ALPACA_SECRET"), "https://paper-api.alpaca.markets", api_version='v2')
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- INSTITUTIONAL PARAMETERS ---
SYMBOL = "BTC/USD"
MAX_POSITION_SIZE = 0.10  # Never more than 10% of total cash
ATR_MULTIPLIER = 2.0      # For Volatility-based Stop Loss
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

class SentinelAI:
    """The High-IQ Executive using Deep Reasoning"""
    def analyze(self, headline):
        try:
            prompt = (
                f"SYSTEM: Act as a Senior Quant at a Tier-1 Hedge Fund.\n"
                f"NEWS: '{headline}'\n"
                f"TASK: Analyze the impact on {SYMBOL}. Think step-by-step. "
                f"Provide a sentiment score from -1.0 (Black Swan/Panic) to 1.0 (Hyper-Bullish). "
                f"Return ONLY the raw float value."
            )
            chat = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return float(chat.choices[0].message.content.strip())
        except Exception as e:
            print(f"⚠️ AI reasoning error: {e}")
            return 0.0

class QuantEngine:
    """The Mathematical Core: Technical Indicator Suite"""
    @staticmethod
    def calculate_indicators(df):
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)
        avg_gain = gain.ewm(com=RSI_PERIOD-1, min_periods=RSI_PERIOD).mean()
        avg_loss = loss.ewm(com=RSI_PERIOD-1, min_periods=RSI_PERIOD).mean()
        rs = avg_gain / avg_loss
        df['rsi'] = 100 - (100 / (1 + rs))

        # MACD
        df['ema_fast'] = df['close'].ewm(span=MACD_FAST, adjust=False).mean()
        df['ema_slow'] = df['close'].ewm(span=MACD_SLOW, adjust=False).mean()
        df['macd'] = df['ema_fast'] - df['ema_slow']
        df['signal'] = df['macd'].ewm(span=MACD_SIGNAL, adjust=False).mean()

        # ATR (Volatility indicator)
        df['high_low'] = 0 # In this simple model, we use Close diff as proxy for ATR
        df['tr'] = df['close'].diff().abs()
        df['atr'] = df['tr'].rolling(window=14).mean()
        
        return df.iloc[-1]

def get_live_data():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(f"SELECT price FROM market_candles WHERE symbol='{SYMBOL}' ORDER BY time DESC LIMIT 100;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows: return None
    df = pd.DataFrame([float(r[0]) for r in rows][::-1], columns=['close'])
    return df

def get_news():
    try:
        url = f"https://cryptopanic.com/api/v1/posts/?auth_token={os.getenv('CRYPTOPANIC_KEY')}&currencies=BTC&filter=hot"
        res = requests.get(url, timeout=5).json()
        return res['results'][0]['title'] if res.get('results') else "No news"
    except: return "No news"

def run_apex():
    print("💠 RIVERFLOW APEX 3.0: SYSTEM ONLINE")
    sentinel = SentinelAI()
    
    while True:
        try:
            # 1. Gather Intelligence
            df = get_live_data()
            if df is None or len(df) < 30:
                print("⏳ Calibration in progress...")
                time.sleep(10); continue
            
            latest = QuantEngine.calculate_indicators(df)
            headline = get_news()
            ai_score = sentinel.analyze(headline)

            # 2. Decision Matrix
            rsi = latest['rsi']
            macd = latest['macd']
            signal = latest['signal']
            atr = latest['atr']
            price = latest['close']

            print(f"📊 [SCAN] BTC: ${price:,.2f}") # <--- ADD THIS LINE BACK
            print(f"📈 [MATH] RSI:{rsi:.1f} | MACD:{macd:.2f} [AI] SCORE:{ai_score:+.2f}")
            print(f"📰 [NEWS] {headline[:60]}...")

            # 3. TRADING LOGIC (The Apex Criteria)
            # Conditions for LONG: 
            # - RSI < 40 (Oversold/Dip)
            # - MACD is trending up (MACD > Signal)
            # - AI Sentiment is Bullish (> 0.3)
            
            if rsi < 40 and macd > signal and ai_score > 0.3:
                account = api.get_account()
                if float(account.cash) > 500:
                    qty = (float(account.cash) * MAX_POSITION_SIZE) / price
                    print(f"💎 CONFLUENCE DETECTED. EXECUTION: {qty:.4f} BTC")
                    api.submit_order(symbol="BTC/USD", qty=qty, side='buy', type='market', time_in_force='gtc')
                    time.sleep(60) # Cooldown

            # 4. VOLATILITY SHIELD (Dynamic Risk)
            for p in api.list_positions():
                if p.symbol == "BTCUSD":
                    entry = float(p.avg_entry_price)
                    # Stop loss is Entry - (ATR * Multiplier)
                    stop_price = entry - (atr * ATR_MULTIPLIER)
                    if price <= stop_price:
                        print(f"🛑 VOLATILITY STOP TRIGGERED. Closing position.")
                        api.submit_order(symbol=p.symbol, qty=p.qty, side='sell', type='market', time_in_force='gtc')

            time.sleep(10)
        except Exception as e:
            print(f"⚠️ Recovering system: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_apex()