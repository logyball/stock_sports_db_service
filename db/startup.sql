
SET GLOBAL time_zone = '-7:00';

CREATE DATABASE IF NOT EXISTS stonks;
USE stonks;

CREATE TABLE IF NOT EXISTS stock_prices (
    symbol VARCHAR(10),
    date DATE,
    low_price DECIMAL(20, 2),
    high_price DECIMAL(20, 2),

    PRIMARY KEY (symbol, date)
);


CREATE TABLE IF NOT EXISTS stock_tickers (
    symbol VARCHAR(10),
    name VARCHAR(255),
    exchange VARCHAR(50),

    PRIMARY KEY (symbol)
);

CREATE USER 'admin'@'%' IDENTIFIED BY 'admin';


/*
    TODO - create users table
    TODO - create "portfolio" table
*/