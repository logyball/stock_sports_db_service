import logging
from json import loads


def get_tickers() -> list[tuple]:
    """
    Grab the stock tickers from associated nasdaq_100 JSON file
    :return: formatted list of stock ticker data
    """
    formatted_ticker_list = []
    with open("stocks/nasdaq_100.json", "r") as nasdaq_json:
        nasdaq = loads(nasdaq_json.read())
        tickers_list = nasdaq.get('corporations', [])
    for t in tickers_list:
        formatted_ticker_list.append((
            t.get('symbol', ''),
            t.get('name', ''),
            t.get('exchange', 'NASDAQ')
        ))
    logging.info("obtained formatted ticker list from json")
    return formatted_ticker_list
