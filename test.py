from app.fetcher import get_new_listings, get_token_overview
from app.scorer import score_token

print("Testing new listings...")
tokens = get_new_listings(3)
print(f"Got {len(tokens)} tokens")

if tokens:
    print("First token keys:", list(tokens[0].keys()))
    for t in tokens:
        addr = t.get('address')
        symbol = t.get('symbol', '?')
        overview = get_token_overview(addr)
        result = score_token(overview)
        print(f"--- {symbol} ---")
        print(f"Risk: {result['risk_label']} | Score: {result['score']}/100")
        for flag in result['flags']:
            print(f"  {flag}")
        print()
else:
    print("No tokens returned - testing trending instead...")
    from app.fetcher import get_trending_tokens
    tokens = get_trending_tokens(3)
    print(f"Got {len(tokens)} trending tokens")
    if tokens:
        print("First token keys:", list(tokens[0].keys()))