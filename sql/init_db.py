#create extension and tables 

from importlib import metadata
import sys
from pathlib import Path 

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

from app.config import DATABSE_URL 
from app.db import engine 


class TSVectorType(UserDefinedType):
    def get_col_spec(self, **kw):
        return "TSVECTOR"

class Vector384Type(UserDefinedType):
    def get_col_spec(self,**kw):
        return "vector(384)"


metadata = MetaData()


resturants = Table(
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
    Column("search", TSVectorType)
)

