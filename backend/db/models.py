from sqlalchemy import Column, BigInteger, Integer, Float, String, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Instrument(Base):
    __tablename__ = 'instruments'
    instrument_token = Column(BigInteger, primary_key=True)
    tradingsymbol = Column(String)
    name = Column(String)
    exchange = Column(String)
    segment = Column(String)
    instrument_type = Column(String)
    expiry = Column(Date)
    strike = Column(Float)
    tick_size = Column(Float)
    lot_size = Column(Integer)
    last_price = Column(Float)

class OHLCV(Base):
    __tablename__ = 'ohlcv'
    id = Column(Integer, primary_key=True)
    instrument_token = Column(BigInteger, ForeignKey('instruments.instrument_token'))
    timestamp = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)
    interval = Column(String)

class Trade(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    symbol = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    direction = Column(String)
    strategy = Column(String)
    pnl = Column(Float)
