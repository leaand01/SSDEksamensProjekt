**SSDEksamensProjekt**

Website for calculating the principal of arbitrary loans. The calculations can be saved for individual users and shared with other users. You can choose to share one or more calculations with individual users or all users.

Below you will find:

- instructions how to run application
- Remarks
- PostGreSQL database connection info
- Flowchart of application


**How to run**

The project is coded in python. Use e.g. PyCharm.

To run this project:
1. create a venv and cd to the root folder of the project. Install required packages by running command: pip install -r requirements.txt
2. Setup PostGreSQL database:
    a. Install PostgreSQL on your machine
    b. Create a database, e.g. using pgAdmin
    c. Import the SQL dump file SSDEksamensProjekt-DB_dump.sql into the created database in b. This is done by running the command: psql -U postgres -d your_database_name -f SSDEksamensProjekt_DB_dump.sql
3. Create a .env file at the root directory and insert values spedified further below (must be done before app can run).   
4. Run app by running command: python main.py
5. You must have gmail.com address in order to login to the app
6. Database info when running app: 2 users have been created in the database: nobody@gmail.com and noone@gmail. For the purpose of playing around with sharing calculations.



**Remarks**

- For https we have generated a self-signed TLS certificate using OpenSSL, as this is a test project. This should not be done for production code.
- Having created a .env file insert the following values (the following values are only shared since this is a test project. Normally - never share confidential information):

client_id=562611440208-79eir3dipi06jm0grqum1pb9girmu2vd.apps.googleusercontent.com
client_secret=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

secret_key_for_signing_session_cookie=PKomLcuf3Y4cN8q1ur7IDIu44DtkK5fanrjMwiGVOjg
secret_key_for_encrypton=ctmXNFrGJKuc5U2wDwGnGZR2bDeOFNpdgNs8wfDAFIw=

postgresql_db_url="postgresql://postgres:PostgreSQL_mySecretPassword@localhost:5432/SSDEksamensProjekt_DB"


**PostGreSQL database connection information used**

password: PostgreSQL_mySecretPassword

port number the server should listen on:
port: 5432


**Flowchart**

![Flowchart](FLowchart.drawio.png)





