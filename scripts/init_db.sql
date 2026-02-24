-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- ==========================================
-- 1. Market Data Table (OHLCV)
-- ==========================================
CREATE TABLE IF NOT EXISTS market_candles (
    time TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    price DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    type TEXT
);

-- Turn it into a Hypertable
SELECT create_hypertable('market_candles', 'time', if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS idx_market_candles_symbol_time ON market_candles (symbol, time DESC);

-- ==========================================
-- 2. Immutable Audit Table (FIXED)
-- ==========================================
CREATE TABLE IF NOT EXISTS execution_audit (
    time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    id SERIAL,
    symbol TEXT NOT NULL,
    action TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    rsi NUMERIC(5, 2),
    macd NUMERIC(10, 2),
    sma_200 NUMERIC(10, 2),
    ai_score NUMERIC(5, 2),
    rag_reasoning TEXT,
    PRIMARY KEY (id, time)  -- FIXED: Combined PK for TimescaleDB compliance
);

-- Convert to a TimescaleDB Hypertable
SELECT create_hypertable('execution_audit', 'time', if_not_exists => TRUE);