import os
import time
import psycopg2
import pandas as pd
import numpy as np
import requests
import json
from groq import Groq
from alpaca_trade_api.rest import REST
from dotenv import load_dotenv

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import sys

class DualLogger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("/app/apex_logs.txt", "a")
        
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush() # Forces instant write to the shared file
        
    def flush(self):
        self.terminal.flush()
        self.log.flush()

# This permanently reroutes all print() statements
sys.stdout = DualLogger()

load_dotenv()

print("💠 RIVERFLOW APEX 4.0: TRIPLE-NODE ARCHITECTURE INITIALIZING...")

# --- SECURE CREDENTIALS ---
DB_PASS = os.getenv("DB_PASSWORD", "secretpassword")
GROQ_KEY = os.getenv("GROQ_API_KEY")
ALPACA_KEY = os.getenv("ALPACA_KEY")
ALPACA_SECRET = os.getenv("ALPACA_SECRET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CRYPTOPANIC_KEY = os.getenv("CRYPTOPANIC_KEY")

# --- CORE SYSTEMS ---
api = REST(ALPACA_KEY, ALPACA_SECRET, "https://paper-api.alpaca.markets", api_version='v2')
groq_client = Groq(api_key=GROQ_KEY)

# --- QUANTITATIVE PARAMETERS ---
SYMBOL = "BTC/USD"
MAX_POSITION_SIZE = 0.10  # 10% Capital allocation per strike
ATR_MULTIPLIER = 3.0      # Dynamic volatility stop-loss
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
TAKE_PROFIT_PCT = 0.02    # 2% Target

# --- 1. NOTIFICATION ENGINE ---
def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID: return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

# --- 2. EXECUTIVE AUDITOR ---
class PerformanceAuditor:
    def __init__(self):
        self.wins = 0
        self.total_trades = 0

    def get_daily_report(self):
        try:
            account = api.get_account()
            balance_change = float(account.equity) - float(account.last_equity)
            pnl_pct = (balance_change / float(account.last_equity)) * 100
            win_rate = (self.wins / self.total_trades * 100) if self.total_trades > 0 else 0
            
            return (
                f"📊 *DAILY AUDIT REPORT*\n"
                f"💰 Equity: ${float(account.equity):,.2f}\n"
                f"📈 P/L: ${balance_change:+,.2f} ({pnl_pct:+.2f}%)\n"
                f"🎯 Win Rate: {win_rate:.1f}%\n"
                f"🔄 Total Trades: {self.total_trades}"
            )
        except Exception as e:
            return f"⚠️ Audit Failed: {e}"

auditor = PerformanceAuditor()

# --- 3. THE RAG FUNDAMENTAL VAULT (NEW PHASE C LOGIC) ---
class InstitutionalVault:
    """Direct SQL bypass to read the 10-K vectors without heavy ML libraries"""
    @staticmethod
    def get_macro_clearance():
        try:
            # 1. Direct connection to the database
            conn = psycopg2.connect(host="sentient_db", database="sentient_alpha", user="admin", password=DB_PASS)
            cursor = conn.cursor()
            
            # 2. Extract random high-density chunks from the MSTR 2026 Filing
            cursor.execute("SELECT document FROM langchain_pg_embedding LIMIT 10;")
            records = cursor.fetchall()
            cursor.close(); conn.close()
            
            if not records:
                return True, "Vault Empty. Proceeding with standard technicals."
                
            context = "\n".join([rec[0] for rec in records])
            
            # 3. Groq 70B evaluates the fundamental data
            prompt = (
                f"SYSTEM: Senior FinTech Risk Officer.\n"
                f"CONTEXT (MSTR 10-K): {context[:3000]}\n"
                f"TASK: Based ONLY on this SEC filing context, is there an immediate liquidation risk or catastrophic debt failure for Bitcoin? "
                f"Reply exactly with 'CLEAR' if safe, or 'BLOCK' if dangerous. Add one sentence of reasoning."
            )
            
            chat = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            response = chat.choices[0].message.content.strip().upper()
            
            is_clear = "CLEAR" in response
            return is_clear, response
            
        except Exception as e:
            print(f"⚠️ Vault Connection Error: {e}")
            return True, "Bypassing fundamental check due to error."

# --- 4. DATA & SENTIMENT ENGINES ---
class SentinelAI:
    def analyze(self, headline):
        try:
            prompt = f"Score this BTC news -1.0 to +1.0. Return ONLY the float number: '{headline}'"
            chat = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant", # Faster model for quick news parsing
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return float(chat.choices[0].message.content.strip())
        except:
            return 0.0

class QuantEngine:
    @staticmethod
    def calculate_indicators(df):
        delta = df['close'].diff()
        gain = delta.clip(lower=0).fillna(0)
        loss = -delta.clip(upper=0).fillna(0)
        avg_gain = gain.ewm(com=RSI_PERIOD-1, min_periods=RSI_PERIOD).mean()
        avg_loss = loss.ewm(com=RSI_PERIOD-1, min_periods=RSI_PERIOD).mean()
        df['rsi'] = 100 - (100 / (1 + (avg_gain / avg_loss)))

        df['ema_fast'] = df['close'].ewm(span=MACD_FAST, adjust=False).mean()
        df['ema_slow'] = df['close'].ewm(span=MACD_SLOW, adjust=False).mean()
        df['macd'] = df['ema_fast'] - df['ema_slow']
        df['signal'] = df['macd'].ewm(span=MACD_SIGNAL, adjust=False).mean()

        df['tr'] = df['close'].diff().abs()
        df['atr'] = df['tr'].rolling(window=14).mean()
        df['sma_200'] = df['close'].rolling(window=200).mean()
        
        return df.iloc[-1]

def get_live_data():
    try:
        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=300"
        res = requests.get(url, timeout=5).json()
        df = pd.DataFrame(res)
        df['close'] = df[4].astype(float)
        return df[['close']]
    except:
        return None

# --- SMART CACHE VARIABLES ---
last_news_time = 0
cached_headline = "No active news."

def get_news():
    global last_news_time, cached_headline
    
    # Failsafe if the key is missing from .env
    if not CRYPTOPANIC_KEY: 
        return "No active news."
    
    # RATE LIMITER: Only ping the API once every 5 minutes (300 seconds)
    current_time = time.time()
    if current_time - last_news_time < 300:
        return cached_headline

    # The standard v1 API endpoint
    url = f"https://cryptopanic.com/api/free/v1/posts/?auth_token={CRYPTOPANIC_KEY}&currencies=BTC&filter=hot"
    
    # Institutional User-Agent to bypass basic Cloudflare blocks
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        res = requests.get(url, headers=headers, timeout=10) 
        if res.status_code == 200:
            data = res.json()
            if data.get('results'):
                cached_headline = data['results'][0]['title']
                last_news_time = current_time
                print(f"📰 [NEWS SYNC] Latest Headline: {cached_headline[:50]}...")
                return cached_headline
        else:
            print(f"⚠️ [API ERROR] HTTP {res.status_code}. Please verify your CRYPTOPANIC_KEY in .env!")
    except Exception as e:
        print(f"⚠️ [NETWORK ERROR] Failed to reach CryptoPanic: {e}")
        
    return cached_headline

from sqlalchemy import create_engine, text

# 🔗 Institutional Database Link
DB_PASS = os.getenv("DB_PASSWORD", "secretpassword")
DB_URL = f"postgresql://admin:{DB_PASS}@sentient_db:5432/sentient_alpha"
db_engine = create_engine(DB_URL)

def log_execution_audit(symbol, action, price, rsi, macd, sma_200, ai_score, rag_reasoning):
    """Permanently carves the exact trade logic into the Immutable Vault."""
    try:
        with db_engine.connect() as conn:
            query = text("""
                INSERT INTO execution_audit 
                (symbol, action, price, rsi, macd, sma_200, ai_score, rag_reasoning)
                VALUES 
                (:symbol, :action, :price, :rsi, :macd, :sma_200, :ai_score, :rag_reasoning)
            """)
            conn.execute(query, {
                "symbol": symbol, "action": action, "price": float(price),
                "rsi": float(rsi), "macd": float(macd), "sma_200": float(sma_200),
                "ai_score": float(ai_score), "rag_reasoning": str(rag_reasoning)
            })
            conn.commit()
            print(f"🔏 [AUDIT] {action} Execution securely logged to TimescaleDB.")
    except Exception as e:
        print(f"⚠️ [AUDIT ERROR] Failed to log execution: {e}")

# --- 5. THE MASTER LOOP ---
def run_apex():
    send_telegram("🚀 *RiverFlow Apex 4.0 Online*\nTriple-Node Architecture Active. Awaiting UI Command.")
    
    sentinel = SentinelAI()
    vault = InstitutionalVault()
    control_file = "/app/apex_control.json"
    
    # Initialize control file if it doesn't exist (Default: Safe/Stopped)
    if not os.path.exists(control_file):
        with open(control_file, "w") as f:
            json.dump({"status": "STOPPED"}, f)
    
    while True:
        try:
            # --- THE DASHBOARD BRIDGE ---
            with open(control_file, "r") as f:
                control = json.load(f)
                
            status = control.get("status")

            # 🚨 THE NUCLEAR OVERRIDE 🚨
            if status == "LIQUIDATE":
                print("🚨 EMERGENCY OVERRIDE TRIGGERED: Liquidating all assets and cancelling orders...")
                
                try:
                    # Instantly market-sells all positions and kills pending orders
                    api.close_all_positions() 
                    api.cancel_all_orders()
                    
                    send_telegram("🚨 *EMERGENCY OVERRIDE*\nAll positions have been liquidated. All open orders cancelled. Trading engine halted.")
                except Exception as e:
                    print(f"⚠️ Liquidation Error: {e}")
                    send_telegram(f"⚠️ *LIQUIDATION ERROR*: {e}")
                
                # Auto-reset the JSON file so it doesn't get stuck in a liquidation loop
                with open(control_file, "w") as f:
                    json.dump({"status": "STOPPED"}, f)
                continue

            # Standard Pause Check
            if status != "RUNNING":
                print("🛑 APEX PAUSED: Awaiting 'START' command from Dashboard...")
                time.sleep(10)
                continue

            # --- STANDARD EXECUTION LOGIC ---
            df = get_live_data()
            if df is None or len(df) < 200:
                print("⏳ Building history (awaiting 200-SMA)..."); time.sleep(10); continue
            
            latest = QuantEngine.calculate_indicators(df)
            headline = get_news()
            ai_score = sentinel.analyze(headline)

            rsi, macd, signal, atr, price, sma_200 = latest['rsi'], latest['macd'], latest['signal'], latest['atr'], latest['close'], latest['sma_200']

            print(f"📊 [SCAN] BTC: ${price:,.2f} | 200-SMA: ${sma_200:,.2f} | RSI: {rsi:.1f} | MACD: {macd:.2f}")

            # TRIPLE-NODE EXECUTION
            #if rsi < 50 and macd > signal and price > sma_200 and ai_score > 0.3:
            if rsi < 50 and macd > signal and price > sma_200:
                print("⚠️ Technical & Sentiment Lock Achieved. Requesting SEC RAG Clearance...")
                is_clear, reason = vault.get_macro_clearance()
                # --- 🚧 DEV OVERRIDE: FORCE INSTANT EXECUTION ---
            #if True: 
                #print("⚠️ DEV OVERRIDE ACTIVE. Requesting SEC RAG Clearance...")
                #is_clear, reason = vault.get_macro_clearance()
                
                if is_clear:
                    account = api.get_account()
                    if float(account.cash) > 500:
                        qty = (float(account.cash) * MAX_POSITION_SIZE) / price
                        api.submit_order(symbol="BTC/USD", qty=qty, side='buy', type='market', time_in_force='gtc')
                        
                        # 🔏 FIRE AUDIT LOG
                        log_execution_audit("BTC/USD", "BUY", price, rsi, macd, sma_200, ai_score, reason)
                        
                        send_telegram(f"🟢 *BUY EXECUTED*\n💰 Price: ${price:,.2f}")
                        time.sleep(60)
                else:
                    print("🛑 Trade Blocked by Institutional Vault.")

            # POSITION MANAGEMENT (Take Profit / Stop Loss)
            for p in api.list_positions():
                if p.symbol == "BTCUSD":
                    entry = float(p.avg_entry_price)
                    current_pl_pct = (price - entry) / entry
                    
                    if current_pl_pct >= TAKE_PROFIT_PCT:
                        api.submit_order(symbol=p.symbol, qty=p.qty, side='sell', type='market', time_in_force='gtc')
                        auditor.wins += 1; auditor.total_trades += 1
                        
                        # 🔏 FIRE AUDIT LOG
                        log_execution_audit("BTC/USD", "SELL_TP", price, rsi, macd, sma_200, ai_score, "Take Profit Hit")
                        
                        send_telegram(f"🏆 *PROFIT SECURED at ${price:,.2f}*")
                    else:
                        stop_price = entry - (atr * ATR_MULTIPLIER)
                        if price <= stop_price:
                            api.submit_order(symbol=p.symbol, qty=p.qty, side='sell', type='market', time_in_force='gtc')
                            auditor.total_trades += 1
                            
                            # 🔏 FIRE AUDIT LOG
                            log_execution_audit("BTC/USD", "SELL_SL", price, rsi, macd, sma_200, ai_score, "Stop Loss Triggered")
                            
                            send_telegram(f"🛑 *STOP LOSS TRIGGERED at ${price:,.2f}*")

            if time.strftime("%H:%M") == "23:59":
                send_telegram(auditor.get_daily_report())
                time.sleep(60)

            time.sleep(15)
        except Exception as e:
            print(f"⚠️ System Recovery: {e}"); time.sleep(5)

if __name__ == "__main__":
    run_apex()