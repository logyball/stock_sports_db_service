from json import loads as json_loads
from pprint import pprint

import mysql.connector
import requests

from credentials.credentials import get_odds_api_key
from db.sports_odds_model import insert_sports, check_team_exists_in_db, insert_team_into_db_return_id, get_single_team_id

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


def _insert_site_data(site: str) -> str:
    ## TODO - insert into DB if not existsing, otherwise
    ##        return key
    return ''


def _get_team_ids(conn: mysql.connector.MySQLConnection, home_team: str, away_team: str, sport: str) -> tuple:
    home_team_id, away_team_id = False, False
    if not check_team_exists_in_db(connection=conn, team=home_team, sport=sport):
        home_team_id = insert_team_into_db_return_id(connection=conn, team=home_team, sport=sport)
    if not check_team_exists_in_db(connection=conn, team=away_team, sport=sport):
        away_team_id = insert_team_into_db_return_id(connection=conn, team=away_team, sport=sport)
    if not home_team_id:
        home_team_id = get_single_team_id(connection=conn, team=home_team, sport=sport)
    if not away_team_id:
        away_team_id = get_single_team_id(connection=conn, team=away_team, sport=sport)
    return home_team_id, away_team_id


def insert_h2h_data(sport: str, market: str):
    api_data = _get_all_odds_for_sport(sport=sport, market=market)
    for odd in api_data:
        site_count = odd.get('sites_count', 0)
        if site_count == 0:
            continue
        teams = odd.get['teams', []]
        home_team = odd.get('home_team', 'Unknown Team')
        teams.remove(home_team)
        away_team = teams.pop(0)
        ## TODO - create entry for teams if not exist
        commence_time = odd.get('commence_time', 0)
        sites = odd.get('sites', [])
        ## TODO - create entry for game in DB
        for site in sites:
            site_name = site.get('site_key', 'Unknown Odds Provider')
            site_key = _insert_site_data(site=site_name)
            h2h_odds = site.get('odds', {}).get('h2h', [])
            home_h2h_odds = h2h_odds[0]
            away_h2h_odds = h2h_odds[1]
            ## TODO - insert into game + odds
            pass
        ## TODO - insert the data about the game
