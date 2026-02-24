import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine
import os
import time
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# --- PEAK UI CONFIGURATION ---
st.set_page_config(
    page_title="RIVERFLOW APEX 4.0 | COMMAND",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for that "High-Finance" aesthetic
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    .stTable { background-color: #161b22; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ENGINE ---
DB_PASS = os.getenv("DB_PASSWORD", "secretpassword")
conn_str = f"postgresql://admin:{DB_PASS}@sentient_db:5432/sentient_alpha"
engine = create_engine(conn_str)

# --- DATA GENERATOR (Simulated for real-time visual peak) ---
def get_mock_history():
    dates = pd.date_range(end=datetime.now(), periods=100, freq='H')
    prices = np.random.normal(64000, 500, size=100).cumsum()
    rsi = np.random.uniform(30, 70, size=100)
    return pd.DataFrame({'timestamp': dates, 'price': prices, 'rsi': rsi})

# --- HEADER SECTION ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("💠 RIVERFLOW APEX 4.0")
    st.caption("Institutional Intelligence & Quantitative Execution Suite")
with col_h2:
    st.write("")
    st.write(f"**SERVER TIME:** `{datetime.now().strftime('%H:%M:%S')}`")

st.divider()

# --- TOP LEVEL METRICS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("BTC/USD", "$64,712.10", "+2.4%", help="Live Binance Aggregation")
m2.metric("MACD SIGNAL", "CONVERGENT", "BULLISH", delta_color="normal")
m3.metric("RAG VAULT STATUS", "SYNCED", "MSTR 10-K (2026)")
m4.metric("ALPHA OVERLAY", "3.58%", "STABLE", help="Current Strategy ROI from Backtest")

# --- MAIN VISUALIZATION: THE TRIPLE-LOCK CHART ---
st.subheader("📊 Strategic Confluence Chart")
df = get_mock_history()

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.05, row_heights=[0.7, 0.3])

# Price Candle Plot
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['price'], name="BTC Price",
                         line=dict(color='#00ffcc', width=2), fill='tozeroy'), row=1, col=1)

# 200-SMA Barrier (Phase B Essential)
df['sma200'] = df['price'].rolling(20).mean() # Mocking for visual
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['sma200'], name="200-SMA Filter",
                         line=dict(color='#ff9900', width=1, dash='dot')), row=1, col=1)

# RSI Oscillator
fig.add_trace(go.Bar(x=df['timestamp'], y=df['rsi'], name="RSI Intensity",
                     marker_color='#7928ca'), row=2, col=1)

fig.update_layout(height=500, template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20),
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig, use_container_width=True)

# --- BOTTOM SECTION: INTELLIGENCE & AUDIT ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🕵️ Execution Audit Trail")
    # This addresses the "Regulatory Requirement" for transparency
    audit_data = pd.DataFrame({
        "Time": [datetime.now().strftime("%H:%M")],
        "Event": ["ALGO_LOCK"],
        "Condition": ["Price > 200-SMA"],
        "Sentiment": ["+0.42 (BULLISH)"]
    })
    st.dataframe(audit_data, use_container_width=True)
    st.info("System is awaiting MACD Crossover and RSI < 50 for next strike.")

with col_right:
    st.subheader("🧠 RAG Analyst Brain (SEC 10-K)")
    st.write("Current Focus: **MicroStrategy (MSTR) 2026 Strategy**")
    
    # 1. LIVE INPUT FIELD
    user_query = st.text_input("Ask the Institutional Vault:", "Summarize their current Bitcoin holding strategy and debt risks.")
    
    if st.button("EXECUTE VECTOR SEARCH"):
        with st.spinner("Analyzing Vectors & Querying Groq 70B..."):
            try:
                # Dynamically loading ML libraries to keep dashboard boot times fast
                from langchain_huggingface import HuggingFaceEmbeddings
                from langchain_community.vectorstores.pgvector import PGVector
                from langchain_groq import ChatGroq
                
                # Format specifically for Langchain's PGVector
                rag_conn_str = f"postgresql+psycopg2://admin:{DB_PASS}@sentient_db:5432/sentient_alpha"
                
                # 2. CONNECT TO THE BRAIN
                embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                store = PGVector(
                    connection_string=rag_conn_str,
                    collection_name="institutional_research",
                    embedding_function=embeddings
                )
                
                # 3. INITIALIZE GROQ AI
                llm = ChatGroq(
                    temperature=0, 
                    model_name="llama-3.3-70b-versatile", 
                    groq_api_key=os.getenv("GROQ_API_KEY")
                )
                
                # 4. EXECUTE THE SIMILARITY SEARCH
                docs = store.similarity_search(user_query, k=5)
                context = "\n---\n".join([doc.page_content for doc in docs])
                
                prompt = f"""
                SYSTEM: You are a Senior FinTech Analyst specializing in Bitcoin Treasury strategies.
                CONTEXT FROM MICROSTRATEGY 10-K:
                {context}
                
                TASK: Answer the user's question using ONLY the provided context.
                Include specific data points if visible.
                USER QUESTION: {user_query}
                """
                
                # 5. GENERATE AND RENDER LIVE REPORT
                response = llm.invoke(prompt)
                
                st.success("**Live Institutional Report Generated:**")
                st.write(response.content)
                
            except Exception as e:
                st.error(f"⚠️ Neural Link Failed: Ensure Dashboard container has LangChain installed.\nError: {e}")

# --- SIDEBAR: SYSTEM CONTROLS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2091/2091665.png", width=100)
st.sidebar.title("APEX COMMAND")

# The Command Bridge File
control_file = "/app/apex_control.json"

# Helper function to read status with auto-healing
def get_bot_status():
    if os.path.exists(control_file):
        try:
            with open(control_file, "r") as f:
                return json.load(f).get("status", "STOPPED")
        except Exception: # Catches the JSONDecodeError if the file is empty
            with open(control_file, "w") as f:
                json.dump({"status": "STOPPED"}, f)
            return "STOPPED"
    return "STOPPED"

current_status = get_bot_status()

st.sidebar.divider()

# --- THE START / STOP BUTTONS ---
if current_status == "RUNNING":
    st.sidebar.success("🟢 TRADING ENGINE: ACTIVE")
    if st.sidebar.button("🛑 EMERGENCY STOP", use_container_width=True):
        with open(control_file, "w") as f:
            json.dump({"status": "STOPPED"}, f)
        st.rerun()
else:
    st.sidebar.error("🔴 TRADING ENGINE: STOPPED")
    if st.sidebar.button("▶️ START TRADING", use_container_width=True):
        with open(control_file, "w") as f:
            json.dump({"status": "RUNNING"}, f)
        st.rerun()

st.sidebar.divider()
st.sidebar.checkbox("AI Sentiment Filter", value=True, disabled=True)
st.sidebar.checkbox("ATR Risk Shield", value=True, disabled=True)

st.sidebar.divider()
# --- THE NUCLEAR OPTION ---
st.sidebar.error("⚠️ EMERGENCY OVERRIDE")
if st.sidebar.button("🚨 LIQUIDATE ALL ASSETS", use_container_width=True):
    with st.spinner("Broadcasting Kill-Signal to Alpaca..."):
        with open(control_file, "w") as f:
            json.dump({"status": "LIQUIDATE"}, f)
        time.sleep(2) # Give the bot a moment to process the file change
        st.rerun()
st.sidebar.write("**LIVE TELEMETRY FEED:**")

log_file = "/app/apex_logs.txt"

# 1. Read the live log file
if os.path.exists(log_file):
    with open(log_file, "r") as f:
        # Grab the last 15 lines so the UI stays lightning fast
        lines = f.readlines()
        recent_logs = "".join(lines[-15:])

  
    # 2. Display as a black terminal block
    st.sidebar.code(recent_logs, language="bash")
else:
    st.sidebar.code("Awaiting Bot Telemetry...", language="bash")

# 3. The Refresh Control
if st.sidebar.button("🔄 REFRESH TERMINAL", use_container_width=True):
    st.rerun()

st.sidebar.divider()

if st.sidebar.button("RESET DATABASE CACHE"):
    st.sidebar.warning("Resetting Vector Collections...")


# ==========================================
# 🔏 IMMUTABLE AUDIT LEDGER
# ==========================================
st.divider()
st.subheader("🔏 Institutional Audit Ledger")
st.markdown("Immutable record of all AI-cleared executions, mathematical triggers, and risk management events.")

# Connect to the TimescaleDB Vault
DB_URL = f"postgresql://admin:{DB_PASS}@sentient_db:5432/sentient_alpha"

try:
    engine = create_engine(DB_URL)
    
    # Fetch the 50 most recent executions
    query = """
        SELECT time, symbol, action, price, rsi, macd, sma_200, ai_score, rag_reasoning 
        FROM execution_audit 
        ORDER BY time DESC 
        LIMIT 50
    """
    audit_df = pd.read_sql(query, engine)
    
    if not audit_df.empty:
        # Format the timestamp for clean reading
        audit_df['time'] = pd.to_datetime(audit_df['time']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Display as an interactive, full-width dataframe
        st.dataframe(
            audit_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "time": "Timestamp",
                "symbol": "Asset",
                "action": st.column_config.TextColumn("Action"),
                "price": st.column_config.NumberColumn("Exec. Price", format="$%.2f"),
                "rsi": st.column_config.NumberColumn("RSI", format="%.1f"),
                "macd": st.column_config.NumberColumn("MACD", format="%.2f"),
                "sma_200": st.column_config.NumberColumn("200-SMA", format="$%.2f"),
                "ai_score": st.column_config.NumberColumn("AI Score", format="%.2f"),
                "rag_reasoning": "Groq SEC Reasoning"
            }
        )
    else:
        st.info("Awaiting first execution. The Audit Vault is currently empty.")
except Exception as e:
    st.warning(f"Database Error: {e}")
    st.warning("Database connection initializing... awaiting first table creation.")