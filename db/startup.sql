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


CREATE TABLE IF NOT EXISTS stocks_sports.sports (
    sport_key VARCHAR(100),
    sport_friendly_name VARCHAR(255),
    league_title VARCHAR(50),
    sport_type VARCHAR(100),

    PRIMARY KEY (sport_key)
);


CREATE TABLE IF NOT EXISTS stocks_sports.sports_teams (
    id INT NOT NULL AUTO_INCREMENT,
    team_name VARCHAR(255),
    sport_key VARCHAR(100),

    PRIMARY KEY (id),
    FOREIGN KEY (sport_key) REFERENCES stocks_sports.sports(sport_key)
);


CREATE TABLE IF NOT EXISTS stocks_sports.odds_providers (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255),
    friendly_name VARCHAR(100),

    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS stocks_sports.games (
    id INT NOT NULL AUTO_INCREMENT,
    game_start_timestamp DATE,
    sport_key VARCHAR(100),
    home_team_id INT,
    away_team_id INT,

    PRIMARY KEY (id),
    FOREIGN KEY (home_team_id) REFERENCES stocks_sports.sports_teams(id),
    FOREIGN KEY (away_team_id) REFERENCES stocks_sports.sports_teams(id)
);


CREATE TABLE IF NOT EXISTS stocks_sports.h2h_odds (
    id INT NOT NULL AUTO_INCREMENT,
    game_id INT,
    time_collected TIMESTAMP,
    odds_provider_id INT,
    home_odds INT,
    away_odds INT,

    PRIMARY KEY (id),
    FOREIGN KEY (game_id) REFERENCES stocks_sports.games(id),
    FOREIGN KEY (odds_provider_id) REFERENCES stocks_sports.odds_providers(id)
);


CREATE TABLE IF NOT EXISTS stocks_sports.over_under_odds (
    id INT NOT NULL AUTO_INCREMENT,
    game_id INT,
    time_collected TIMESTAMP,
    odds_provider_id INT,
    over_under DECIMAL (20, 3),
    over_odds INT,
    under_odds INT,

    PRIMARY KEY (id),
    FOREIGN KEY (game_id) REFERENCES stocks_sports.games(id),
    FOREIGN KEY (odds_provider_id) REFERENCES stocks_sports.odds_providers(id)
);


CREATE TABLE IF NOT EXISTS stocks_sports.spread_odds (
    id INT NOT NULL AUTO_INCREMENT,
    game_id INT,
    time_collected TIMESTAMP,
    odds_provider_id INT,
    home_spread DECIMAL (20, 3),
    away_spread DECIMAL (20, 3),
    home_odds INT,
    away_odds INT,

    PRIMARY KEY (id),
    FOREIGN KEY (game_id) REFERENCES stocks_sports.games(id),
    FOREIGN KEY (odds_provider_id) REFERENCES stocks_sports.odds_providers(id)
);

/*
    TODO - create users table
    TODO - create "portfolio" table
*/