from prefect import flow, task
from backend.db import SessionLocal
from backend.models import ScrapedData
from backend.scrapers.factory import ScraperFactory
from sqlalchemy import text

@task
def scrape_site(site_name: str):
    scraper = ScraperFactory.get_scraper(site_name)
    return scraper.scrape()

@task
def store_data(records: list[dict]):
    session = SessionLocal()
    try:
        for record in records:
            data = ScrapedData(
                site_name=record["site_name"],
                title=record["title"],
                content=record["content"],
                scraped_at=record["scraped_at"]
            )
            session.add(data)
        session.commit()
    finally:
        session.close()

@task
def cleanup_old_data():
    session = SessionLocal()
    try:
        session.execute(text("DELETE FROM scraped_data WHERE scraped_at < NOW() - INTERVAL '10 days'"))
        session.commit()
    finally:
        session.close()

@flow(name="scrape_flow_test")
def test_flow():
    data = scrape_site("ekantipur")
    store_data(data)
    cleanup_old_data()

if __name__ == "__main__":
    test_flow()
