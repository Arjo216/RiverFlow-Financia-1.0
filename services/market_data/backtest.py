import pandas as pd
import numpy as np
import yfinance as yf
import time

# --- BACKTEST PARAMETERS ---
# --- OPTIMIZED BACKTEST PARAMETERS ---
INITIAL_CAPITAL = 10000.0  
POSITION_SIZE = 0.10       
TAKE_PROFIT_PCT = 0.02     # Lowered from 4% to 2% (Realistic 1H target)
ATR_MULTIPLIER = 3.0       # Raised from 2.0 to 3.0 (Wider stop-loss to avoid fake-outs)

print("💠 RIVERFLOW APEX 4.0: QUANTITATIVE BACKTEST SUITE (v2)")
print("📥 Downloading 2 Years of Historical Hourly Data...")

# 1. FETCH HISTORICAL DATA
df = yf.download('BTC-USD', period='2y', interval='1h', progress=False)

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.droplevel(1)
df = df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'})
df = df.dropna()

print(f"✅ Loaded {len(df):,} hours of Bitcoin market data.")
print("⚙️ Crunching Institutional Indicators & Macro Filters...")

# 2. CALCULATE INDICATORS
# RSI
delta = df['close'].diff()
gain = (delta.where(delta > 0, 0)).fillna(0)
loss = (-delta.where(delta < 0, 0)).fillna(0)
avg_gain = gain.ewm(com=13, min_periods=14).mean()
avg_loss = loss.ewm(com=13, min_periods=14).mean()
df['rsi'] = 100 - (100 / (1 + (avg_gain / avg_loss)))

# MACD
df['ema_fast'] = df['close'].ewm(span=12, adjust=False).mean()
df['ema_slow'] = df['close'].ewm(span=26, adjust=False).mean()
df['macd'] = df['ema_fast'] - df['ema_slow']
df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()

# ATR Proxy
df['tr'] = df['high'] - df['low']
df['atr'] = df['tr'].rolling(14).mean()

# 🛡️ THE NEW MACRO FILTER: 200 SMA
df['sma_200'] = df['close'].rolling(window=200).mean()

# Drop the first 200 hours because they don't have enough data to calculate the SMA
df = df.dropna()

# 3. THE SIMULATION ENGINE
print("🚀 Initiating Trend-Filtered Historical Simulation...\n")

capital = INITIAL_CAPITAL
position_qty = 0
entry_price = 0
wins = 0
losses = 0
trade_log = []

for index, row in df.iterrows():
    price = row['close']
    rsi = row['rsi']
    macd = row['macd']
    sig = row['signal']
    atr = row['atr']
    sma_200 = row['sma_200']

    # --- IF WE HAVE NO OPEN POSITION ---
    if position_qty == 0:
        # 🛡️ THE NEW RULE: Price MUST be > sma_200 to execute a buy
        if rsi < 50 and macd > sig and price > sma_200:
            trade_amount = capital * POSITION_SIZE
            position_qty = trade_amount / price
            capital -= trade_amount
            entry_price = price

    # --- IF WE ARE IN A TRADE ---
    elif position_qty > 0:
        current_pl_pct = (price - entry_price) / entry_price
        stop_price = entry_price - (atr * ATR_MULTIPLIER)

        # A. Take Profit Hit
        if current_pl_pct >= TAKE_PROFIT_PCT:
            capital += position_qty * price
            position_qty = 0
            wins += 1
            trade_log.append("WIN")
            
        # B. Volatility Stop-Loss Hit
        elif price <= stop_price:
            capital += position_qty * price
            position_qty = 0
            losses += 1
            trade_log.append("LOSS")

# Liquidate any open position at the end of the 2 years
if position_qty > 0:
    capital += position_qty * df.iloc[-1]['close']

# 4. PERFORMANCE TEAR SHEET
total_trades = wins + losses
win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
net_profit = capital - INITIAL_CAPITAL
roi = (net_profit / INITIAL_CAPITAL) * 100

print("==================================================")
print("📊 APEX 4.0: TREND-FILTERED TEAR SHEET")
print("==================================================")
print(f"⏱️ Timeframe Evaluated : 2 Years (Hourly)")
print(f"💵 Initial Capital     : ${INITIAL_CAPITAL:,.2f}")
print(f"💰 Final Equity        : ${capital:,.2f}")
print(f"📈 Net Profit          : ${net_profit:,.2f} ({roi:+.2f}%)")
print("--------------------------------------------------")
print(f"🔄 Total Executions    : {total_trades}")
print(f"🏆 Winning Trades      : {wins}")
print(f"🛑 Losing Trades       : {losses}")
print(f"🎯 Strategy Win Rate   : {win_rate:.1f}%")
print("==================================================")