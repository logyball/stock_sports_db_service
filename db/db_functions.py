import logging

import mysql.connector
from mysql.connector import connect, Error
from credentials.credentials import get_db_credentials


def insert_many_rows(connection: mysql.connector.MySQLConnection, query: str, data: list) -> None:
    """Wrapper for MySQL to insert lots of rows to a table using a passed-in query"""
    with connection.cursor() as cursor:
        cursor.executemany(query, data)
        try:
            connection.commit()
            logging.info(f'query {query} executed successfully')
        except mysql.connector.errors.Error as e:
            logging.fatal(f'query {query} broke: {e}')


def insert_single_row(connection: mysql.connector.MySQLConnection, query: str, data: list) -> None:
    """Wrapper for MySQL to insert a single row to a table using a passed-in query"""
    with connection.cursor() as cursor:
        cursor.execute(query, data)
        try:
            connection.commit()
            logging.info(f'query {query} executed successfully')
        except mysql.connector.errors.Error as e:
            logging.fatal(f'query {query} broke: {e}')


def insert_single_row_return_id(connection: mysql.connector.MySQLConnection, query: str, data: tuple) -> int:
    """Wrapper for MySQL to insert a single row to a table using a passed-in query"""
    row_id = -1
    with connection.cursor() as cursor:
        cursor.execute(query, data)
        try:
            connection.commit()
            row_id = cursor.lastrowid
            logging.info(f'query {query} executed successfully')
        except mysql.connector.errors.Error as e:
            logging.fatal(f'query {query} broke: {e}')
    return row_id


def get_many_rows(connection: mysql.connector.MySQLConnection, query: str) -> list[tuple]:
    """Wrapper for MySQL to grab more than one row from a table using a passed-in query"""
    data = []
    with connection.cursor() as cursor:
        cursor.execute(query)
        try:
            data = [row for row in cursor.fetchall()]
        except mysql.connector.errors.Error as e:
            logging.fatal(f'query {query} broke: {e}')
    return data


def get_single_row(connection: mysql.connector.MySQLConnection, query: str, data: tuple) -> tuple:
    """Wrapper for MySQL to grab more than one row from a table using a passed-in query"""
    with connection.cursor() as cursor:
        cursor.execute(query, data)
        try:
            row = cursor.fetchone()
        except mysql.connector.errors.Error as e:
            logging.fatal(f'query {query} broke: {e}')
    return row


def get_count(connection: mysql.connector.MySQLConnection, query: str, data: tuple) -> int:
    """Wrapper for MySQL to return the count of a query"""
    with connection.cursor() as cursor:
        cursor.execute(query, data)
        try:
            count_tup = cursor.fetchone()
        except mysql.connector.errors.Error as e:
            logging.fatal(f'query {query} broke: {e}')
    count = count_tup[0]
    return count


def get_database_connection(verbose: bool = False) -> mysql.connector.MySQLConnection:
    """Wrapper for MySQL to get a db connection using credentials helpers"""
    db_credentials = get_db_credentials()
    try:
        c = connect(
            host=db_credentials.get('db_host'),
            user=db_credentials.get('db_user'),
            password=db_credentials.get('db_pass'),
            database=db_credentials.get('db_name'),
            port=db_credentials.get('db_port')
        )
        if verbose:
            c.cmd_debug()
        logging.info(f'obtained db connection to {c.database}')
        return c
    except Error as e:
        logging.fatal(f'could not establish database connection: {e}')
