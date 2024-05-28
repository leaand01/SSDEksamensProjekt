import os

from dotenv import load_dotenv


load_dotenv()

google_sso = {"client_id": os.environ.get('client_id', None),
              "client_secret": os.environ.get('client_secret', None),
              "redirect_uri": "https://127.0.0.1:8000/auth",
              "scope": ['email', 'openid'],
              "allow_insecure_http": True,
              "use_state": True,
              }

secret_key_for_signing_session_cookie = os.environ.get('secret_key_for_signing_session_cookie')
slow_api_rate_limit = '5/second'

postgresql_db_url = os.environ.get('postgresql_db_url')

secret_key_for_encryption = os.environ.get('secret_key_for_encrypton')
list_access_levels = ['read_only', 'write']
