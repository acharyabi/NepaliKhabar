import requests
import time
import logging

def fetch_with_retry(url: str, max_retries: int = 5, backoff_factor: float = 0.3) -> requests.Response:
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            wait = backoff_factor * (2 ** (attempt - 1))
            logging.warning(f"Attempt {attempt} failed for URL {url}. Retrying in {wait} seconds...")
            time.sleep(wait)
    logging.error(f"All {max_retries} attempts failed for URL {url}.")
    return None
