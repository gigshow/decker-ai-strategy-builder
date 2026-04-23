# Quick Start

**Signal → State → Strategy. Three ways in.**

| Path | Time | Start |
|------|------|-------|
| **Python SDK** | 60 sec | `pip install decker-client` |
| **REST API** | 2 min | `curl` + `X-API-Key` header |
| **Telegram** | 5 min | [@deckerclawbot](https://t.me/deckerclawbot) |

Get your API key first: [decker-ai.com](https://decker-ai.com) → Settings → API Keys

---

## Path A — Python SDK

```bash
pip install decker-client
```

```python
from decker_client import Client

client = Client(api_key="dk_live_xxx")

# Structural narrative for BTCUSDT 1h
narr = client.signals.get_narrative("BTCUSDT", "1h")
print(narr.text)
# → "B-leg confirmed at 66% progress. Counter-swing absorbed.
#    Recommend: 30% partial TP or hold to target."

# Latest signal — direction, entry, target, stop
sig = client.signals.get_latest("BTCUSDT")
print(sig.direction, sig.entry_price, sig.target_price)
# → long  96000  100000
```

---

## Path B — REST API

```bash
# Verify your key
curl -X POST https://api.decker-ai.com/api/v1/public/auth/verify \
  -H "X-API-Key: dk_live_xxx"
# → {"valid": true, "tier": "free", "rate_limit": 100}

# Get structural narrative
curl "https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/narrative?timeframe=1h" \
  -H "X-API-Key: dk_live_xxx"

# Get latest signal
curl "https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/latest" \
  -H "X-API-Key: dk_live_xxx"
```

All `/public/*` endpoints require `X-API-Key`. Rate limit headers are returned on every response.

Full endpoint reference: [api-guide.md](api-guide.md) · [api.decker-ai.com/docs](https://api.decker-ai.com/docs)

---

## Path C — Telegram

1. Open [@deckerclawbot](https://t.me/deckerclawbot)
2. Connect your account at [decker-ai.com/decker-link-telegram](https://decker-ai.com/decker-link-telegram)
3. Ask in plain language:

| Say | What you get |
|-----|-------------|
| `bitcoin signal` | BTCUSDT signal — direction, entry, target, stop |
| `show position` | Portfolio summary |
| `what should I do with this signal?` | Progress-based strategy from the rulebook |
| `ETH buy 0.01` | Order with approval flow |

---

## Rate Limits

| Tier | Limit |
|------|-------|
| FREE | 100 req/day |
| BASIC | 10,000 req/day |
| PREMIUM | 100,000 req/day |

Headers on every response: `X-RateLimit-Remaining`, `X-RateLimit-Reset`  
Exceeded → HTTP 429 + `Retry-After`

---

## Next Steps

- [API Guide](api-guide.md) — Full endpoint reference, field definitions, error codes
- [Developer API Guide](DEVELOPER_API_GUIDE.md) — Auth, SDK, FAQ
- [Architecture](architecture.md) — How the signal engine works
- [RULES.yaml](../operation_rules/RULES.yaml) — Open rulebook (v2.4.7+)
- [Article Series](medium/README.md) — Deep dives into the state engine
