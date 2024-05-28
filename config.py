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



"""
Eksportere din PostgreSQL-database til en SQL-fil:
køre følgende kommando i terminal: 
pg_dump -U postgres -d SSDEksamensProjekt_DB -F p -f SSDEksamensProjekt_DB_dump.sql

hvor postgres er username SSDEksamensProjekt_DB er database name og SSDEksamensProjekt_DB_dump.sql er navnet på dumpede fil
password er PostgreSQL_mySecretPassword



pg_dump -U username -d dbname -F p -f filename.sql
pg_dump -U postgres -d SSDEksamensProjekt_DB -F p -f SSDEksamensProjekt_DB_dump.sql


Genoprette databasen fra SQL-filen:
psql -U username -d dbname -f filename.sql
psql -U postgres -d SSDEksamensProjekt_DB -f SSDEksamensProjekt_DB_dump.sql



postgresql_db_url="postgresql://postgres:PostgreSQL_mySecretPassword@localhost:5432/SSDEksamensProjekt_DB"


"""


"""
TLS certificate


Obtaining Certificates:

Let's Encrypt: Let's Encrypt provides an automated mechanism called ACME (Automatic Certificate Management Environment)
for obtaining SSL/TLS certificates. You can use ACME clients like Certbot or acme.sh to request and renew certificates automatically.
Self-signed Certificates: For development purposes, you can generate self-signed certificates using tools like OpenSSL.
Self-signed certificates are not trusted by default and are mainly suitable for testing and development environments.


 1. har installer OpenSSl
 
 2. kør kommando : openssl genpkey -algorithm RSA -out server.key
 for a generere private key. This generates the file server.key in the current directory.
 
 3. generate a self-signed certificate using the private key:
 openssl req -new -x509 -days 365 -key server.key -out server.crt
 this generate the file server.crt in the current directory
 
 Run your FastAPI application with the self-signed SSL/TLS certificates using Uvicorn:

uvicorn app:app --host 127.0.0.1 --port 8000 --ssl-keyfile ./server.key --ssl-certfile ./server.crt --reload

  
"""