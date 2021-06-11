import mysql.connector
from db.db_queries import INSERT_STOCK_PRICE_ROWS, INSERT_STOCK_PRICE_ROWS_IGNORE_DUPLICATES
from db.db_functions import insert_many_rows

import logging


def insert_many_stock_prices_no_ignore(connection: mysql.connector.MySQLConnection, stock_prices: list[tuple]) -> None:
    insert_no_overwrite_query = INSERT_STOCK_PRICE_ROWS
    logging.info(f"Writing into {connection.database} - stock_prices without overwriting. Sample: {stock_prices[0]}")
    insert_many_rows(connection=connection, query=insert_no_overwrite_query, data=stock_prices)


def insert_many_stock_prices(connection: mysql.connector.MySQLConnection, stock_prices: list[tuple]) -> None:
    insert_query = INSERT_STOCK_PRICE_ROWS_IGNORE_DUPLICATES
    logging.info(f"Writing into {connection.database} - stock_prices, ignoring duplicates. Sample: {stock_prices[0]}")
    insert_many_rows(connection=connection, query=insert_query, data=stock_prices)
