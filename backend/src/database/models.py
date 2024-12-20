from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.config import Config

Base = declarative_base()

class EkantipurArticle(Base):
    __tablename__ = 'ekantipur_articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    href = Column(String(500), nullable=False)
    summary = Column(Text, nullable=True)
    image = Column(String(500), nullable=True)

class KathmanduPostArticle(Base):
    __tablename__ = 'kathmandupost_articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    href = Column(String(500), nullable=False)
    summary = Column(Text, nullable=True)
    image = Column(String(500), nullable=True)

# Add more models as needed for additional scrapers
    
def init_db():
    # engine = create_engine(Config.DATABASE_URL)
    print("DEBUG: Models Config.DATABASE_URL =", Config.DATABASE_URL)

    engine = create_engine(Config.DATABASE_URL, echo=True)
    Base.metadata.create_all(bind=engine)