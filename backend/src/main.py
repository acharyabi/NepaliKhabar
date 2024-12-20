import logging
from logging.handlers import RotatingFileHandler
from src.database.models import init_db
from src.factories.concrete_factory import EkantipurFactory, KathmanduPostFactory
from src.api import create_app
# import threading
import uvicorn
from prefect import flow, get_run_logger, task
from src.config import Config

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(Config.LOG_LEVEL)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(Config.LOG_LEVEL)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    file_handler = RotatingFileHandler(
        Config.LOG_FILE, maxBytes=10*1024*1024, backupCount=5
    )
    
    file_handler.setLevel(Config.LOG_LEVEL)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


@task
def run_ekantipur():
    loggerData = get_run_logger()
    loggerData.info("Starting Ekantipur scraping...")
    ekantipur_factory = EkantipurFactory()
    ekantipur_scraper = ekantipur_factory.create_scraper()
    ekantipur_data = ekantipur_scraper.scrape()
    ekantipur_scraper.save_to_db(ekantipur_data)
    
@task
def run_kathmandupost():
    loggerData = get_run_logger()
    loggerData.info("Starting KathmanduPost scraping...")
    kathmandupost_factory = KathmanduPostFactory()
    kathmandupost_scraper = kathmandupost_factory.create_scraper()
    kathmandupost_data = kathmandupost_scraper.scrape()
    kathmandupost_scraper.save_to_db(kathmandupost_data)

@flow
def collect_scraping_data():
    run_ekantipur()
    run_kathmandupost()
    
def main():
    setup_logging()
    logging.info("Starting scraping process...")
    logging.info("Initializing the database...")
    init_db()    
    # Start scraping in a separate thread
    # scraping_thread = threading.Thread(target=run_scraping)
    # scraping_thread.start()
    
    # Start the prefect deployment locally.
    collect_scraping_data.serve(name="scraping-sites-deployment", cron="0 8,20 * * *")
    logging.info("Scraping completed successfully.")
    
    # Create FastAPI app
    # app = create_app()
    # uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()