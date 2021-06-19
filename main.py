import sys
import argparse
import logging

from db.db_functions import get_database_connection
from db.stock_ticker_model import load_tickers_into_db, get_stock_tickers_from_db
from stocks.stock_prices import historical_stock_data_batch, yesterdays_stock_data_batch
from stocks.stonk_tickers import get_tickers


def init_setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='increase output verbosity',
                        action='store_true')
    parser.add_argument('-t', '--tickers', help='insert stock tickers',
                        action='store_true')
    parser.add_argument('-b', '--back-populate', help='run the back-population script',
                        action='store_true')
    parser.add_argument('-d', '--daily', help='run the daily script of the NASDAQ 100',
                        action='store_true')
    parser.add_argument('-p', '--production', help='Run in full mode, e.g. send metrics to prometheus',
                        action='store_true')
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(
            format='%(asctime)s [%(levelname)6s] | %(filename)25s:%(lineno)3s -- %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.DEBUG
        )
        logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
    else:
        logging.basicConfig(
            format='%(asctime)s [%(levelname)6s] | %(filename)25s:%(lineno)3s -- %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.INFO
        )
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    return args


def main():
    args = init_setup()
    connection = get_database_connection(verbose=True)
    if not connection:
        sys.exit(1)
    if args.tickers:
        logging.info('getting stock tickers')
        ticker_list = get_tickers()
        load_tickers_into_db(connection=connection, ticker_list=ticker_list)
    if args.back_populate:
        logging.info('running back population')
        symbol_list = get_stock_tickers_from_db(connection=connection)
        historical_stock_data_batch(connection=connection, symbol_list=symbol_list)
    if args.daily:
        logging.info('run daily population')
        symbol_list = get_stock_tickers_from_db(connection=connection)
        yesterdays_stock_data_batch(connection=connection, symbol_list=symbol_list)


if __name__ == '__main__':
    main()
