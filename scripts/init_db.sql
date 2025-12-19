-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- 1. Market Data Table (OHLCV)
CREATE TABLE IF NOT EXISTS market_candles (
    time TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    price DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    type TEXT
);

-- Turn it into a Hypertable (Optimized for time-series)
SELECT create_hypertable('market_candles', 'time');

-- Index for fast retrieval
CREATE INDEX ON market_candles (symbol, time DESC);