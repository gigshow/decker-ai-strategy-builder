# Decker API Guide

Base URL: `https://api.decker-ai.com`  
OpenAPI spec: [api.decker-ai.com/docs](https://api.decker-ai.com/docs)

---

## Authentication

All `/api/v1/public/*` endpoints require an `X-API-Key` header.

```
X-API-Key: dk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Get your key at [decker-ai.com](https://decker-ai.com) → Settings → API Keys.

---

## Rate Limits

| Tier | Limit | Headers |
|------|-------|---------|
| **FREE** | 100 req/day | `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` |
| **BASIC** | 10,000 req/day | same |
| **PREMIUM** | 100,000 req/day | same |

Limit exceeded → `HTTP 429` with `Retry-After` header.

Verify your key and tier:

```bash
curl -X POST https://api.decker-ai.com/api/v1/public/auth/verify \
  -H "X-API-Key: dk_live_xxx"
# → {"valid": true, "tier": "free", "rate_limit": 100}
```

---

## Public Endpoints

These require `X-API-Key`. Responses include rate limit headers.

### Verify API Key

```
POST /api/v1/public/auth/verify
```

```bash
curl -X POST https://api.decker-ai.com/api/v1/public/auth/verify \
  -H "X-API-Key: dk_live_xxx"
```

```json
{
  "valid": true,
  "tier": "basic",
  "rate_limit": 10000,
  "permissions": ["signals:read", "signals:narrative"]
}
```

---

### Structural Narrative (LLM)

```
GET /api/v1/public/signals/{symbol}/narrative?timeframe=1h
```

Returns the LLM-generated explanation of the current structural state.

```bash
curl "https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/narrative?timeframe=1h" \
  -H "X-API-Key: dk_live_xxx"
```

```json
{
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "text": "B-leg confirmed at 66% progress. Counter-swing absorbed. Recommend: 30% partial TP or hold to target.",
  "generated_at": "2026-04-23T10:00:00Z"
}
```

---

### Latest Signal

```
GET /api/v1/public/signals/{symbol}/latest
```

Returns direction, entry, target, stop for the current active signal.

```bash
curl "https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/latest" \
  -H "X-API-Key: dk_live_xxx"
```

```json
{
  "symbol": "BTCUSDT",
  "direction": "long",
  "entry_price": 96000,
  "target_price": 100000,
  "stop_loss": 92000,
  "progress_pct": 66,
  "status": "in_progress"
}
```

---

### Health Check

```
GET /api/v1/public/health
```

No auth required. Returns service status.

```bash
curl https://api.decker-ai.com/api/v1/public/health
# → {"status": "ok"}
```

---

## Additional Endpoints (Beta)

These endpoints are available for exploration. API key optional.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/signals/{symbol}/state` | Signal state + `progress_pct` + `operation_gate` |
| `GET` | `/api/v1/signals/{symbol}/strategy` | Strategy from YAML rulebook |
| `GET` | `/api/v1/signals/{symbol}/consultation` | AI rationale + ranked choices |
| `GET` | `/api/v1/llm/opportunities` | LLM insight feed (conviction, tf_alignment, choices) |
| `GET` | `/api/v1/judgment/coverage` | 20 symbols × 6 timeframes coverage |

---

## Python SDK

```bash
pip install decker-client    # Python 3.9+
```

```python
from decker_client import Client, RateLimitError

with Client(api_key="dk_live_xxx") as client:
    # Structural narrative
    narr = client.signals.get_narrative("BTCUSDT", "1h")
    print(narr.text)

    # Latest signal
    sig = client.signals.get_latest("BTCUSDT")
    print(f"{sig.direction} | entry={sig.entry_price} target={sig.target_price}")

    # Rate limit remaining
    print(client.last_rate_limit.remaining)

    # Handle rate limits
    try:
        narr = client.signals.get_narrative("SOLUSDT", "4h")
    except RateLimitError as e:
        print(f"Retry in {e.retry_after}s")
```

Full guide: [DEVELOPER_API_GUIDE.md](DEVELOPER_API_GUIDE.md)

---

## Signal Fields

### `progress_pct`

Every signal has a lifecycle from formation (0%) to target (100%).

| progress_pct | State | Suggested action |
|---|---|---|
| 0–32% | Early | Wait or prepare entry |
| 33–66% | Active | Entry window, risk management begins |
| 67–89% | Late | Partial take-profit, reduce size |
| 90–100% | At target | Prepare full exit |

### `status` values

| status | Meaning |
|--------|---------|
| `in_progress` | Active — target and stop not yet hit |
| `target_reached` | Price reached target |
| `stop_hit` | Stop loss triggered |
| `expired` | Signal timed out |
| `unknown` | Insufficient data to determine |

### `operation_gate`

Three modes from the structural state machine:

| Gate | Meaning |
|------|---------|
| `GO` | Structural conditions favorable — entry or hold |
| `WATCH` | Transition — wait for confirmation |
| `HOLD` | Counter-trend risk — reduce or exit |

---

## LLM Insight Feed

```
GET /api/v1/llm/opportunities?symbol=BTC&minConfidence=0.6&limit=5
```

Optimized for agent/chatbot use. Each entry contains `conviction`, `progress_pct`, `rationale`, and ranked `choices`.

```json
{
  "opportunities": [
    {
      "symbol": "BTCUSDT",
      "timeframe": "4h",
      "direction": "long",
      "conviction": 0.72,
      "progress_pct": 66,
      "status": "in_progress",
      "rationale": "B-leg at 66% — counter-swing absorbed. 30% partial TP suggested.",
      "choices": [
        { "action": "hold", "description": "Hold to target" },
        { "action": "partial_take_profit", "pct": 30, "description": "30% partial TP" },
        { "action": "full_close", "description": "Close full position" }
      ],
      "tf_alignment": "fully_aligned",
      "entry_price": 96000,
      "target_price": 100000,
      "stop_loss": 92000
    }
  ]
}
```

`tf_alignment` values: `fully_aligned` · `lower_aligned` · `counter_trend` · `transition` · `mixed`

**Cost**: Rule-based path — $0 LLM tokens.

---

## Error Codes

| HTTP | Code | Meaning |
|------|------|---------|
| 401 | `invalid_api_key` | Key missing, malformed, or not found |
| 403 | `permission_denied` | Key valid but lacks required permission |
| 404 | `not_found` | Symbol has no active signal |
| 422 | `validation_error` | Bad request parameters |
| 429 | `rate_limit_exceeded` | Daily quota exhausted — check `Retry-After` |
| 500 | `server_error` | Internal error |

---

## Data Sources

- **Price data**: Binance primary, Hyperliquid secondary (DEX perpetuals)
- **Signal engine**: Deterministic state machine — same input → same output, always
- **LLM role**: Explains structural state in plain language — does not make trading decisions
- **RULES.yaml**: Open YAML rulebook — [operation_rules/RULES.yaml](../operation_rules/RULES.yaml)
