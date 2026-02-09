#create extension and tables 

from importlib import metadata
import sys
from pathlib import Path

from sqlalchemy.dialects import postgresql 

#allow impport app when running as  pyhon sql/init_dbpy 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import (
    text,
    MetaData,
    Table,
    Column,
    Integer,
    Text,
    Numeric,
    ForeignKey,
    Index, 
    ) 

from sqlalchemy.dialects.postgresql import JSONB 
from sqlalchemy.types import UserDefinedType

from app.config import DATABASE_URL 
from app.db import engine 


class TSVectorType(UserDefinedType):
    def get_col_spec(self, **kw):
        return "TSVECTOR"

class Vector384Type(UserDefinedType):
    def get_col_spec(self,**kw):
        return "vector(384)"


metadata = MetaData()


restaurants = Table(
    "restaurants",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", Text, nullable=False),
    Column("address", JSONB),
    Column("cuisine", Text),
    Column("hours", JSONB),
    Column("rating", Numeric(2,1)),
    Column("review_count", Integer),
    Column("description", Text),
    Column("embedding", Vector384Type()),
    Column("search", TSVectorType())
)

reviews = Table(
    "reviews",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("restaurant_id", Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False),
    Column("text", Text, nullable=False),
    Column("rating", Integer)
)

idx_restaurant_search = Index(
    "idx_restaurant_search",
    restaurants.c.search,
    postgresql_using="gin" 
)

def init_db():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()

    metadata.create_all(engine)

    #ivfflat aka ANN 
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_restaurants_embedding
        ON restaurants USING ivfflat (embedding vector_cosine_ops) WITH (lists = 3)
        """))
        conn.commit() 
    print("DB Success initialization")


if __name__ == "__main__":
    init_db()