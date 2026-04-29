from app.fetcher import get_new_listings, get_token_overview
from app.scorer import score_token

tokens = get_new_listings(3)
for t in tokens:
    addr = t['address']
    symbol = t['symbol']
    overview = get_token_overview(addr)
    result = score_token(overview)
    print(f"--- {symbol} ({addr[:8]}...) ---")
    print(f"Risk: {result['risk_label']} | Score: {result['score']}/100")
    for flag in result['flags']:
        print(f"  {flag}")
    print()