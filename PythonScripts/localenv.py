import os
from venv import load_dotenv

load_dotenv()
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')

RAD_URLS=os.getenv('RAD_URLS')
RAD_USER=os.getenv('RAD_USER')
RAD_PASS=os.getenv('RAD_PASS')
RAD_ADDR=os.getenv('RAD_ADDR')

DB = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASS,
    "host": DB_HOST
}

RAD = {
    "url": RAD_URLS,
    "user": RAD_USER,
    "passwod": RAD_PASS,
    "addressbook": RAD_ADDR 
}