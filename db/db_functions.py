import logging

import mysql.connector
from mysql.connector import connect, Error
from credentials.credentials import get_db_credentials


def insert_many_rows(connection: mysql.connector.MySQLConnection, query: str, data: list) -> None:
    with connection.cursor() as cursor:
        cursor.executemany(query, data)
        try:
            connection.commit()
            logging.info(f'query {query} executed successfully')
        except mysql.connector.errors.Error as e:
            logging.fatal(f'query {query} broke: {e}')


def insert_single_row(connection: mysql.connector.MySQLConnection, query: str, data: list) -> None:
    with connection.cursor() as cursor:
        cursor.execute(query, data)
        try:
            connection.commit()
            logging.info(f'query {query} executed successfully')
        except mysql.connector.errors.Error as e:
            logging.fatal(f'query {query} broke: {e}')


def get_many_rows(connection: mysql.connector.MySQLConnection, query: str) -> list[tuple]:
    data = []
    with connection.cursor() as cursor:
        cursor.execute(query)
        try:
            data = [row for row in cursor.fetchall()]
        except mysql.connector.errors.Error as e:
            logging.fatal(f'query {query} broke: {e}')
    return data


def get_database_connection(verbose: bool = False) -> mysql.connector.MySQLConnection:
    creds = get_db_credentials()
    try:
        c = connect(
            host=creds.get('db_host'),
            user=creds.get('db_user'),
            password=creds.get('db_pass'),
            database=creds.get('db_name'),
            port=creds.get('db_port')
        )
        if verbose:
            c.cmd_debug()
        logging.info(f'obtained db connection to {c.database}')
        return c
    except Error as e:
        logging.fatal(f'couldnt establish database connection: {e}')
