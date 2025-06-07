-- Optional: create DB if not already done via Docker
-- CREATE DATABASE algodb;

-- Use the DB
-- \c algodb;

-- Table to store instrument metadata (e.g., NIFTY, INFY)
CREATE TABLE IF NOT EXISTS instruments (
    instrument_token BIGINT PRIMARY KEY,
    tradingsymbol VARCHAR(50),
    name VARCHAR(100),
    exchange VARCHAR(20),
    lot_size INT,
    tick_size FLOAT
);

-- Table to store historical OHLCV data
CREATE TABLE IF NOT EXISTS ohlcv (
    id SERIAL PRIMARY KEY,
    instrument_token BIGINT REFERENCES instruments(instrument_token),
    timestamp TIMESTAMPTZ NOT NULL,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume BIGINT,
    UNIQUE (instrument_token, timestamp)
);

-- Table to log trades executed by strategies
CREATE TABLE IF NOT EXISTS trades (
    id SERIAL PRIMARY KEY,
    strategy_name VARCHAR(50),
    instrument_token BIGINT REFERENCES instruments(instrument_token),
    order_type VARCHAR(10),        -- BUY or SELL
    quantity INT,
    price FLOAT,
    executed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table to log backtest or live strategy performance
CREATE TABLE IF NOT EXISTS performance_metrics (
    id SERIAL PRIMARY KEY,
    strategy_name VARCHAR(50),
    date DATE,
    total_trades INT,
    win_rate FLOAT,
    pnl FLOAT,
    max_drawdown FLOAT,
    sharpe_ratio FLOAT
);
