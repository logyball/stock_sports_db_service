from json import loads as json_loads
from pprint import pprint

import mysql.connector
import requests

from credentials.credentials import get_odds_api_key
from db.sports_odds_model import insert_sports

ODDS_API_BASE_URL_V3 = 'https://api.the-odds-api.com/v3/'
REGION = 'us'
ODDS_FORMAT = 'american'


def _make_odds_api_get_request(function: str, params: dict) -> list:
    api_url = ''.join([ODDS_API_BASE_URL_V3, function])
    params['apiKey'] = get_odds_api_key()
    res = requests.get(api_url, params=params)
    res_json = json_loads(res.text)
    if not bool(res_json.get('success', False)):
        print('do some error condition')
    return res_json.get('data', [])


def create_list_of_sports(conn: mysql.connector.MySQLConnection) -> None:
    data = _make_odds_api_get_request(function='sports', params={})
    formatted_data = []
    for data_dict in data:
        formatted_data.append((
            data_dict.get('key', 'Unknown Sport'),
            data_dict.get('details', 'Unknown Friendly Name'),
            data_dict.get('title', 'Unknown League Title'),
            data_dict.get('group', 'Unknown Group'),
        ))
    insert_sports(connection=conn, sports=formatted_data)


def _get_all_odds_for_sport(sport: str, market: str) -> list:
    p = {
        'sport': sport,
        'region': REGION,
        'market': market,
        'oddsFormat': ODDS_FORMAT
    }
    return _make_odds_api_get_request(function='odds', params=p)
