import logging

from yaml import load, Loader
from os import environ


def _get_key_helper(key: str, env_var: str) -> str:
    if environ.get('LOCAL', False):
        key = load(open('credentials/credentials.yml', 'r'), Loader=Loader).get(key, False)
    else:
        key = environ.get(env_var, False)
    return key


def get_odds_api_key() -> str:
    """
    Return the-Odds-API api Key.  Set LOCAL=true in the environment variables to use credentials.yml.  Otherwise,
    reads the credentials from ODDS_API_KEY environment var.
    """
    key = _get_key_helper(key='the_odds_api', env_var='ODDS_API_KEY')
    if not key:
        raise LookupError("couldn't find the odds api key")
    return key


def get_alpha_vantage_key() -> str:
    """
    Return the AV API Key.  Set LOCAL=true in the environment variables to use credentials.yml.  Otherwise,
    reads the credentials from ALPHA_VANTAGE_API_KEY environment var.
    """
    key = _get_key_helper(key='alpha_vantage', env_var='ALPHA_VANTAGE_API_KEY')
    if not key:
        raise LookupError("couldn't find alpha vantage key")
    return key


def get_db_credentials() -> dict:
    """
    Return the DB credentials.  Set LOCAL=true in the environment variables to use credentials.yml.  Otherwise,
    reads the credentials from DB_* environment var.
    Note DB_PORT is assumed to be 3306 and can be overridden, but is not required.

    :return: dictionary with database credential information
    """
    if environ.get('LOCAL', False):
        c = load(open('credentials/credentials.yml', 'r'), Loader=Loader)
        if not {'db_user', 'db_name', 'db_host', 'db_pass'}.issubset(set(c.keys())):
            raise KeyError('db key not found in credentials yaml. all must exist: db_user, db_name, db_host', 'db_pass')
        return {
            'db_user': c.get('db_user'),
            'db_name': c.get('db_name'),
            'db_host': c.get('db_host'),
            'db_pass': c.get('db_pass'),
            'db_port': c.get('db_port', 3306)
        }
    else:
        d = {
            'db_user': environ.get('DB_USER'),
            'db_name': environ.get('DB_NAME'),
            'db_host': environ.get('DB_HOST'),
            'db_pass': environ.get('DB_PASS'),
            'db_port': environ.get('DB_PORT', 3306)
        }
        if not all(d.values()):
            logging.error(f'not all database values found in environment.  Current values: {d}')
            raise KeyError('db key not found in env vars. all must exist: DB_USER, DB_NAME, DB_HOST, DB_PASS')
        return d
