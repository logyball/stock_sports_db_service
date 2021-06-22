import datetime
import logging
from time import sleep

import mysql.connector
import requests

from credentials.credentials import get_alpha_vantage_key
from db.stock_prices_model import insert_many_stock_prices_no_ignore, insert_many_stock_prices

AV_BASE_URL = "https://www.alphavantage.co/query?function"
SEARCH_SLEEP_TIME = 150


def _get_previous_market_days_date() -> datetime:
    """
    Get the previous day the stock market was open.
    If monday or sunday, return Friday, otherwise return previous day.

    Not to be called outside this module.
    """
    now = datetime.datetime.today()
    day_of_week = now.weekday()
    if 1 <= day_of_week <= 5:
        timedelta_days = 1
    elif day_of_week == 6:
        timedelta_days = 2
    else:
        timedelta_days = 3
    prev_day = now - datetime.timedelta(days=timedelta_days)
    logging.info(f'retrieving date: {prev_day.date()}')
    return prev_day


def _make_av_api_get(api_function: str, symbol: str, output_size: str, interval: str = '') -> dict:
    """
    Make an HTTP GET request to AV API.  Trying to emulate the SDK, since it isn't cross platform :/
    https://www.alphavantage.co/documentation/

    Not to be called outside this module.

    :param api_function: the function to call - TIME_SERIES_DAILY or TIME_SERIES_INTRADAY
    :param symbol: The stock ticker to grab
    :param output_size: granularity - full or compact
    :param interval: (OPTIONAL) - 60min or 30min
    :return: The dictionary representation of the JSON response body
    """
    api_str_base = f'{AV_BASE_URL}={api_function}&symbol={symbol}&'
    if interval:
        api_str_base += f'interval={interval}&'
    api_str = ''.join([api_str_base, f'outputsize={output_size}&', 'apikey=', get_alpha_vantage_key()])
    res = requests.get(api_str)
    if res.status_code != 200:
        logging.error(f'error retrieving {symbol} from AV API')
        logging.error(f'response code was {res.status_code}: {res.json()}')
        return {}
    return res.json()


def _get_individual_symbol_historical_data(symbol: str) -> list[tuple]:
    """
    Private function to get time series data from AV API, translate to tuple, and return
    to calling function.

    Not to be called outside this module.
    """
    data_list = []
    logging.info(f'getting data from av api for {symbol}')
    res = _make_av_api_get(api_function='TIME_SERIES_DAILY', symbol=symbol, output_size='full')
    if not res:
        return []
    for date_str, info in res.get("Time Series (Daily)", {}).items():
        data_list.append((symbol, date_str, info.get('3. low'), info.get('2. high')))
    if data_list:
        logging.info(f'retrieved historical data from {symbol} -> sample: {data_list[0]}')
    return data_list


def _find_high_low_value(response_data: dict, prev_date: datetime.date) -> tuple:
    """
    Private function for get_stock_data_individual_date - find high and low value
    of the response data.

    Not to be called outside this module.
    """
    global_high = -1
    global_low = 10000000000  # outrageous price
    for dt, values in response_data.get('Time Series (60min)', {}).items():
        i_date = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        if i_date.date() == prev_date:
            global_high = max(global_high, float(values.get('2. high', -1)))
            global_low = min(global_low, float(values.get('3. low', 10000000000)))
    return global_high, global_low


def _get_stock_data_individual_date(symbol: str, date: datetime.date) -> tuple:
    """
    Return a single stocks' performance from a single market day

    Not to be called outside this module.
    :param symbol: Which stock to check
    :param date: the date to fetch
    :return: tuple(the symbol, the date fetched, low value from that day, high value from that day)
    """
    res = _make_av_api_get(api_function='TIME_SERIES_INTRADAY', symbol=symbol, output_size='compact',
                           interval='60min')
    if not res:
        return ()
    global_high, global_low = _find_high_low_value(response_data=res, prev_date=date)
    logging.info(f'Retrieved daily stock: {symbol}, hi: {global_high}, low: {global_low}')
    return symbol, date, global_low, global_high


def historical_stock_data_batch(connection: mysql.connector.MySQLConnection, symbol_list: list[str]):
    """
    Retrieve historical data for all stocks, insert into DB.
    Avoid AV rate limiter by running 5 queries every 2 minutes

    :param connection: MySQL DB connection
    :param symbol_list: List of stock tickers to grab
    :return: None
    """
    data = []
    i = 0
    for s in symbol_list:
        data.extend(_get_individual_symbol_historical_data(symbol=s))
        i += 1
        if i % 5 == 0:
            insert_many_stock_prices_no_ignore(connection=connection, stock_prices=data[i - 5:])
            logging.info('retrieved and inserted 5 records, sleeping for 120 seconds to avoid AV rate limitation')
            sleep(SEARCH_SLEEP_TIME)


def yesterdays_stock_data_batch(connection: mysql.connector.MySQLConnection, symbol_list: list[str]) -> None:
    """
    Retrieve the data from the stock market for yesterday, insert into DB.
    Avoid AV rate limiter by running 5 queries every 2 minutes

    :param connection: MySQL DB connection
    :param symbol_list: List of stock tickers to grab
    :return: None
    """
    data = []
    prev_date = _get_previous_market_days_date().date()
    i = 0
    for s in symbol_list:
        data.append(_get_stock_data_individual_date(symbol=s, date=prev_date))
        i += 1
        if i % 5 == 0:
            insert_many_stock_prices(connection=connection, stock_prices=data[i - 5:])
            logging.info('retrieved and inserted 5 records, sleeping for 120 seconds to avoid AV rate limitation')
            sleep(SEARCH_SLEEP_TIME)
