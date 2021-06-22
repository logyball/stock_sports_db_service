from json import loads as json_loads
from pprint import pprint

import requests

from credentials.credentials import get_odds_api_key

ODDS_API_BASE_URL_V3 = 'https://api.the-odds-api.com/v3/'


def _make_odds_api_get_request(function: str, params: dict):
    api_url = ''.join([ODDS_API_BASE_URL_V3, function])
    params['apiKey'] = get_odds_api_key()
    res = requests.get(api_url, params=params)
    res_json = json_loads(res.text)
    if not bool(res_json.get('success', False)):
        print('do some error condition')
    return res_json.get('data', [])


def get_sports_list():
    data = _make_odds_api_get_request(function='sports')
    pprint(data)


def get_sports_odds():
    p = {
        'sport': 'basketball_nba',
        'region': 'us',
        'market': 'totals',
        'oddsFormat': 'american'
    }
    data = _make_odds_api_get_request(function='odds', params=p)
    pprint(data)