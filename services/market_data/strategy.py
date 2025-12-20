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

# --- BROKER, BRAIN & NOTIFIER ---
api = REST(os.getenv("ALPACA_KEY"), os.getenv("ALPACA_SECRET"), "https://paper-api.alpaca.markets", api_version='v2')
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- TELEGRAM SYSTEM ---
def send_telegram(message):
    """Sends professional Markdown alerts to your phone"""
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id: return
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"⚠️ Telegram Alert Error: {e}")

# --- INSTITUTIONAL PARAMETERS ---
SYMBOL = "BTC/USD"
MAX_POSITION_SIZE = 0.10  # Max 10% of total capital per trade
ATR_MULTIPLIER = 2.0      # Volatility-based Stop Loss multiplier
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

class SentinelAI:
    """The High-IQ Executive: Groq-powered news reasoning"""
    def analyze(self, headline):
        try:
            prompt = (
                f"SYSTEM: Senior Quant Strategist.\n"
                f"NEWS: '{headline}'\n"
                f"TASK: Assess BTC/USD impact. Think step-by-step. "
                f"Score -1.0 (Panic) to 1.0 (Bullish). Return ONLY raw float."
            )
            chat = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return float(chat.choices[0].message.content.strip())
        except Exception as e:
            print(f"⚠️ AI error: {e}")
            return 0.0

class QuantEngine:
    """Mathematical Core: Technical Indicator Suite"""
    @staticmethod
    def calculate_indicators(df):
        # RSI calculation
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)
        avg_gain = gain.ewm(com=RSI_PERIOD-1, min_periods=RSI_PERIOD).mean()
        avg_loss = loss.ewm(com=RSI_PERIOD-1, min_periods=RSI_PERIOD).mean()
        df['rsi'] = 100 - (100 / (1 + (avg_gain / avg_loss)))

        # MACD calculation
        df['ema_fast'] = df['close'].ewm(span=MACD_FAST, adjust=False).mean()
        df['ema_slow'] = df['close'].ewm(span=MACD_SLOW, adjust=False).mean()
        df['macd'] = df['ema_fast'] - df['ema_slow']
        df['signal'] = df['macd'].ewm(span=MACD_SIGNAL, adjust=False).mean()

        # ATR proxy (Volatility tracking)
        df['tr'] = df['close'].diff().abs()
        df['atr'] = df['tr'].rolling(window=14).mean()
        
        return df.iloc[-1]

def get_live_data():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(f"SELECT price FROM market_candles WHERE symbol='{SYMBOL}' ORDER BY time DESC LIMIT 100;")
    rows = cur.fetchall()
    cur.close(); conn.close()
    if not rows: return None
    return pd.DataFrame([float(r[0]) for r in rows][::-1], columns=['close'])

def get_news():
    """Fetches hot crypto news with SSL and Rate-Limit protection"""
    token = os.getenv('CRYPTOPANIC_KEY')
    # Added 'public=true' and 'kind=news' for better compatibility
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={token}&currencies=BTC&filter=hot&public=true"
    
    try:
        # verify=False bypasses SSL certificate issues inside Docker
        # Added a 10-second timeout to prevent the bot from hanging
        res = requests.get(url, timeout=10, verify=False) 
        
        if res.status_code == 200:
            data = res.json()
            if data.get('results'):
                return data['results'][0]['title']
            return "No news currently trending."
        elif res.status_code == 429:
            return "Rate Limited: Waiting for API cooldown..."
        else:
            return f"API Status Error: {res.status_code}"
            
    except Exception as e:
        # This will now print the actual error to your terminal for debugging
        print(f"🔄 News feed retry... (Technical Error: {e})")
        return "News feed temporarily unavailable...""

def run_apex():
    print("💠 RIVERFLOW APEX 4.0: LIVE FIRE MODE")
    send_telegram("🚀 *RiverFlow Apex 4.0 Online*\nGuard Mode Active. Volatility Shield: Engaged.")
    
    sentinel = SentinelAI()
    while True:
        try:
            # 1. INTELLIGENCE GATHERING
            df = get_live_data()
            if df is None or len(df) < 30:
                print("⏳ Building history..."); time.sleep(10); continue
            
            latest = QuantEngine.calculate_indicators(df)
            headline = get_news()
            ai_score = sentinel.analyze(headline)

            # 2. DECISION MATRIX
            rsi, macd, signal, atr, price = latest['rsi'], latest['macd'], latest['signal'], latest['atr'], latest['close']

            print(f"📊 [SCAN] BTC: ${price:,.2f}")
            print(f"📈 [MATH] RSI:{rsi:.1f} | MACD:{macd:.2f} [AI] SCORE:{ai_score:+.2f}")
            print(f"📰 [NEWS] {headline[:60]}...")

            # 3. TRADING EXECUTION (The "Triple Agreement" rule)
            if rsi < 40 and macd > signal and ai_score > 0.3:
                account = api.get_account()
                if float(account.cash) > 500:
                    qty = (float(account.cash) * MAX_POSITION_SIZE) / price
                    api.submit_order(symbol="BTC/USD", qty=qty, side='buy', type='market', time_in_force='gtc')
                    
                    alert = (f"🟢 *BUY EXECUTED*\n💰 Price: ${price:,.2f}\n📈 RSI: {rsi:.1f}\n🧠 AI Sentiment: {ai_score:+.2f}\n"
                             f"📰 {headline[:50]}...")
                    send_telegram(alert)
                    time.sleep(60) # Post-trade cooldown

            # 4. VOLATILITY SHIELD (Risk Defense)
            for p in api.list_positions():
                if p.symbol == "BTCUSD":
                    entry = float(p.avg_entry_price)
                    stop_price = entry - (atr * ATR_MULTIPLIER)
                    if price <= stop_price:
                        api.submit_order(symbol=p.symbol, qty=p.qty, side='sell', type='market', time_in_force='gtc')
                        send_telegram(f"🛑 *STOP LOSS TRIGGERED*\nBTC position closed at ${price:,.2f} to protect capital.")

            time.sleep(15)
        except Exception as e:
            print(f"⚠️ System Recovery: {e}"); time.sleep(5)

if __name__ == "__main__":
    run_apex()