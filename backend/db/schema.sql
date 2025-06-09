 
CREATE TABLE IF NOT EXISTS instruments (
    instrument_token BIGINT PRIMARY KEY,
    tradingsymbol TEXT,
    name TEXT,
    exchange TEXT,
    segment TEXT,
    instrument_type TEXT,
    expiry DATE,
    strike NUMERIC,
    tick_size NUMERIC,
    lot_size INTEGER,
    last_price NUMERIC
);

CREATE TABLE IF NOT EXISTS ohlcv (
    id SERIAL PRIMARY KEY,
    instrument_token BIGINT,
    timestamp TIMESTAMPTZ,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    interval TEXT,
    FOREIGN KEY (instrument_token) REFERENCES instruments(instrument_token)
);

CREATE TABLE IF NOT EXISTS trades (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    symbol TEXT,
    price NUMERIC,
    quantity INTEGER,
    direction TEXT,
    strategy TEXT,
    pnl NUMERIC
);
