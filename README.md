# 🛡️ OnChain Threat Radar

> Real-time rug pull & pump-and-dump detection for Solana tokens — powered by [Birdeye Data API](https://bds.birdeye.so)

![OnChain Threat Radar Dashboard](https://img.shields.io/badge/Birdeye-Data%20API-blue) ![Python](https://img.shields.io/badge/Python-3.13-green) ![FastAPI](https://img.shields.io/badge/FastAPI-0.136-teal) ![Sprint](https://img.shields.io/badge/BirdeyeAPI-Sprint%202-purple)

---

## 🚨 What It Does

OnChain Threat Radar is a live security dashboard that automatically scans new Solana token listings and trending tokens, scoring each one from **0 (safe) to 100 (dangerous)** using a multi-signal risk algorithm.

It helps traders and researchers identify potential rug pulls, pump & dump schemes, and suspicious token activity **before** they become victims.

---

## ⚡ Live Features

- 🔴 **Risk Scoring Engine** — scores every token 0–100 across 6 threat signals
- 🆕 **New Listings Scanner** — monitors fresh Solana token launches in real time
- 🔥 **Trending Token Scanner** — detects manipulation in currently trending tokens
- 🔍 **Instant Token Lookup** — paste any Solana address for an immediate risk report
- 📈 **Sparkline History** — tracks how a token's risk score changes across scans
- 🚨 **Alert History Panel** — running log of all medium/high risk tokens detected
- 🔄 **Auto-refresh** — re-scans automatically every 60 seconds
- ⬇️ **Export** — download scan results as JSON or CSV
- 🔗 **Birdeye Links** — direct link to each token on Birdeye for deeper research

---

## 🧠 Risk Scoring Algorithm

Each token is scored across 6 signals pulled from the Birdeye API:

| Signal | Max Points | What It Detects |
|--------|-----------|-----------------|
| Liquidity depth | 25 pts | Low liquidity = easy price manipulation |
| Volume/MarketCap ratio | 25 pts | Extreme ratio = coordinated pump signal |
| Price spike (24h) | 20 pts | 200%+ move = possible pump in progress |
| Holder count | 20 pts | <50 holders = extremely concentrated ownership |
| Wash trading signal | 15 pts | High volume + very few trades = fake activity |
| Unique wallet count | 10 pts | Few wallets + high volume = coordinated buying |

**Risk Labels:**
- 🟢 LOW RISK: 0–39
- 🟡 MEDIUM RISK: 40–69
- 🔴 HIGH RISK: 70–100

---

## 🛠️ Tech Stack

- **Backend:** Python 3.13, FastAPI, Uvicorn
- **Data:** [Birdeye Data API](https://bds.birdeye.so) — `/defi/v2/tokens/new_listing`, `/defi/token_overview`, `/defi/token_trending`
- **Frontend:** Vanilla HTML/CSS/JS, Chart.js (sparklines)
- **Deployment:** Render

---

## 📡 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/scan?limit=15` | Scan latest new token listings |
| `GET /api/trending?limit=15` | Scan currently trending tokens |
| `GET /api/token/{address}` | Score a single token by address |
| `GET /api/history` | Get alert history log |
| `GET /api/export?format=csv` | Export scan as CSV |
| `GET /api/export?format=json` | Export scan as JSON |

---

## 🚀 Run Locally

```bash
git clone https://github.com/erioluwaaluko-tech/onchain-threat-radar.git
cd onchain-threat-radar
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Create a `.env` file:
BIRDEYE_API_KEY=your_api_key_here

Start the backend:
```bash
uvicorn app.main:app --reload
```

Open `dashboard.html` in your browser and click **⚡ Scan Now**.

---

## 🔑 Birdeye API Endpoints Used

- `/defi/v2/tokens/new_listing` — fetches freshest token launches
- `/defi/token_overview` — price, volume, liquidity, holders, market cap
- `/defi/token_trending` — currently trending tokens by rank

---

## 🏆 Built For

[Birdeye Data BIP Competition](https://bds.birdeye.so) — Sprint 2 (April 25 – May 2, 2026)

Built by [@erioluwaaluko-tech](https://github.com/erioluwaaluko-tech)