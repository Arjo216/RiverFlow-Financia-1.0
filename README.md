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
DB_PASSWORD=mysecretpassword0
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

## 🗺️ Strategic Roadmap & Architecture Analysis

This project is guided by a comprehensive institutional SWOT analysis (**RiverFlow Framework**), prioritizing regulatory compliance and architectural reliability over experimental features.

### 🚦 SWOT Summary (Q1 2026 Strategy)

| Strategic Dimension | Assessment | Score | Action Plan |
|---------------------|------------|-------|-------------|
| **Intellectual Differentiation** | ⭐⭐⭐⭐⭐ | 9/10 | **Maintain:** Multi-agent architecture remains core. |
| **Industry Alignment** | ⭐⭐⭐⭐⭐ | 9/10 | **Focus:** Double down on RAG & Compliance. |
| **Data Pipeline (Phase 1)** | ⭐⭐⭐⭐⭐ | 10/10 | **Completed:** RiverFlow Apex 4.0 is production-ready. |
| **RAG Implementation** | ⭐⭐⭐⭐ | 7/10 | **Next Step:** Implement hallucination evaluation suites. |
| **GNN Risk Modeling** | ⭐⭐ | 3/10 | **Pivot:** Downgrade to "Research Prototype" status. |
| **RL Execution** | ⭐⭐ | 3/10 | **Mitigate:** Replace with Rule-Based Execution (Current). |
| **Regulatory Compliance** | ⭐ | 2/10 | **Critical:** Immediate focus for next iteration. |

---

### 🔭 Future Development Phases

#### Phase A: The "Analyst" Upgrade (RAG Pipeline)
**Objective:** Transition from simple headline analysis (Groq) to full document intelligence.
- [ ] **Data Source:** Integrate direct SEC 10-K filing downloads.
- [ ] **Architecture:** Deploy dedicated `analyst-agent` service using LangChain.
- [ ] **Compliance:** Add "Citation Tracking" to link specific trade signals to document page numbers.
- [ ] **Quality:** Implement `FailSafeQA` benchmarks to measure hallucination rates.

#### Phase B: The "Glass Box" Dashboard
**Objective:** Solve the "Black Box" problem by visualizing decision logic.
- [ ] **Frontend:** Streamlit/Next.js dashboard for real-time monitoring.
- [ ] **Explainability:** Visual breakdown of the "Triple-Lock" signal (RSI + MACD + Sentiment).
- [ ] **Audit Trail:** Immutable logs of *why* every trade was executed (Regulatory requirement).

#### Phase C: Supply Chain Graph (Research)
**Objective:** Map hidden supplier risks without affecting production trading.
- [ ] **Graph DB:** Initialize Neo4j for relationship mapping.
- [ ] **Inference:** Offline analysis of supplier shock propagation.
- [ ] **Isolation:** Run strictly in "Shadow Mode" (no execution authority).

> *"RiverFlow prioritizes the reliability of a Honda over the theoretical speed of a Formula 1 car without brakes."*

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
