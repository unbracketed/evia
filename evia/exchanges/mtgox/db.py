from datetime import datetime
from sqlalchemy import Column, DateTime, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class MtGoxTicker(Base):
    __tablename__ = 'ticker_mtgox'

    timestamp = Column(DateTime, primary_key=True)
    time_received = Column(DateTime, default=datetime.now())
    symbol = Column(String)
    high = Column(Float)
    low = Column(Float)
    avg = Column(Float)
    vwap = Column(Float)
    vol = Column(Float)
    last_local = Column(Float)
    last_orig = Column(Float)
    last_all = Column(Float)
    last = Column(Float)
    buy = Column(Float)
    sell = Column(Float)


class MtGoxTrade(Base):
    __tablename__ = 'trades_mtgox'

    type = Column(String)
    date = Column(DateTime)
    amount = Column(Float)
    price = Column(Float)
    tid = Column(String, primary_key=True)
    price_currency = Column(String)
    trade_type = Column(String)
    primary = Column(String)
    properties = Column(String)


class MtGoxDepth(Base):
    __tablename__ = 'depth_mtgox'

    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    type_str = Column(String)
    price = Column(Float)
    volume = Column(Float)
    currency = Column(String)
    timestamp = Column(DateTime)
