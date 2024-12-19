# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import SessionLocal
from .models import ScrapedData
from .config import FRONTEND_ORIGINS

app = FastAPI()

origins = FRONTEND_ORIGINS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/data")
def get_latest_data(site_name: str = None):
    session = SessionLocal()
    query = session.query(ScrapedData)
    if site_name:
        query = query.filter(ScrapedData.site_name == site_name)
    data = query.order_by(ScrapedData.scraped_at.desc()).limit(50).all()
    session.close()
    return [
        {
            "site_name": d.site_name,
            "title": d.title,
            "content": d.content,
            "scraped_at": d.scraped_at.isoformat()
        } for d in data
    ]
