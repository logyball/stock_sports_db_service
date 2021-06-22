import mysql.connector
from db.db_queries import INSERT_SPORTS, GET_SPORTS_KEYS
from db.db_functions import insert_many_rows, get_many_rows

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


