# Developer API Guide

Everything you need to integrate Decker into your app, bot, or agent.

---

## 1. Quickstart (3 lines)

```bash
pip install decker-client
```

```python
from decker_client import Client

client = Client(api_key="dk_live_xxx")
sig = client.signals.get_latest("BTCUSDT")
print(f"{sig.direction} | {sig.entry_price} → {sig.target_price}")
# → long | 96000 → 100000
```

Get your key: [decker-ai.com](https://decker-ai.com) → Settings → API Keys

---

## 2. Authentication

All `/api/v1/public/*` endpoints require:

```
X-API-Key: dk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Never put the key in a URL. Always use the header.

**Verify your key:**

```bash
curl -X POST https://api.decker-ai.com/api/v1/public/auth/verify \
  -H "X-API-Key: dk_live_xxx"
```

```json
{ "valid": true, "tier": "free", "rate_limit": 100 }
```

---

## 3. Rate Limits

| Tier | Daily Limit | How to upgrade |
|------|------------|----------------|
| FREE | 100 req/day | [decker-ai.com](https://decker-ai.com) → Billing |
| BASIC | 10,000 req/day | same |
| PREMIUM | 100,000 req/day | same |

Every response includes:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1745452800
```

When exceeded → HTTP 429 + `Retry-After: 3600`

**Python SDK — check remaining:**

```python
client.signals.get_latest("BTCUSDT")
print(client.last_rate_limit.remaining)  # → 87
```

---

## 4. Endpoints

### Public (require `X-API-Key`)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/public/auth/verify` | Verify key + get tier |
| `GET` | `/api/v1/public/health` | Liveness (no auth) |
| `GET` | `/api/v1/public/signals/{symbol}/narrative` | LLM narrative |
| `GET` | `/api/v1/public/signals/{symbol}/latest` | Signal: direction, entry, target, stop |

### Additional (beta, key optional)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/signals/{symbol}/state` | State + `progress_pct` + `operation_gate` |
| `GET` | `/api/v1/signals/{symbol}/strategy` | Rulebook strategy |
| `GET` | `/api/v1/signals/{symbol}/consultation` | AI rationale + ranked choices |
| `GET` | `/api/v1/llm/opportunities` | Multi-symbol insight feed |
| `GET` | `/api/v1/judgment/coverage` | 20 symbols × 6 timeframes |

Full spec: [api.decker-ai.com/docs](https://api.decker-ai.com/docs)

---

## 5. Python SDK

```bash
pip install decker-client    # Python 3.9+
```

### Basic usage

```python
from decker_client import Client

with Client(api_key="dk_live_xxx") as client:
    # Narrative
    narr = client.signals.get_narrative("BTCUSDT", "1h")
    print(narr.text, narr.generated_at)

    # Latest signal
    sig = client.signals.get_latest("ETHUSDT")
    print(f"{sig.direction} | entry={sig.entry_price} target={sig.target_price}")

    # Health check
    health = client.health.check()
    print(health.ok)  # True

    # Rate limit info
    rl = client.last_rate_limit
    print(f"{rl.remaining}/{rl.limit} remaining today")
```

### Error handling

```python
from decker_client import Client, RateLimitError, AuthError, NotFoundError

with Client(api_key="dk_live_xxx") as client:
    try:
        sig = client.signals.get_latest("BTCUSDT")
    except AuthError:
        print("Invalid API key")
    except NotFoundError:
        print("No active signal for this symbol")
    except RateLimitError as e:
        print(f"Rate limited — retry in {e.retry_after}s")
```

Source: [`sdk/python/`](../sdk/python/) · [PyPI](https://pypi.org/project/decker-client/)

---

## 6. curl Examples

```bash
# Verify key
curl -X POST https://api.decker-ai.com/api/v1/public/auth/verify \
  -H "X-API-Key: dk_live_xxx"

# Narrative
curl "https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/narrative?timeframe=1h" \
  -H "X-API-Key: dk_live_xxx"

# Latest signal
curl "https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/latest" \
  -H "X-API-Key: dk_live_xxx"

# Health (no auth)
curl https://api.decker-ai.com/api/v1/public/health

# LLM insight feed (beta)
curl "https://api.decker-ai.com/api/v1/llm/opportunities?symbol=BTC&limit=5"
```

---

## 7. Error Codes

| HTTP | When | What to do |
|------|------|------------|
| 401 | Missing or invalid key | Check `X-API-Key` header |
| 403 | Key valid but lacks permission | Upgrade tier or contact support |
| 404 | No active signal for symbol | Try again later or use `/coverage` |
| 422 | Bad parameters | Check the OpenAPI spec |
| 429 | Daily quota exceeded | Wait until reset (`X-RateLimit-Reset`) |
| 500 | Server error | Retry with backoff; check [status](https://api.decker-ai.com/api/v1/public/health) |

---

## 8. FAQ

**Q: Which symbols are supported?**  
A: 20 symbols including BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT. Check `/api/v1/judgment/coverage` for the full list.

**Q: Which timeframes are available?**  
A: 15m, 1h, 4h, 8h, 1d, 1w. Default for most endpoints is 1h.

**Q: What is `progress_pct`?**  
A: Every signal has a lifecycle from 0% (formation) to 100% (target reached). 66% means the signal has covered 2/3 of the entry-to-target distance. See [api-guide.md](api-guide.md#progress_pct) for the full table.

**Q: What is `operation_gate`?**  
A: Structural mode — `GO` (enter/hold), `WATCH` (wait), `HOLD` (counter-trend risk). Determined by the state machine, not ML.

**Q: Why does the narrative cost $0?**  
A: The signal and strategy come from a deterministic state machine + YAML rulebook. LLM is only used to translate the structural state into plain language — once per signal state change, cached thereafter.

**Q: Is there a webhook or streaming API?**  
A: Not yet. For real-time updates, poll `/signals/{symbol}/latest` or use the Telegram bot.

**Q: Where do I get help?**  
A: [GitHub Issues](https://github.com/gigshow/decker-ai-strategy-builder/issues) · [Telegram bot](https://t.me/deckerclawbot)
