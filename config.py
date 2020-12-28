import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_BOT = os.getenv('TOKEN_BOT')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
PGHOST = os.getenv('PGHOST')
PG_USER = os.getenv('PG_USER')
PG_PASS = os.getenv('POSTGRES_PASSWORD')
