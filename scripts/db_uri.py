"""Print a percent-encoded Postgres connection URI for PostgREST (loads .env)."""
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()
user = os.getenv("POSTGRES_USER") or ""
password = os.getenv("POSTGRES_PASSWORD") or ""
host = os.getenv("POSTGRES_HOST", "pgdb")
port = os.getenv("POSTGRES_PORT", "5432")
db = os.getenv("POSTGRES_DB", "postgres")

uri = f"postgres://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{db}"
print(uri)
