# backend/models.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, text
import datetime

Base = declarative_base()

class ScrapedData(Base):
    __tablename__ = "scraped_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    site_name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(5000), nullable=False)
    scraped_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'), nullable=False)