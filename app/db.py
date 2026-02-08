 # SQLAlchemy engine/session, asyncpg if needed
from config import DATABASE_URL 

from sqlalchemy import create_engine, sessionmaker, Session 

engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True
    )

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False )

def get_session():
    """context manager for session
    """
    session = SessionLocal() 
    try:
         yield session 
    finally:
        session.close() 