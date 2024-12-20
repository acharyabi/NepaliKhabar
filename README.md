# Nepali News Scraper Workflow

This repository contains a Prefect-based workflow to scrape content from multiple Nepali news websites.

## Table of Contents
1. [Prerequisites](#prerequisites)  
2. [Setup](#setup)  
3. [Configuration](#configuration)  
4. [Usage](#usage)  
5. [Deployment & Execution](#deployment--execution)  
6. [Contributing](#contributing)  
7. [Project Structure](#project-structure)  
---

## Prerequisites

- **Python 3.10+** [I've use python 3.13 for this project]  
- **Prefect** [https://docs.prefect.io/] (v3+)  
- PostgreSQL database (or any other database supported by your connection parameters)  
- Basic command-line proficiency
- I've tried new uv package manager but you can use anything you like.
---

## Setup

1. **Clone this repository**:
   ```bash
   git clone https://github.com/acharyabi/NepaliKhabar.git
   cd NepaliKhabar
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   uv venv
   uv init
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   uv add -r requirements.txt
   ```
---

## Configuration

### Environment Variables

You can configure the following environment variables to customize your setup:

- **`DATABASE_URL`**: Connection string for your Postgres (or other) database.  
  Example:
  ```bash
  export DATABASE_URL=postgresql://root:root@localhost:5432/scraper_db
  ```
- **`LOG_FILE`**: Path to the log file.  
  Example:
  ```bash
  export LOG_FILE=app.log
  ```
- **`LOG_LEVEL`**: Level of logging (e.g., DEBUG, INFO, WARNING, ERROR).  
  Example:
  ```bash
  export LOG_LEVEL=INFO
  ```

You can place these in a `.env` file (if desired) and use a Python library such as [python-dotenv](https://pypi.org/project/python-dotenv/) to load them automatically.

---

## Usage

1. **Prepare the Database**  
   Ensure you have a running PostgreSQL instance with the appropriate user and password. If needed, create your `scraper_db`:
   ```sql
   CREATE DATABASE scraper_db;
   CREATE USER root WITH ENCRYPTED PASSWORD 'root';
   GRANT ALL PRIVILEGES ON DATABASE scraper_db TO root;
   ```

2. **Set Environment Variables**  
   Make sure `DATABASE_URL`, `LOG_FILE`, and `LOG_LEVEL` are set properly in your shell or `.env` file.

3. **Build or Update the Flow**  
   Edit your flow (`scraping_flow.py`) and tasks (`site_scrapers.py`) if you need to add more  news sites to scrape.

---

## Deployment & Execution

To run your scraping job using Prefect, follow these steps:

1. **Create a Work Pool**  
   ```bash
   prefect work-pool create "scrape-queue"
   ```
   This sets up a queue to which workers can subscribe.

2. **Start a Worker**  
   ```bash
   prefect worker start --pool scrape-queue
   ```
   A worker will start listening to the `scrape-queue` for any scheduled or triggered flows.

3. **Run the Deployment**  
   ```bash
   prefect deployment run 'collect-scraping-data/scraping-sites-deployment'
   ```
   This command triggers the flow in the `scraping-sites-deployment`.

4. **Monitor the Flow**  
   - Use the Prefect UI (Prefect Cloud or Prefect UI if you’re running locally) to monitor the state of your flows and tasks, view logs, and manage schedules.


## Contributing
1. **Fork the repository**  
2. **Create a feature branch**
3. **Commit your changes** 
4. **Push to the branch** : We welcome contributions to add new sites, optimize performance, or improve reliability.
---

## Project Structure

A typical structure might look like this:

```
NepaliKhabar/
├── backend
│   └── src
│       ├── __init__.py
│       ├── api
│       │   ├── __init__.py
│       │   └── endpoints.py
│       ├── config.py       # Database configuration.
│       ├── database        # Database logic, models, and session management.
│       │   ├── __init__.py
│       │   ├── models.py
│       │   └── session.py
│       ├── factories       # Abstract & concrete factories for building objects.
│       │   ├── __init__.py
│       │   ├── abstact_factory.py
│       │   └── concrete_factory.py
│       ├── main.py         # Entry point for running the app.
│       ├── scrapers        # Web scraping logic for various Nepali news sites.
│       │   ├── __init__.py
│       │   ├── base_scraper.py
│       │   ├── ekantipur_scraper.py
│       │   └── kathmandupost_scraper.py
│       ├── tests           # Automated tests for scrapers.
│       │   ├── test_api.py
│       │   └── test_scrappers.py
│       └── utils           # Utility functions.
│           ├── __init__.py
│           └── request_utils.py
├── docker-compose.yaml     # Docker configuration for spinning up services.
├── requirements.txt        # Project dependencies.
│
```
- **flows**: Contains Prefect flows, which define the high-level orchestration.  
- **tasks**: Contains lower-level tasks to scrape individual websites.
- **deployments**: Contains Prefect deployment configurations that specify schedules.

---

**Happy Scraping!**  
If you encounter any issues or have suggestions, please [open an issue](https://github.com/acharyabi/NepaliKhabar). 
Feel free to customize this **README** to best fit your project and organizational needs.

