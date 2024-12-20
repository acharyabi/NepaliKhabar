
from fastapi import FastAPI
def create_app() -> FastAPI:
    app = FastAPI(
        title="Web Scraper API",
        description="API to access scraped articles from Ekantipur and KathmanduPost",
        version="1.0.0",
    )
    from src.api.endpoints import router
    app.include_router(router, prefix="/api", tags=["Articles"])
    return app
