from json import loads as json_loads
from pprint import pprint
from datetime import datetime

import mysql.connector
import requests

from credentials.credentials import get_odds_api_key
from db.sports_odds_model import insert_sports, check_team_exists_in_db, insert_team_into_db_return_id, \
    get_single_team_id, check_game_exists_in_db, get_game_id, insert_game_into_db_return_id, check_site_exists_in_db, \
    get_site_id, insert_site_into_db_return_id, insert_h2h_odds, insert_totals_odds

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


def create_list_of_sports(conn: mysql.connector.MySQLConnection) -> list:
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
    return formatted_data


def _get_all_odds_for_sport(sport: str, market: str) -> list:
    p = {
        'sport': sport,
        'region': REGION,
        'market': market,
        'oddsFormat': ODDS_FORMAT
    }
    return _make_odds_api_get_request(function='odds', params=p)


def _insert_site_data(conn: mysql.connector.MySQLConnection, site: str, friendly_name: str) -> int:
    site_id = None
    if not check_site_exists_in_db(connection=conn, site_name=site):
        site_id = insert_site_into_db_return_id(connection=conn, site_name=site, friendly_name=friendly_name)
    if not site_id:
        site_id = get_site_id(connection=conn, site_name=site)
    return site_id


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


def _team_insertion_wrapper(odds_info: dict, conn: mysql.connector.MySQLConnection, sport: str) -> tuple:
    teams = odds_info.get('teams', [])
    home_team = odds_info.get('home_team', 'Unknown Team')
    teams.remove(home_team)
    away_team = teams.pop(0)
    return _get_team_ids(conn=conn, home_team=home_team, away_team=away_team, sport=sport)


def _insert_game(conn: mysql.connector.MySQLConnection, home_team_id: int, away_team_id: int, start_time: float, sport: str) -> int:
    start_datetime = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
    game_dict = {
        'home_team_id': home_team_id,
        'away_team_id': away_team_id,
        'start_time': start_datetime,
        'sport_key': sport
    }
    if check_game_exists_in_db(connection=conn, game_info=game_dict):
        return get_game_id(connection=conn, game_info=game_dict)
    return insert_game_into_db_return_id(connection=conn, game_info=game_dict)


def _insert_individual_h2h_odds_data(conn: mysql.connector.MySQLConnection, game_id: int, site_id: int, home_odds: int, away_odds: int) -> int:
    collected_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = (game_id, collected_datetime, site_id, home_odds, away_odds)
    odds_id = insert_h2h_odds(connection=conn, data=data)
    return odds_id


def _insert_individual_totals_odds_data(conn: mysql.connector.MySQLConnection, game_id: int, site_id: int, total: float, over_odds: int, under_odds: int) -> int:
    collected_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = (game_id, collected_datetime, site_id, total, over_odds, under_odds)
    odds_id = insert_totals_odds(connection=conn, data=data)
    return odds_id


def insert_h2h_data(conn: mysql.connector.MySQLConnection, sport: str):
    api_data = _get_all_odds_for_sport(sport=sport, market='h2h')
    for odd in api_data:
        site_count = odd.get('sites_count', 0)
        if site_count == 0:
            continue
        home_team_id, away_team_id = _team_insertion_wrapper(odds_info=odd, conn=conn, sport=sport)
        commence_time = float(odd.get('commence_time', 0))
        game_id = _insert_game(conn=conn, home_team_id=home_team_id, away_team_id=away_team_id,
                               start_time=commence_time, sport=sport)
        sites = odd.get('sites', [])
        for site in sites:
            site_name = site.get('site_key', 'Unknown Odds Provider')
            site_friendly_name = site.get('site_nice', 'Unknown Odds Provider friendly name')
            site_id = _insert_site_data(conn=conn, site=site_name, friendly_name=site_friendly_name)
            h2h_odds = site.get('odds', {}).get('h2h', [])
            home_h2h_odds = h2h_odds[0]
            away_h2h_odds = h2h_odds[1]
            _insert_individual_h2h_odds_data(conn=conn, game_id=game_id, site_id=site_id, home_odds=home_h2h_odds, away_odds=away_h2h_odds)


def insert_totals_data(conn: mysql.connector.MySQLConnection, sport: str):
    api_data = _get_all_odds_for_sport(sport=sport, market='totals')
    print(api_data)
    for odd in api_data:
        site_count = odd.get('sites_count', 0)
        if site_count == 0:
            continue
        home_team_id, away_team_id = _team_insertion_wrapper(odds_info=odd, conn=conn, sport=sport)
        commence_time = float(odd.get('commence_time', 0))
        game_id = _insert_game(conn=conn, home_team_id=home_team_id, away_team_id=away_team_id,
                               start_time=commence_time, sport=sport)
        sites = odd.get('sites', [])
        for site in sites:
            site_name = site.get('site_key', 'Unknown Odds Provider')
            site_friendly_name = site.get('site_nice', 'Unknown Odds Provider friendly name')
            site_id = _insert_site_data(conn=conn, site=site_name, friendly_name=site_friendly_name)
            totals_odds = site.get('odds', {}).get('totals', {})
            points = float(totals_odds.get('points')[0])
            position = totals_odds.get('position')
            over_position = position.index('over')
            under_position = position.index('under')
            over_odds = totals_odds.get('odds')[over_position]
            under_odds = totals_odds.get('odds')[under_position]
            _insert_individual_totals_odds_data(conn=conn, game_id=game_id, site_id=site_id, total=points, over_odds=over_odds, under_odds=under_odds)


def insert_spreads_data(conn: mysql.connector.MySQLConnection, sport: str):
    api_data = _get_all_odds_for_sport(sport=sport, market='spreads')
    print(api_data)
    for odd in api_data:
        site_count = odd.get('sites_count', 0)
        if site_count == 0:
            continue
        # pprint(odd)
        # home_team_id, away_team_id = _team_insertion_wrapper(odds_info=odd, conn=conn, sport=sport)
        # commence_time = float(odd.get('commence_time', 0))
        # game_id = _insert_game(conn=conn, home_team_id=home_team_id, away_team_id=away_team_id,
        #                        start_time=commence_time, sport=sport)
        # sites = odd.get('sites', [])
        # for site in sites:
        #     site_name = site.get('site_key', 'Unknown Odds Provider')
        #     site_friendly_name = site.get('site_nice', 'Unknown Odds Provider friendly name')
        #     site_id = _insert_site_data(conn=conn, site=site_name, friendly_name=site_friendly_name)
        #     h2h_odds = site.get('odds', {}).get('h2h', [])
        #     home_h2h_odds = h2h_odds[0]
        #     away_h2h_odds = h2h_odds[1]
        #     _insert_individual_h2h_odds_data(conn=conn, game_id=game_id, site_id=site_id, home_odds=home_h2h_odds, away_odds=away_h2h_odds)