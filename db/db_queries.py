INSERT_TICKERS_IGNORE_DUPLICATES = """
    INSERT IGNORE INTO stocks_sports.stock_tickers
    (symbol, name, exchange)
    VALUES (%s, %s, %s);
"""

INSERT_STOCK_PRICE_ROWS_IGNORE_DUPLICATES = """
    INSERT IGNORE INTO stocks_sports.stock_prices
    (symbol, date, low_price, high_price)
    VALUES (%s, %s, %s, %s);
"""


INSERT_STOCK_PRICE_ROWS = """
    INSERT INTO stocks_sports.stock_prices
    (symbol, date, low_price, high_price)
    VALUES (%s, %s, %s, %s);
"""


INSERT_SPORTS = """
    INSERT INTO stocks_sports.sports
    (sport_key, sport_friendly_name, league_title, sport_type)
    VALUES (%s, %s, %s, %s);
"""


GET_SPORTS_KEYS = """
    SELECT sport_key 
    FROM stocks_sports.sports;
"""


GET_STOCK_TICKERS = """
    SELECT symbol 
    FROM stocks_sports.stock_tickers;
"""


GET_ODDS_PROVIDERS = """
    SELECT name 
    FROM stocks_sports.odds_providers;
"""


GET_SPORTS = """
    SELECT sport_key, sport_friendly_name
    FROM stocks_sports.sports;
"""
