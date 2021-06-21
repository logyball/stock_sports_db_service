import logging

from yaml import load, Loader
from os import environ


def get_alpha_vantage_key() -> str:
    """
    Return the AV API Key.  Set LOCAL=true in the environment variables to use credentials.yml.  Otherwise,
    reads the credentials from ALPHA_VANTAGE_API_KEY environment var.
    """
    if environ.get('LOCAL', False):
        key = load(open('credentials/credentials.yml', 'r'), Loader=Loader).get('alpha_vantage', False)
    else:
        key = environ.get('ALPHA_VANTAGE_API_KEY', False)
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
