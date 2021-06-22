import sys
import argparse
import logging

from mysql.connector import MySQLConnection
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

from db.db_functions import get_database_connection
from db.stock_ticker_model import load_tickers_into_db, get_stock_tickers_from_db
from db.sports_odds_model import get_list_of_sports_from_db
from stocks.stock_prices import historical_stock_data_batch, yesterdays_stock_data_batch
from stocks.stonk_tickers import get_tickers

from odds.sports_odds import create_list_of_sports


def init_setup() -> tuple:
    """
    Collect arguments from the command line, initialize prometheus registry if applicable
    :return: (args object, prometheus registry)
    """
    p_reg = None
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
    if args.production:
        p_reg = CollectorRegistry()
    return args, p_reg


def log_gauge_to_prometheus(prom_gauge: Gauge, prometheus_registry: CollectorRegistry) -> None:
    """
    Wrapper to send a gauge to a Prometheus PushGateway
    :param prom_gauge: the gauge to send
    :param prometheus_registry: the registry to send to
    """
    prom_gauge.set_to_current_time()
    try:
        push_to_gateway('prometheus-pushgateway.monitoring:9091', job='stocks_job',
                        registry=prometheus_registry)
    except Exception as e:
        logging.error(f'error pushing gauge {prom_gauge} to prometheus.\n{e}')


def run_ticker_population(prometheus_registry: CollectorRegistry, connection: MySQLConnection, prod: bool, ) -> None:
    """Wrapper to populate the DB with stock tickers"""
    gauge = Gauge('stock_tickers_last_successful_run', 'Last the stock ticker symbols were successfully inserted into '
                                                   'the db', registry=prometheus_registry)
    logging.info('getting stock tickers')
    ticker_list = get_tickers()
    load_tickers_into_db(connection=connection, ticker_list=ticker_list)
    logging.info('successfully finished stock ticker population')
    if prod:
        logging.info('Logging to prometheus - successfully populated stock tickers')
        log_gauge_to_prometheus(prom_gauge=gauge, prometheus_registry=prometheus_registry)


def run_back_population(prometheus_registry: CollectorRegistry, connection: MySQLConnection, prod: bool) -> None:
    """Wrapper to back populate the DB with historical stock data"""
    gauge = Gauge('stock_back_population_last_successful_run',
              'Last the stock back population job was run successfully', registry=prometheus_registry)
    logging.info('running back population')
    symbol_list = get_stock_tickers_from_db(connection=connection)
    historical_stock_data_batch(connection=connection, symbol_list=symbol_list)
    logging.info('successfully finished back population')
    if prod:
        logging.info('Logging to prometheus - successful back population')
        log_gauge_to_prometheus(prom_gauge=gauge, prometheus_registry=prometheus_registry)


def run_daily_population(prometheus_registry: CollectorRegistry, connection: MySQLConnection, prod: bool) -> None:
    """Wrapper to populate the DB with daily stock data"""
    gauge = Gauge('stock_daily_last_successful_run',
              'Last the stock daily job was run successfully', registry=prometheus_registry)
    logging.info('run daily population')
    symbol_list = get_stock_tickers_from_db(connection=connection)
    yesterdays_stock_data_batch(connection=connection, symbol_list=symbol_list)
    logging.info('successfully finished daily population')
    if prod:
        logging.info('Logging to prometheus - successfully populated daily batch job')
        log_gauge_to_prometheus(prom_gauge=gauge, prometheus_registry=prometheus_registry)


def main() -> None:
    args, p_registry = init_setup()
    conn = get_database_connection(verbose=args.verbose)
    # create_list_of_sports(conn=conn)
    print(get_list_of_sports_from_db(connection=conn))
    # if not conn:
    #     sys.exit(1)
    # if args.tickers:
    #     run_ticker_population(prod=args.production, prometheus_registry=p_registry, connection=conn)
    # if args.back_populate:
    #     run_back_population(prod=args.production, prometheus_registry=p_registry, connection=conn)
    # if args.daily:
    #     run_daily_population(prod=args.production, prometheus_registry=p_registry, connection=conn)


if __name__ == '__main__':
    main()
