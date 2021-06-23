import mysql.connector
from db.db_queries import INSERT_SPORTS, GET_SPORTS_KEYS, GET_SINGLE_TEAM, INSERT_SINGLE_TEAM_RETURN_ID, GET_SINGLE_TEAM_ID
from db.db_functions import insert_many_rows, get_many_rows, get_count, insert_single_row_return_id, get_single_row

import logging


def insert_sports(connection: mysql.connector.MySQLConnection, sports: list[tuple]) -> None:
    """
    Using INSERT_SPORTS query, insert rows into the stock_sports.sports
    If a duplicate row is found, a Primary Key error is raised.
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


def insert_team_into_db_return_id(connection: mysql.connector.MySQLConnection, team: str, sport: str) -> int:
    insert_query = INSERT_SINGLE_TEAM_RETURN_ID
    logging.info(f'Inserting team {team}')
    row_id = insert_single_row_return_id(connection=connection, query=insert_query, data=(team, sport))
    return row_id  ## TODO - error and -1 handling here


def get_single_team_id(connection: mysql.connector.MySQLConnection, team: str, sport: str) -> int:
    select_query = GET_SINGLE_TEAM_ID
    logging.debug(f'Get {team} ID from DB')
    row = get_single_row(connection=connection, query=select_query, data=(team, sport))
    return row[0]
