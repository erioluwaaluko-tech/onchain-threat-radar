import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BIRDEYE_API_KEY")
BASE_URL = "https://public-api.birdeye.so"

HEADERS = {
    "accept": "application/json",
    "x-chain": "solana",
    "X-API-KEY": API_KEY
}

def _get(url, params=None):
    """Base request with rate limit protection — 1 request/sec on free tier."""
    time.sleep(1.1)
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json().get("data", {})
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {url} → {e}")
        return {}

def get_new_listings(limit=20):
    """Fetch latest new token listings."""
    data = _get(f"{BASE_URL}/defi/v2/tokens/new_listing", {"limit": limit})
    return data.get("items", [])

def get_token_overview(token_address):
    """Fetch price, volume, liquidity, holder count and market data."""
    return _get(f"{BASE_URL}/defi/token_overview", {"address": token_address})

def get_trending_tokens(limit=20):
    """Fetch currently trending tokens."""
    data = _get(f"{BASE_URL}/defi/token_trending", {
        "sort_by": "rank", "sort_type": "asc", "offset": 0, "limit": limit
    })
    return data.get("tokens", [])

def get_price_history(token_address):
    """Fetch 24h OHLCV price history to detect pump patterns."""
    return _get(f"{BASE_URL}/defi/ohlcv", {
        "address": token_address,
        "type": "1H",
        "limit": 24
    })