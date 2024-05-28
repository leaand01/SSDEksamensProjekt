**SSDEksamensProjekt**


**How to run**

The project is coded in python. Use e.g. PyCharm.

To run this project:
1. create a venv and cd to the root folder of the project. Install required packages by running command: pip install -r requirements.txt
2. Setup PostGreSQL database:
    a. Install PostgreSQL on your machine
    b. Create a database, e.g. using pgAdmin
    c. Import the SQL dump file SSDEksamensProjekt-DB_dump.sql into the created database in b. This is done by running the command: psql -U postgres -d your_database_name -f SSDEksamensProjekt_DB_dump.sql
3. Run app by running command: python main.py
4. Database info when running app: 2 users have been created in the database: nobody@gmail.com and noone@gmail. For the purpose of playing around with sharing calculations.


**Remarks**
The .env file has been shared on Github, for easy setup and as this is a test project. Normally .env containing confidential information should never be committed.


**PostGreSQL database connection information used**

password: PostgreSQL_mySecretPassword

port number the server should listen on:
port: 5432



