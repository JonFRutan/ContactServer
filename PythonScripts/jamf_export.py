#jfr
import os, requests
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')

DB = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASS,
    "host": DB_HOST
}

# jamf payloads can accept the following fields:
# Field Name:                      Required:
# Account Description              No
# Hostname                         Yes
# Port                             Yes
# Principal URL                    No
# Account User Name                Yes
# Account Password                 No
# Use SSL                          No
# Communication Service Rules      No
#Note that payload variables may be applied in the literal payload as such:
# %Username%@domain.com
