# RiverFlow-Financia-1.0
Autonomous Multi-Agent Hedge Fund Architecture. Combines Event-Driven Microservices (Kafka), Real-Time Market Data (TimescaleDB), and AI Agents (RAG/GNN) for institutional-grade alpha generation

# 🌊 RiverFlow Finance: AI-Driven Event Pipeline

**RiverFlow Finance** is an autonomous, event-driven financial data pipeline designed to ingest real-time market data and analyze financial sentiment using AI.

It combines **High-Frequency Data Engineering** (Kafka/Redpanda) with **Generative AI** (RAG/Vector Embeddings) to create a system that "sees" price movements and "reads" financial reports simultaneously.

---

## 🚀 Architecture

The system is containerized using Docker and consists of four main components:

### 1. 📡 Market Ingestor (The Eyes)
* **Tech:** Python, Alpaca API (WebSockets)
* **Role:** Listens to real-time crypto markets (e.g., BTC/USD).
* **Output:** Streams raw trade/quote data into the Event Bus.

### 2. 📨 Event Bus (The Nervous System)
* **Tech:** Redpanda (Kafka-compatible), High-throughput
* **Role:** Buffers data between producers and consumers to ensure zero data loss during high-volatility bursts.

### 3. 💾 Data Persistence (The Memory)
* **Tech:** TimescaleDB (PostgreSQL Extension)
* **Role:** Stores massive amounts of time-series market data.
* **Writer Service:** A dedicated Python consumer that pulls from Kafka and writes to DB efficiently.

### 4. 🧠 AI Analyst (The Brain)
* **Tech:** LangChain, Hugging Face, pgvector
* **Role:** Reads financial documents (10-K filings, news), converts text into Vector Embeddings, and stores them in `pgvector` for Semantic Search and RAG (Retrieval-Augmented Generation).

---

## 🛠️ Tech Stack

* **Languages:** Python 3.9+
* **Infrastructure:** Docker, Docker Compose
* **Streaming:** Redpanda (Kafka)
* **Database:** TimescaleDB + pgvector
* **AI/ML:** LangChain, Sentence-Transformers (Hugging Face)

---

## ⚡ Quick Start

### 1. Prerequisites
* Docker & Docker Compose installed.
* Alpaca Markets API Keys (Free Tier).
* Hugging Face Access Token (Write permissions).

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