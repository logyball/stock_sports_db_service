import mysql.connector
from db.db_queries import INSERT_TICKERS_IGNORE_DUPLICATES, GET_STOCK_TICKERS
from db.db_functions import insert_many_rows, get_many_rows

import logging


def load_tickers_into_db(connection: mysql.connector.MySQLConnection, ticker_list: list) -> None:
    """
    Using INSERT_TICKERS_IGNORE_DUPLICATES query, insert the stock tickers.  Don't error out on duplicates.
    """
    ticker_insert_query = INSERT_TICKERS_IGNORE_DUPLICATES
    logging.info("loading ticker_list into stock_tickers")
    insert_many_rows(connection=connection, query=ticker_insert_query, data=ticker_list)


def get_stock_tickers_from_db(connection: mysql.connector.MySQLConnection) -> list[str]:
    """Return the list of stock tickers present in the db"""
    get_ticker_query = GET_STOCK_TICKERS
    tickers = get_many_rows(connection=connection, query=get_ticker_query)
    return [t[0] for t in tickers]
