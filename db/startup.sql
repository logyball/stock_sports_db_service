SET GLOBAL time_zone = '-7:00';

CREATE DATABASE IF NOT EXISTS stocks_sports;

CREATE TABLE IF NOT EXISTS stocks_sports.stock_prices (
    symbol VARCHAR(10),
    date DATE,
    low_price DECIMAL(20, 2),
    high_price DECIMAL(20, 2),

    PRIMARY KEY (symbol, date)
);


CREATE TABLE IF NOT EXISTS stocks_sports.stock_tickers (
    symbol VARCHAR(10),
    name VARCHAR(255),
    exchange VARCHAR(50),

    PRIMARY KEY (symbol)
);

/*
    TODO - create users table
    TODO - create "portfolio" table
*/