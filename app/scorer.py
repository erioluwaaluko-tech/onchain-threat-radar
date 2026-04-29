def score_token(overview: dict) -> dict:
    """
    Score a token's risk level using market data from token_overview.
    Score: 0 (safest) → 100 (most dangerous).
    """
    score = 0
    flags = []

    # --- LIQUIDITY CHECK ---
    liquidity = overview.get("liquidity", 0) or 0
    if liquidity < 1000:
        score += 25
        flags.append(f"🚨 Extremely low liquidity (${liquidity:,.0f}) — easy to manipulate price")
    elif liquidity < 10000:
        score += 12
        flags.append(f"⚠️ Low liquidity (${liquidity:,.0f}) — moderate manipulation risk")

    # --- VOLUME VS MARKET CAP (pump signal) ---
    volume_24h = overview.get("v24hUSD", 0) or 0
    market_cap = overview.get("mc", 0) or 0
    if market_cap and volume_24h:
        ratio = volume_24h / market_cap
        if ratio > 10:
            score += 25
            flags.append(f"🚨 Volume is {ratio:.1f}x market cap — extreme pump signal")
        elif ratio > 5:
            score += 15
            flags.append(f"🚨 Volume is {ratio:.1f}x market cap — strong pump signal")
        elif ratio > 2:
            score += 8
            flags.append(f"⚠️ Volume is {ratio:.1f}x market cap — unusual activity")

    # --- PRICE CHANGE SPIKE ---
    price_change = overview.get("priceChange24hPercent", 0) or 0
    if price_change > 500:
        score += 20
        flags.append(f"🚨 Price up {price_change:.0f}% in 24h — possible coordinated pump")
    elif price_change > 200:
        score += 12
        flags.append(f"⚠️ Price up {price_change:.0f}% in 24h — high volatility")
    elif price_change < -60:
        score += 15
        flags.append(f"🚨 Price down {abs(price_change):.0f}% in 24h — possible rug pull in progress")

    # --- HOLDER COUNT ---
    holders = overview.get("holder", 0) or 0
    if holders < 50:
        score += 20
        flags.append(f"🚨 Only {holders} holders — extremely concentrated ownership")
    elif holders < 200:
        score += 10
        flags.append(f"⚠️ Only {holders} holders — low distribution")

    # --- TRADE COUNT (wash trading signal) ---
    trades_24h = overview.get("trade24h", 0) or 0
    if volume_24h > 100000 and trades_24h < 20:
        score += 15
        flags.append(f"🚨 High volume (${volume_24h:,.0f}) but only {trades_24h} trades — likely wash trading")

    # --- UNIQUE WALLETS ---
    unique_wallets = overview.get("uniqueWallet24h", 0) or 0
    if unique_wallets < 10 and volume_24h > 10000:
        score += 10
        flags.append(f"⚠️ Only {unique_wallets} unique wallets trading — coordinated activity likely")

    score = min(score, 100)

    if score >= 70:
        risk_label = "🔴 HIGH RISK"
    elif score >= 40:
        risk_label = "🟡 MEDIUM RISK"
    else:
        risk_label = "🟢 LOW RISK"

    return {
        "score": score,
        "risk_label": risk_label,
        "flags": flags if flags else ["✅ No major red flags detected"]
    }