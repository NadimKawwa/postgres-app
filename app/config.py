import os 
from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv()

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = quote_plus(os.environ['POSTGRES_PASSWORD'])

DATABASE_URL=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:54320/postgres"
