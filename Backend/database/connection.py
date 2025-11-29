from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.database_models import Base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gold_prices.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
