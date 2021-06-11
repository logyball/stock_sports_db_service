from sqlalchemy import Column, String, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
SqlAlchemyBase = declarative_base()


class Stock(SqlAlchemyBase):
    __tablename__ = 'stock_prices'
    symbol: Column = Column(String, primary_key=True)
    date: Column = Column(Date, primary_key=True)
    low_price: Column = Column(DECIMAL)
    high_price: Column = Column(DECIMAL)


class Ticker(SqlAlchemyBase):
    __tablename__ = 'stock_tickers'
    symbol: Column = Column(String, primary_key=True)
    name: Column = Column(String)
    exchange: Column = Column(String)