import datetime
import logging
import math
from time import sleep

import mysql.connector
import requests

from credentials.credentials import get_alpha_vantage_key
from db.stock_prices_model import insert_many_stock_prices_no_ignore, insert_many_stock_prices


def get_previous_market_days_date() -> datetime:
    """
    Get the previous day the stock market was open.
    If monday or sunday, return Friday, otherwise return previous day
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


def get_individual_symbol_historical_data_raw_api(symbol: str) -> list[tuple]:
    data_list = []
    logging.info(f'getting data from av api for {symbol}')
    api_key = get_alpha_vantage_key()
    api_str = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}"
    res = requests.get(api_str)
    res_d = res.json()
    if res.status_code > 299:
        logging.error(f'error retrieving {symbol} from AV API')
        logging.error(f'response code was {res.status_code}: {res.json()}')
        return []
    for date_str, info in res_d.get("Time Series (Daily)", {}).items():
        data_list.append((
            symbol,
            date_str,
            info.get('3. low'),
            info.get('2. high')
        ))
    if data_list:
        logging.info(f'retrieved historical data from {symbol} -> sample: {data_list[0]}')
    return data_list


def get_prev_market_day_stock_data_individual_raw_api(symbol: str, prev_day: datetime) -> tuple:
    api_key = get_alpha_vantage_key()
    api_str = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=60min&outputsize=compact&apikey={api_key}'
    res = requests.get(api_str)
    res_d = res.json()
    if res.status_code > 299:
        logging.error(f'error retrieving {symbol} from AV API')
        logging.error(f'response code was {res.status_code}: {res.json()}')
        return ()
    global_high = -1
    global_low = math.inf
    for dt, values in res_d.get('Time Series (60min)', {}).items():
        i_date = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        if i_date.date() == prev_day.date():
            global_high = max(global_high, float(values.get('2. high', -1)))
            global_low = min(global_low, float(values.get('3. low', math.inf)))
    logging.info(f'Retrieved daily stock: {symbol}, hi: {global_high}, low: {global_low}')
    return (
        symbol,
        prev_day.date(),
        global_low,
        global_high
    )


def historical_stock_data_batch(connection: mysql.connector.MySQLConnection, symbol_list: list[str]):
    data = []
    rate_limiter_counter = 5
    for s in symbol_list:
        data.extend(get_individual_symbol_historical_data_raw_api(symbol=s))
        rate_limiter_counter -= 1
        if rate_limiter_counter == 0:
            rate_limiter_counter = 5
            insert_many_stock_prices_no_ignore(connection=connection, stock_prices=data)
            logging.info('retrieved and inserted 5 records, sleeping for 120 seconds to avoid AV rate limitation')
            data = []
            sleep(120)


def yesterdays_stock_data_batch(connection: mysql.connector.MySQLConnection, symbol_list: list[str]):
    data = []
    prev_day = get_previous_market_days_date()
    rate_limiter_counter = 5
    for s in symbol_list:
        data.append(get_prev_market_day_stock_data_individual_raw_api(symbol=s, prev_day=prev_day))
        rate_limiter_counter -= 1
        if rate_limiter_counter == 0:
            rate_limiter_counter = 5
            insert_many_stock_prices(connection=connection, stock_prices=data)
            logging.info('retrieved and inserted 5 records, sleeping for 120 seconds to avoid AV rate limitation')
            data = []
            sleep(120)
