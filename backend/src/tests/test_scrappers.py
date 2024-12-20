import pytest
from unittest.mock import patch
from src.scrapers.ekantipur_scraper import EkantipurScraper
from src.scrapers.kathmandupost_scraper import KathmanduPostScraper

@pytest.fixture
def ekantipur_scraper():
    return EkantipurScraper()

@pytest.fixture
def kathmandupost_scraper():
    return KathmanduPostScraper()

@patch('src.utils.request_utils.fetch_with_retry')
def test_ekantipur_scraper_scrape(mock_fetch, ekantipur_scraper):
    # Mock the response object
    mock_response = mock_fetch.return_value
    mock_response.content = b"""
    <section class="main-news">
        <article>
            <h2><a href="/article1">Title 1</a></h2>
            <p>Summary 1</p>
            <img src="image1.jpg" />
        </article>
        <article>
            <h2><a href="/article2">Title 2</a></h2>
            <p>Summary 2</p>
            <img src="image2.jpg" />
        </article>
    </section>
    """
    data = ekantipur_scraper.scrape()
    assert len(data) == 2
    assert data[0]['title'] == 'Title 1'
    assert data[0]['href'] == '/article1'
    assert data[0]['summary'] == 'Summary 1'
    assert data[0]['image'] == 'https://image1.jpg'

@patch('src.utils.request_utils.fetch_with_retry')
def test_kathmandupost_scraper_scrape(mock_fetch, kathmandupost_scraper):
    # Mock the response object
    mock_response = mock_fetch.return_value
    mock_response.content = b"""
    <div class="container">
        <div class="row order">
            <article>
                <h3><a href="/article1">Title A</a></h3>
                <p>Summary A</p>
                <img data-src="imageA.jpg" />
            </article>
            <article>
                <h3><a href="/article2">Title B</a></h3>
                <p>Summary B</p>
                <img data-src="imageB.jpg" />
            </article>
        </div>
    </div>
    """
    data = kathmandupost_scraper.scrape()
    assert len(data) == 2
    assert data[0]['title'] == 'Title A'
    assert data[0]['href'] == 'https://kathmandupost.com/article1'
    assert data[0]['summary'] == 'Summary A'
    assert data[0]['image'] == 'imageA.jpg'