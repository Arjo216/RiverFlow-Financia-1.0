# RiverFlow-Financia-1.0
Autonomous Multi-Agent Hedge Fund Architecture. Combines Event-Driven Microservices (Kafka), Real-Time Market Data (TimescaleDB), and AI Agents (RAG/GNN) for institutional-grade alpha generation

# 🌊 RiverFlow Finance: AI-Driven Event Pipeline

# 💠 RiverFlow Apex 4.0: Autonomous Intelligence Engine
> **Next-Generation Quantitative Trading Framework with Groq AI Reasoning**

RiverFlow Apex is an institutional-grade algorithmic trading suite that fuses high-speed technical analysis with Large Language Model (LLM) sentiment synthesis. It is designed for autonomous execution on the Alpaca paper trading exchange.

## 🚀 Core Architecture
* **Neural Engine**: Leverages Llama-3.3-70B via **Groq LPUs** for sub-second financial news reasoning.
* **Technical Suite**: Integrated **RSI, MACD, and ATR** calculators for multi-factor signal confluence.
* **Volatility Shield**: Dynamic risk management using **Average True Range (ATR)** to adapt stop-losses to market regimes.
* **Real-time Intelligence**: Live news aggregation via **CryptoPanic API**.
* **Mobile Command**: Professional Markdown-formatted alerts via **Telegram Bot API**.

## 📊 Strategy Confluence (Triple-Lock)
A trade is only executed when three distinct independent layers agree:
1.  **Math**: RSI indicates an oversold dip (< 40).
2.  **Momentum**: MACD signal crossover confirms upward trend.
3.  **Sentiment**: Groq AI assigns a confidence score > 0.3 to the current news cycle.

## 🛠️ Tech Stack
* **Language**: Python 3.9+
* **Infrastructure**: Docker & Docker Compose
* **Database**: TimescaleDB (Time-series optimized PostgreSQL)
* **Messaging**: Redpanda (High-performance Kafka alternative)

## 🛡️ Risk Management
* **Stop-Loss**: Volatility-adjusted (ATR x 2.0).
* **Take-Profit**: Fixed at 4% for disciplined capital harvesting.
* **Position Sizing**: Hard-capped at 10% of total equity per trade.

## 🚦 Quick Start (Post-Maintenance)
1. **Initialize Infrastructure**: `docker-compose up -d`
2. **Deploy Strategy**: `docker cp services/market_data/strategy.py sentient_writer:/app/strategy.py`
3. **Engage Engine**: `docker exec -it sentient_writer python strategy.py`

---

### 1. Prerequisites
* Docker & Docker Compose installed.
* Alpaca Markets API Keys (Free Tier).
* Hugging Face Access Token (Write permissions).


*Disclaimer: For educational purposes only. Automated trading involves significant risk of loss.*


### 2. Environment Setup
Create a `.env` file in the root directory:
```bash
ALPACA_KEY=your_alpaca_key
ALPACA_SECRET=your_alpaca_secret
DB_PASSWORD=secretpassword
HUGGINGFACE_TOKEN=hf_your_token
KAFKA_BROKER=redpanda:9092


📂 Project Structure
├── services/
│   ├── market_data/        # Ingestor & Writer services
│   └── edgar_processor/    # AI Analyst service
├── scripts/
│   └── init_db.sql         # Database schema & vector extension
├── docker-compose.yml      # Orchestration
├── requirements.txt        # Dependencies
└── README.md               # Documentation



🔮 Future Roadmap:
Connect AI Analyst to Live News API.

Implement Trading Execution based on Sentiment + Technical Analysis.

Deploy to Kubernetes (EKS/GKE).

---

### **Part 2: Safe Git Push (Do Not Leak Keys!)**

Before you push to GitHub, we **MUST** ignore your `.env` file so hackers don't steal your API keys.

#### **Step 1: Create a `.gitignore` file**
Run this command to create a file that tells Git what to ignore:

```bash
echo ".env" > .gitignore
echo "__pycache__/" >> .gitignore
echo "venv/" >> .gitignore
echo "*.log" >> .gitignore