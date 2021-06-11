from yaml import load, Loader
from os import environ


def get_alpha_vantage_key() -> str:
    if environ.get('LOCAL', False):
        key = load(open('credentials/credentials.yml', 'r'), Loader=Loader).get('alpha_vantage', False)
    else:
        key = environ.get('ALPHA_VANTAGE_API_KEY', False)
    if not key:
        raise LookupError("couldn't find alpha vantage key")
    return key


def get_db_credentials() -> dict:
    if environ.get('LOCAL', False):
        c = load(open('credentials/credentials.yml', 'r'), Loader=Loader)
        if not {'db_user', 'db_name', 'db_host', 'db_pass'}.issubset(set(c.keys())):  # Check if all required keys are present
            raise KeyError('db key not found in credentials yaml. all must exist: db_user, db_name, db_host', 'db_pass')
        return {
            'db_user': c.get('db_user'),
            'db_name': c.get('db_name'),
            'db_host': c.get('db_host'),
            'db_pass': c.get('db_pass'),
            'db_port': c.get('db_port')
        }
    else:
        d = {
            'db_user': environ.get('DB_USER'),
            'db_name': environ.get('DB_NAME'),
            'db_host': environ.get('DB_HOST'),
            'db_pass': environ.get('DB_PASS'),
            'db_port': environ.get('DB_PORT')
        }
        if not all(d.values()):
            raise KeyError('db key not found in env vars. all must exist: db_user, db_name, db_host, db_pass')
        return d
