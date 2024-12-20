# backend/src/api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from src.database.session import SessionLocal
from src.database.models import EkantipurArticle, KathmanduPostArticle

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for response validation
class Article(BaseModel):
    id: int
    title: str
    href: str
    summary: str = None
    image: str = None

    class Config:
        orm_mode = True

@router.get('/health')
def health(data:str=None):
    return print(f"Server is Up{data}")

@router.get("/ekantipur", response_model=List[Article])
def get_ekantipur_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articles = db.query(EkantipurArticle).offset(skip).limit(limit).all()
    return articles

@router.get("/kathmandupost", response_model=List[Article])
def get_kathmandupost_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articles = db.query(KathmanduPostArticle).offset(skip).limit(limit).all()
    return articles