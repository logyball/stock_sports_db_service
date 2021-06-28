import mysql.connector
from db.db_queries import INSERT_SPORTS, GET_SPORTS_KEYS, GET_SINGLE_TEAM, INSERT_SINGLE_TEAM_RETURN_ID,\
    GET_SINGLE_TEAM_ID, CHECK_SINGLE_GAME_EXISTS, GET_SINGLE_GAME_ID, INSERT_SINGLE_GAME_RETURN_ID, CHECK_SITE_EXISTS, \
    GET_SINGLE_SITE_ID, INSERT_SITE_RETURN_ID, INSERT_H2H_ODDS_ROW_RETURN_ID
from db.db_functions import insert_many_rows, get_many_rows, get_count, insert_single_row_return_id, get_single_row

import logging


def insert_sports(connection: mysql.connector.MySQLConnection, sports: list[tuple]) -> None:
    """
    Using INSERT_SPORTS query, insert rows into the stock_sports.sports
    Duplicates are ignored
    """
    insert_query = INSERT_SPORTS
    logging.info(f"Writing into {connection.database} - sports without overwriting. Sample: {sports[0]}")
    insert_many_rows(connection=connection, query=insert_query, data=sports)


def get_list_of_sports_from_db(connection: mysql.connector.MySQLConnection) -> list[str]:
    select_query = GET_SPORTS_KEYS
    logging.info('Getting list of sports keys')
    res = get_many_rows(connection=connection, query=select_query)
    return [i[0] for i in res]


def check_team_exists_in_db(connection: mysql.connector.MySQLConnection, team: str, sport: str) -> bool:
    select_query = GET_SINGLE_TEAM
    logging.debug(f'Check if {team} already exists in DB')
    count = get_count(connection=connection, query=select_query, data=(team, sport))
    return count > 0


def check_game_exists_in_db(connection: mysql.connector.MySQLConnection, game_info: dict) -> bool:
    select_query = CHECK_SINGLE_GAME_EXISTS
    logging.debug(f'Check if game already exists in DB')
    data = (
        game_info['home_team_id'], game_info['away_team_id'], game_info['start_time'], game_info['sport_key']
    )
    count = get_count(connection=connection, query=select_query, data=data)
    return count > 0


def get_game_id(connection: mysql.connector.MySQLConnection, game_info: dict) -> bool:
    select_query = GET_SINGLE_GAME_ID
    logging.debug(f'Get the ID of a single game w/ info: {game_info}')
    data = (
        game_info['home_team_id'], game_info['away_team_id'], game_info['start_time'], game_info['sport_key']
    )
    row = get_single_row(connection=connection, query=select_query, data=data)
    return row[0]


def insert_game_into_db_return_id(connection: mysql.connector.MySQLConnection, game_info: dict) -> int:
    insert_query = INSERT_SINGLE_GAME_RETURN_ID
    logging.debug(f'Inserting game into DB: {game_info}')
    data = (
        game_info['start_time'], game_info['sport_key'], game_info['home_team_id'], game_info['away_team_id']
    )
    row_id = insert_single_row_return_id(connection=connection, query=insert_query, data=data)
    return row_id  ## TODO - error and -1 handling here


def insert_team_into_db_return_id(connection: mysql.connector.MySQLConnection, team: str, sport: str) -> int:
    insert_query = INSERT_SINGLE_TEAM_RETURN_ID
    logging.info(f'Inserting team {team}')
    row_id = insert_single_row_return_id(connection=connection, query=insert_query, data=(team, sport))
    return row_id  ## TODO - error and -1 handling here


def insert_site_into_db_return_id(connection: mysql.connector.MySQLConnection, site_name: str, friendly_name: str) -> int:
    insert_query = INSERT_SITE_RETURN_ID
    logging.info(f'Inserting site {site_name}')
    row_id = insert_single_row_return_id(connection=connection, query=insert_query, data=(site_name, friendly_name))
    return row_id  ## TODO - error and -1 handling here


def get_single_team_id(connection: mysql.connector.MySQLConnection, team: str, sport: str) -> int:
    select_query = GET_SINGLE_TEAM_ID
    logging.debug(f'Get {team} ID from DB')
    row = get_single_row(connection=connection, query=select_query, data=(team, sport))
    return row[0]


def get_site_id(connection: mysql.connector.MySQLConnection, site_name: str) -> int:
    select_query = GET_SINGLE_SITE_ID
    logging.debug(f'Get {site_name} ID from DB')
    row = get_single_row(connection=connection, query=select_query, data=(site_name,))
    return row[0]


def check_site_exists_in_db(connection: mysql.connector.MySQLConnection, site_name: str) -> bool:
    select_query = CHECK_SITE_EXISTS
    logging.debug(f'Check if site {site_name} already exists in DB')
    count = get_count(connection=connection, query=select_query, data=(site_name,))
    return count > 0


def insert_h2h_odds(connection: mysql.connector.MySQLConnection, data: tuple) -> int:
    insert_query = INSERT_H2H_ODDS_ROW_RETURN_ID
    logging.info(f'Inserting odds for game {data[0]}: {data[3]}, {data[4]}')
    row_id = insert_single_row_return_id(connection=connection, query=insert_query, data=data)
    return row_id  ## TODO - error and -1 handling here
