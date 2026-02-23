<div align="center">

# 🌊 RiverFlow Apex 4.0
**Autonomous Multi-Agent Hedge Fund Architecture**

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)](#)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](#)
[![TimescaleDB](https://img.shields.io/badge/TimescaleDB-Optimized-F0B70D?style=for-the-badge&logo=postgresql&logoColor=black)](#)
[![AI Reasoner](https://img.shields.io/badge/Groq-Llama_3.3_70B-f44336?style=for-the-badge&logo=meta&logoColor=white)](#)
[![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen?style=for-the-badge)](#)

*Fusing Event-Driven Microservices (Kafka), Real-Time Market Data (TimescaleDB), and AI Agents (RAG/GNN) for institutional-grade alpha generation.*

</div>

---

## 💠 The Autonomous Intelligence Engine
> *"RiverFlow prioritizes the reliability of a Honda over the theoretical speed of a Formula 1 car without brakes."*

**RiverFlow Apex** is an institutional-grade algorithmic trading suite that fuses high-speed technical analysis with Large Language Model (LLM) sentiment synthesis. It is designed for autonomous execution on the Alpaca paper trading exchange, utilizing a strict Triple-Node Architecture.

### 🚀 Core Architecture
* 🧠 **Neural Engine**: Leverages `Llama-3.3-70B` via **Groq LPUs** for sub-second financial news and SEC filing reasoning.
* 📈 **Technical Suite**: Integrated **RSI, MACD, and 200-SMA** calculators for multi-factor signal confluence.
* 🛡️ **Volatility Shield**: Dynamic risk management using the **Average True Range (ATR)** to adapt stop-losses to shifting market regimes.
* ⚡ **Real-time Intelligence**: Live news aggregation via the **CryptoPanic API** and fundamental clearance via a PGVector SEC Vault.
* 📱 **Mobile Command**: Professional Markdown-formatted auditing and live alerts via the **Telegram Bot API**.

---

## 📊 Strategy Confluence (The Triple-Lock)
A trade is only executed when three distinct, independent layers agree. If one fails, the trade is blocked.

1. **Math**: RSI indicates an oversold dip (`< 50`) and Price > 200-SMA.
2. **Momentum**: MACD signal crossover confirms an upward trend.
3. **Sentiment**: Groq AI parses live news and assigns a confidence score `> +0.3`.

---

## 🛠️ Technology Stack
| Component | Technology | Description |
| :--- | :--- | :--- |
| **Logic** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | Core quantitative logic and ML pipeline execution. |
| **Infra** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) | Multi-container isolation for strict separation of concerns. |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/TimescaleDB-316192?style=flat-square&logo=postgresql&logoColor=white) | Time-series optimized vector storage for market data and RAG. |
| **Stream** | ![Apache Kafka](https://img.shields.io/badge/Redpanda-231F20?style=flat-square&logo=apachekafka&logoColor=white) | High-performance, low-latency event streaming. |

---

## 🚦 Quick Start & Deployment
*Disclaimer: For educational purposes only. Automated trading involves significant risk of loss.*

### 1. Prerequisites
* Docker & Docker Compose installed.
* Alpaca Markets API Keys (Free Tier).
* Hugging Face Access Token (Write permissions).

### 2. Secure Environment Setup
Create a `.env` file in the root directory. **(Never commit this file to version control).**
```bash
ALPACA_KEY=your_alpaca_key
ALPACA_SECRET=your_alpaca_secret
DB_PASSWORD=mysecretpassword0
HUGGINGFACE_TOKEN=hf_your_token
KAFKA_BROKER=redpanda:9092


3. Initialize the Engine
Bash
# Boot the multi-container infrastructure
docker-compose up -d

# Deploy the live strategy to the execution node
docker cp services/market_data/strategy.py sentient_writer:/app/strategy.py

# Engage the execution engine
docker exec -it sentient_writer python strategy.py


📂 Project Structure
Plaintext
RiverFlow-Financia-1.0/
├── services/
│   ├── market_data/        # Live Ingestor & Trading Bot Strategy
│   └── edgar_processor/    # AI Analyst & Streamlit Dashboard UI
├── scripts/
│   └── init_db.sql         # Database schema & PGVector extensions
├── docker-compose.yml      # Orchestration & Volume Mapping
├── requirements.txt        # Container Dependencies
└── README.md               # Architecture Documentation


🛡️ Risk & Security Parameters
Capital Protection: Position sizes are hard-capped at 10% of total equity per trade.

Stop-Loss: Volatility-adjusted trailing proxy (ATR x 3.0).

Take-Profit: Fixed target at 2% for disciplined capital harvesting.


⚠️ Security Warning: Safe Git Push Protocol
Before pushing this repository to GitHub, you MUST configure your exclusions to prevent API key leaks. Create a .gitignore file in your root directory and run:

Bash
echo ".env" > .gitignore
echo "__pycache__/" >> .gitignore
echo "venv/" >> .gitignore
echo "*.log" >> .gitignore


🗺️ Strategic Roadmap & Architecture Analysis
This project is guided by a comprehensive institutional SWOT analysis (The RiverFlow Framework), prioritizing regulatory compliance and architectural reliability over experimental features.

Q1 2026 Strategy Assessment
Strategic Dimension,Assessment,Score,Action Plan
Intellectual Differentiation,⭐⭐⭐⭐⭐,9/10,Maintain: Multi-agent architecture remains core.
Industry Alignment,⭐⭐⭐⭐⭐,9/10,Focus: Double down on RAG & Compliance.
Data Pipeline (Phase 1),⭐⭐⭐⭐⭐,10/10,Completed: RiverFlow Apex 4.0 is production-ready.
RAG Implementation,⭐⭐⭐⭐,7/10,Next Step: Implement hallucination evaluation suites.
GNN Risk Modeling,⭐⭐,3/10,"Pivot: Downgrade to ""Research Prototype"" status."
RL Execution,⭐⭐,3/10,Mitigate: Replace with Rule-Based Execution (Current).
Regulatory Compliance,⭐,2/10,Critical: Immediate focus for next iteration.


🔭 Future Development Phases
🟢 Phase A: The "Analyst" Upgrade (RAG Pipeline) - [IN PROGRESS]
[x] Data Source: Integrate direct SEC 10-K filing downloads.

[x] Architecture: Deploy dedicated analyst-agent service using LangChain.

[ ] Compliance: Add "Citation Tracking" to link specific trade signals to document page numbers.

[ ] Quality: Implement FailSafeQA benchmarks to measure hallucination rates.

🟡 Phase B: The "Glass Box" Dashboard - [DEPLOYED]
[x] Frontend: Streamlit dashboard for real-time monitoring and Emergency Liquidation overrides.

[x] Explainability: Visual breakdown of the "Triple-Lock" signal and Terminal Telemetry.

[ ] Audit Trail: Immutable logs of why every trade was executed (Regulatory requirement).

🔴 Phase C: Supply Chain Graph (Research) - [PENDING]
[ ] Graph DB: Initialize Neo4j for macro relationship mapping.

[ ] Inference: Offline analysis of supplier shock propagation.

[ ] Isolation: Run strictly in "Shadow Mode" (no execution authority).

<div align="center">



<i>Engineered for Alpha. Built for Resilience.</i>
</div>