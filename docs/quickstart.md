# Quick Start

**Signal → State → Strategy. Three ways in.**

| Path | Time | Start |
|------|------|-------|
| **Telegram Bot** | 1 min | [@deckerclawbot](https://t.me/deckerclawbot) → `/btc` |
| **REST API** | 3 min | Get key → curl |
| **Python SDK** | 5 min | Get key → git clone → pip install |

---

## Step 0 — Get your API key (30 seconds)

All API paths (REST and SDK) require an API key. Get one now:

1. Open Telegram → [@deckerclawbot](https://t.me/deckerclawbot)
2. Send `/start`
3. Send `/apikey` → receive `dk_live_xxxxxxxxxxxxxxxxxxxxxxxx`

> **Lost your key?** Run `/apikey reset` — revokes and reissues.

---

## Path A — Telegram Bot (no code required)

The fastest way to see Decker in action:

1. Open [@deckerclawbot](https://t.me/deckerclawbot)
2. Connect at [decker-ai.com/decker-link-telegram](https://decker-ai.com/decker-link-telegram)
3. Ask in plain language:

| Say | What you get |
|-----|-------------|
| `bitcoin signal` or `/btc` | BTCUSDT latest signal (direction, entry, target, stop, progress) |
| `eth 4h` | ETHUSDT 4h timeframe signal |
| `what should I do?` | Progress-based strategy from the rulebook |
| `show position` | Current portfolio summary |

---

## Path B — REST API

```bash
# Health check — no key required
curl https://api.decker-ai.com/api/v1/public/health
# → {"status": "ok"}

# Verify your key
curl -X POST https://api.decker-ai.com/api/v1/public/auth/verify \
  -H "X-API-Key: dk_live_xxx"
# → {"valid": true, "tier": "free", "rate_limit": 100}

# Latest signal
curl "https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/latest?timeframe=1h" \
  -H "X-API-Key: dk_live_xxx"

# Structural narrative
curl "https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/narrative?timeframe=4h" \
  -H "X-API-Key: dk_live_xxx"
```

**Supported symbols**: `BTCUSDT` `ETHUSDT` `SOLUSDT` `BNBUSDT` `XRPUSDT` `DOGEUSDT`  
**Supported timeframes**: `30m` `1h` `4h` `1d`

Other symbols/timeframes → `404`.

All `/public/*` endpoints require `X-API-Key`. Rate limit headers are returned on every response.

→ Full endpoint reference: [api-guide.md](api-guide.md) · [api.decker-ai.com/docs](https://api.decker-ai.com/docs)

---

## Path C — Python SDK

The SDK is included in this repository:

```bash
git clone https://github.com/gigshow/decker-ai-strategy-builder.git
pip install -e decker-ai-strategy-builder/sdk/python/
```

```python
from decker_client import Client, RateLimitError, NotFoundError

with Client(api_key="dk_live_xxx") as client:
    # Latest signal
    sig = client.signals.get_latest("BTCUSDT", timeframe="1h")
    print(f"{sig.direction} | entry={sig.entry_price} | progress={sig.progress_pct}%")
    print(f"gate: {sig.operation_gate}")  # GO / WATCH / HOLD

    # Structural narrative
    narr = client.signals.get_narrative("BTCUSDT", "4h")
    print(narr.text)

    # Rate limit info
    rl = client.last_rate_limit
    print(f"{rl.remaining}/{rl.limit} remaining today")
```

> `pip install decker-client` (PyPI) is planned — not yet published. Use the local install above.

→ SDK reference: [sdk/python/README.md](../sdk/python/README.md)

---

## Rate Limits

| Tier | Limit | How to upgrade |
|------|-------|----------------|
| FREE | 100 req/day | Contact via Telegram bot |
| BASIC | 10,000 req/day | Contact via Telegram bot |
| PREMIUM | 100,000 req/day | Contact via Telegram bot |

Headers on every response: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`  
Exceeded → HTTP 429 + `Retry-After`

---

## Understanding the Response

```json
{
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "direction": "long",
  "entry_price": 94200.0,
  "target_price": 97500.0,
  "stop_loss": 92800.0,
  "progress_pct": 67.3,
  "operation_gate": "GO",
  "generated_at": "2026-04-23T05:00:00Z"
}
```

| Field | Meaning |
|-------|---------|
| `direction` | `long` or `short` |
| `progress_pct` | How far the signal has moved toward its target (0–100%) |
| `operation_gate` | `GO` = enter now · `WATCH` = observing · `HOLD` = stand by |
| `entry_price` | Suggested entry level |
| `target_price` | Target exit level |
| `stop_loss` | Stop-loss level |

> **Only enter on `GO`.** `WATCH` and `HOLD` mean the engine is not yet issuing an entry signal.

---

## Next Steps

- [Developer API Guide](DEVELOPER_API_GUIDE.md) — Auth, error codes, SDK, FAQ
- [API Guide](api-guide.md) — Full endpoint reference
- [Architecture](architecture.md) — How the signal engine works
- [RULES.yaml](../operation_rules/RULES.yaml) — Open rulebook (v2.4.7+)
- [Article Series](medium/README.md) — Deep dives
