import os
from dotenv import load_dotenv


class CredentialsUtility(object):

    DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\'))
    ENV_PATH = os.path.join(DATA_DIR, 'env.bat')
    load_dotenv(dotenv_path=ENV_PATH)

    def __init__(self):
        pass

    @staticmethod
    def get_wc_api_keys():
        wc_key = os.environ.get('WC_KEY')
        wc_secret = os.environ.get('WC_SECRET')

        if not wc_key or not wc_secret:
            raise Exception("The API credentials 'WC_KEY' and 'WC_SECRET' must be in env variable")
        else:
            return {'wc_key': wc_key, 'wc_secret': wc_secret}

    @staticmethod
    def get_db_credentials():
        db_user = os.environ.get('DB_USER')
        db_password = os.environ.get('DB_PASSWORD')

        if not db_user or not db_password:
            raise Exception("The DB credentials 'DB_USER' and 'DB_PASSWORD' must be in env variable")
        else:
            return {'db_user': db_user, 'db_password': db_password}

