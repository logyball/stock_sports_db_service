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

GET_SINGLE_TEAM = """
    SELECT COUNT(*) 
    FROM stocks_sports.sports_teams
    WHERE team_name = %s
    AND sport_key = %s;
"""

CHECK_SINGLE_GAME_EXISTS = """
    SELECT COUNT(*)
    FROM stocks_sports.games
    WHERE home_team_id = %s
    AND away_team_id = %s
    AND game_start_timestamp = %s
    AND sport_key = %s;
"""

GET_SINGLE_GAME_ID = """
    SELECT id
    FROM stocks_sports.games
    WHERE home_team_id = %s
    AND away_team_id = %s
    AND game_start_timestamp = %s
    AND sport_key = %s;
"""

GET_SINGLE_TEAM_ID = """
    SELECT id
    FROM stocks_sports.sports_teams
    WHERE team_name = %s
    AND sport_key = %s;
"""

INSERT_SINGLE_GAME_RETURN_ID = """
    INSERT INTO stocks_sports.games
    (game_start_timestamp, sport_key, home_team_id, away_team_id)
    VALUES (%s, %s, %s, %s);
"""

INSERT_SINGLE_TEAM_RETURN_ID = """
    INSERT INTO stocks_sports.sports_teams
    (team_name, sport_key)
    VALUES (%s, %s);
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
