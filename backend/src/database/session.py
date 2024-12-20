from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import Config

print("DEBUG: Session Config.DATABASE_URL =", Config.DATABASE_URL)
engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)