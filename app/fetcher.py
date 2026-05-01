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
    """Base request with rate limit protection."""
    time.sleep(1.1)
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("data", {})
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {url} → {e}")
        return {}

def get_new_listings(limit=20):
    """Fetch recently active smaller tokens likely to include new/risky listings."""
    data = _get(f"{BASE_URL}/defi/tokenlist", {
        "sort_by": "v24hUSD",
        "sort_type": "desc",
        "offset": 50,
        "limit": limit,
        "min_liquidity": 100,
        "max_liquidity": 500000
    })
    return data.get("tokens", [])

def get_token_overview(token_address):
    """Fetch price, volume, liquidity, holder count and market data."""
    # Try v3 market data first
    result = _get(f"{BASE_URL}/defi/v3/token/market-data", {
        "address": token_address
    })
    if result:
        return result
    # Fallback to original overview
    return _get(f"{BASE_URL}/defi/token_overview", {"address": token_address})

def get_trending_tokens(limit=20):
    """Fetch currently trending tokens."""
    data = _get(f"{BASE_URL}/defi/token_trending", {
        "sort_by": "rank",
        "sort_type": "asc",
        "offset": 0,
        "limit": limit
    })
    return data.get("tokens", [])