from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.fetcher import get_new_listings, get_token_overview, get_trending_tokens
from app.scorer import score_token
from collections import defaultdict, deque
import time
import csv
import io
from fastapi.responses import StreamingResponse, HTMLResponse
from pathlib import Path

app = FastAPI(
    title="OnChain Threat Radar",
    description="Real-time rug pull and pump & dump detection for Solana tokens",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- IN-MEMORY CACHE ---
# Stores last 10 risk scores per token address for sparkline
score_history = defaultdict(lambda: deque(maxlen=10))

# Stores last 50 flagged tokens across all scans for history log
scan_log = deque(maxlen=50)


def enrich_token(token: dict) -> dict:
    addr = token.get("address")
    symbol = token.get("symbol", "?")
    name = token.get("name", "?")
    logo = token.get("logoURI", "")
    liquidity = token.get("liquidity", 0)
    listed_at = token.get("liquidityAddedAt", "")

    overview = get_token_overview(addr)
    result = score_token(overview)

    # Record score in history
    score_history[addr].append({
        "score": result["score"],
        "ts": time.strftime("%H:%M", time.gmtime())
    })

    enriched = {
        "address": addr,
        "symbol": symbol,
        "name": name,
        "logo": logo,
        "listed_at": listed_at,
        "liquidity": overview.get("liquidity", liquidity) or liquidity,
        "price": overview.get("price", 0),
        "market_cap": overview.get("mc", 0),
        "volume_24h": overview.get("v24hUSD", 0),
        "price_change_24h": overview.get("priceChange24hPercent", 0) or overview.get("v24hChangePercent", 0),
        "holders": overview.get("holder", 0) or overview.get("holders", 0),
        "unique_wallets_24h": overview.get("uniqueWallet24h", 0),
        "trades_24h": overview.get("trade24h", 0),
        "risk_score": result["score"],
        "risk_label": result["risk_label"],
        "flags": result["flags"],
        "score_history": list(score_history[addr]),
    }
    # Add to scan log if medium or high risk
    if result["score"] >= 40:
        scan_log.appendleft({
            "address": addr,
            "symbol": symbol,
            "risk_score": result["score"],
            "risk_label": result["risk_label"],
            "scanned_at": time.strftime("%H:%M:%S", time.gmtime()),
        })

    return enriched


@app.get("/")
def root():
    html_path = Path(__file__).parent.parent / "dashboard.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(encoding="utf-8"))
    return {"status": "online", "message": "OnChain Threat Radar is running"}

@app.get("/api/scan")
def scan_new_listings(limit: int = 10):
    tokens = get_new_listings(limit)
    results = []
    for token in tokens:
        try:
            results.append(enrich_token(token))
        except Exception as e:
            print(f"[SKIP] {token.get('symbol')} — {e}")
    results.sort(key=lambda x: x["risk_score"], reverse=True)
    return {
        "scanned_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "count": len(results),
        "tokens": results
    }


@app.get("/api/trending")
def scan_trending(limit: int = 10):
    tokens = get_trending_tokens(limit)
    results = []
    for token in tokens:
        try:
            results.append(enrich_token(token))
        except Exception as e:
            print(f"[SKIP] {token.get('symbol')} — {e}")
    results.sort(key=lambda x: x["risk_score"], reverse=True)
    return {
        "scanned_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "count": len(results),
        "tokens": results
    }


@app.get("/api/token/{address}")
def scan_single_token(address: str):
    token = {"address": address, "symbol": "?", "name": "?"}
    return enrich_token(token)


@app.get("/api/history")
def get_scan_history():
    """Return the last 50 medium/high risk tokens seen across all scans."""
    return {
        "count": len(scan_log),
        "tokens": list(scan_log)
    }


@app.get("/api/export")
def export_scan(format: str = "json", limit: int = 20):
    """Export latest new listings scan as JSON or CSV."""
    tokens = get_new_listings(limit)
    results = []
    for token in tokens:
        try:
            results.append(enrich_token(token))
        except Exception as e:
            print(f"[SKIP] {token.get('symbol')} — {e}")
    results.sort(key=lambda x: x["risk_score"], reverse=True)

    if format == "csv":
        output = io.StringIO()
        fields = ["symbol", "name", "address", "risk_score", "risk_label",
                  "price", "liquidity", "market_cap", "volume_24h",
                  "price_change_24h", "holders"]
        writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=threat-radar-scan.csv"}
        )

    return {
        "scanned_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "count": len(results),
        "tokens": results
    }