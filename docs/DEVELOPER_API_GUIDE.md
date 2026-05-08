# Decker Developer API Guide

Everything you need to integrate Decker signals into your app, bot, or agent.  
Full OpenAPI spec: [api.decker-ai.com/docs](https://api.decker-ai.com/docs)

---

## 0. Try it first (no sign-up)

```bash
curl https://api.decker-ai.com/api/v1/public/demo
```

Returns live BTCUSDT 1h signal right now — no API key needed.  
Rate limit: **10 req/IP/day**.

```json
{
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "direction": "long",
  "entry_price": 94200.0,
  "target_price": 97500.0,
  "stop_loss": 92800.0,
  "progress_pct": 27.3,
  "operation_gate": "GO",
  "narrative": "GO — A-cycle active at 27% progress. Entry window open.",
  "_demo": {
    "note": "Demo endpoint — BTCUSDT 1h only, 10 req/IP/day.",
    "get_full_access": "Telegram @deckerclawbot → /apikey"
  }
}
```

Once you've seen live data, follow steps 1–3 below to get your API key.

---

## 1. Quickstart (3 steps)

### Step 1 — Sign up & link Telegram

1. Create an account at [decker-ai.com](https://decker-ai.com)
2. Go to **decker-ai.com/decker-link-telegram** → get your link code
3. Open Telegram **@deckerclawbot** and send `/start {code}`

### Step 2 — Get your API key

In the Telegram bot:

```
/apikey
```

→ Receive a key in the format `dk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`  
→ The full key is shown **once only**. Copy it now.

> Lost your key? Run `/apikey reset` to revoke and reissue.

### Step 3 — Make your first call

```bash
curl "https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/latest?timeframe=1h" \
  -H "X-API-Key: dk_live_xxx"
```

```json
{
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "direction": "long",
  "entry_price": 94200.0,
  "target_price": 97500.0,
  "stop_loss": 92800.0,
  "current_price": 95100.0,
  "progress_pct": 27.3,
  "operation_gate": "GO",
  "generated_at": "2026-04-23T05:00:00Z"
}
```

---

## 2. Authentication

All public API requests require:

```
X-API-Key: dk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

| Field | Value |
|-------|-------|
| Key format | `dk_live_<32 URL-safe chars>` |
| Where to issue | Telegram `/apikey` |
| Expiry | None by default |
| Revoke | `/apikey reset` |

> **Note**: `Authorization: Bearer` headers are not recognized by the public API.

**Verify your key:**

```bash
curl -X POST https://api.decker-ai.com/api/v1/public/auth/verify \
  -H "X-API-Key: dk_live_xxx"
```

```json
{ "valid": true, "tier": "free", "rate_limit": 100, "permissions": ["read:signals"] }
```

---

## 3. Rate Limits

Quota resets daily at **UTC midnight**.

| Tier | Price | Daily Limit | How to upgrade |
|------|-------|------------|----------------|
| FREE | $0 (forever) | 30 calls/day | Default on `/apikey` |
| PRO | $20 / month · 7d trial | 10,000 calls/day | Telegram bot · auto-charge after trial |
| ENTERPRISE | Contact us | 100,000+ calls/day · custom SLA | Contact via Telegram bot |

> **Beta** (current): all authenticated users get **PRO full access** for free (`BETA_TIER_OVERRIDE=PRO` env on backend).

Every response includes:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1745452800
```

When exceeded → HTTP 429 + `Retry-After: <seconds>`

---

## 4. Endpoints

### `GET /api/v1/public/health` — Liveness (no auth)

```bash
curl https://api.decker-ai.com/api/v1/public/health
# → {"status": "ok"}
```

### `POST /api/v1/public/auth/verify` — Verify key

```bash
curl -X POST https://api.decker-ai.com/api/v1/public/auth/verify \
  -H "X-API-Key: dk_live_xxx"
```

### `GET /api/v1/public/signals/{symbol}/latest` — Latest signal

```bash
curl "https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/latest?timeframe=1h" \
  -H "X-API-Key: dk_live_xxx"
```

**`timeframe` values**: `15m`, `30m`, `1h`, `4h`, `8h`, `1d`, `1w`  
**`operation_gate`**: `GO` = entry signal · `WATCH` = observing · `HOLD` = stand by  
→ Only enter on `GO`.

### `GET /api/v1/public/signals/{symbol}/narrative` — Structural narrative

Rule-based plain-language summary. Deterministic, zero LLM cost.

```bash
curl "https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/narrative?timeframe=4h" \
  -H "X-API-Key: dk_live_xxx"
```

```json
{
  "symbol": "BTCUSDT",
  "timeframe": "4h",
  "narrative": "BTCUSDT·4h — WATCH, c_state B_SET, label INSIDE_AFTER_2_TO_1.",
  "axis": "observation",
  "generated_at": "2026-04-23T05:00:00Z"
}
```

**`axis`**: `bullish` | `bearish` | `observation`

### `GET /api/v1/public/demo` — Live demo (no API key)

Returns BTCUSDT 1h combined signal + narrative. No authentication needed.  
Rate limited to **10 req/IP/day**. Ideal for embedding in README examples or quick experiments.

```bash
curl https://api.decker-ai.com/api/v1/public/demo
```

Response includes all fields from `/latest` plus `narrative` and `axis`.

### `GET /api/v1/public/stats` — Signal activity stats (no API key)

Returns 30-day engine signal evaluation counts per symbol, with GO/WATCH/HOLD distribution.  
No authentication required. Cached for **60 seconds**.

```bash
curl https://api.decker-ai.com/api/v1/public/stats
```

```json
{
  "period_days": 30,
  "engine": "engine:live_l1",
  "total_evaluations": 8240,
  "symbol_count": 6,
  "updated_at": "2026-04-23T10:00:00Z",
  "symbols": [
    {
      "symbol": "BTCUSDT",
      "total_evaluations": 2160,
      "gate_distribution": { "GO": 980, "WATCH": 720, "HOLD": 460 },
      "timeframes": ["1h", "4h", "1d"],
      "last_evaluated_at": "2026-04-23T09:58:00Z"
    }
  ]
}
```

> `gate_distribution` shows structural bias: `GO` = favorable for entry, `WATCH` = observing transition, `HOLD` = counter-trend risk.

### `GET /api/v1/public/krx/signals` — KRX Korean stocks (Beta)

KOSPI + KOSDAQ universe with **portfolio actions** (ADD/HOLD/REDUCE/EXIT) — not buy/sell. Daily 16:30 KST evaluation. **Beta tier free**.

```bash
curl -H "X-API-Key: $KEY" \
  'https://api.decker-ai.com/api/v1/public/krx/signals?gate=GO&market=KOSPI&limit=10'
```

**Query**: `gate` (GO/WATCH/HOLD) · `action` (ADD/HOLD/REDUCE/EXIT) · `sector` · `market` (KOSPI/KOSDAQ/ALL) · `timeframe` (1d/1w) · `limit` (≤500)

**Response signal fields**:
```typescript
{
  ticker:           string                // "005930"
  company_name:     string                // "삼성전자"
  market:           "KOSPI" | "KOSDAQ"
  sector:           string                // KSIC 33-classification
  action_gate:      "GO" | "WATCH" | "HOLD"
  portfolio_action: "ADD" | "HOLD" | "REDUCE" | "EXIT"
  entry_krw:        number | null         // entry price (KRW)
  target_krw:       number | null
  stop_krw:         number | null
  key_direction:    "+" | "-" | "0"
  c_state:          string                // engine FSM state
  user_state:       "DRIVE" | "FORMING" | "PENDING" | "WATCH" | "IDLE"
  krx_context: {
    foreign_streak:        number | null  // foreign net-buy days (KIS API integration pending)
    kospi200_rs_pct:       number | null
    dart_recency_days:     number | null
    limit_lock_state:      "normal" | "upper_limit_locked" | "lower_limit_locked"
  }
}
```

Response meta: `gate_counts` · `action_counts` · `data_freshness` (fresh/stale/danger).

### `GET /api/v1/public/krx/market` — KRX market macro (Beta)

Market header — USD/KRW · base rate · KOSPI200 · signal distribution + sector breakdown + data_freshness.

```bash
curl -H "X-API-Key: $KEY" 'https://api.decker-ai.com/api/v1/public/krx/market'
```

> **KRX beta limits**: Foreign net-buy / market cap / fundamentals require KIS Open API integration (Q3-Q4 2026). KIS automated trading is on the Q4 roadmap. Source of truth: [`docs/krx/KRX_BUSINESS_MODEL_AND_ROADMAP_2026-05-09.md`](krx/KRX_BUSINESS_MODEL_AND_ROADMAP_2026-05-09.md).

---

## 5. Supported Symbols & Timeframes

### Crypto (GA)
Engine-evaluated symbols: `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `BNBUSDT`, `XRPUSDT`, `DOGEUSDT`
Timeframes: `30m`, `1h`, `4h`, `1d` (expanding)

Any symbol/TF outside this list returns **404**.

### KRX Korean stocks (Beta)
**KOSPI 948 + KOSDAQ 1,822 = 2,770 tickers** with daily OHLCV. Evaluation universe = top 200 by trading value ∪ user watchlist ∪ momentum spike ∪ volume spike (`/krx/signals` returns universe top 200 by default).
Ticker format: 6-digit numeric (`005930` Samsung Electronics, `010170` Daehan Optic, etc). Timeframe `1d` (1w expanding).

---

## 6. Python SDK

The SDK is included in this repository at [`sdk/python/`](../sdk/python/).

```bash
git clone https://github.com/gigshow/decker-ai.git
pip install -e decker-ai/sdk/python/
```

> `pip install decker-client` (PyPI) is planned — not yet published.

### Basic usage

```python
from decker_client import Client

with Client(api_key="dk_live_xxx") as client:
    # Latest signal
    sig = client.signals.get_latest("BTCUSDT", timeframe="1h")
    print(f"{sig.direction} | entry={sig.entry_price} target={sig.target_price}")

    # Narrative
    narr = client.signals.get_narrative("BTCUSDT", "4h")
    print(narr.text)

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
        print("Invalid API key — run /apikey reset in Telegram")
    except NotFoundError:
        print("No active signal for this symbol/timeframe")
    except RateLimitError as e:
        print(f"Rate limited — retry in {e.retry_after}s")
```

---

## 7. Error Codes

| HTTP | Code | Cause | Fix |
|------|------|-------|-----|
| 401 | `UNAUTHORIZED` | Missing, invalid, or revoked key | `/apikey reset` in Telegram |
| 404 | `NOT_FOUND` | Symbol/TF not evaluated by engine | Try supported symbols (BTC/ETH/SOL/BNB/XRP/DOGE) and TFs (30m/1h/4h/1d) |
| 422 | `UNPROCESSABLE_ENTITY` | `X-API-Key` header missing entirely | Add the header |
| 429 | `RATE_LIMIT_EXCEEDED` | Daily quota exceeded | Wait for UTC midnight reset or upgrade |
| 5xx | `SERVER_ERROR` | Transient server error | Retry with exponential backoff |

> Missing header → 422. Header present but key invalid → 401.

---

## 8. FAQ

**Q. Can I get an API key without Telegram?**  
A. Not currently. Telegram `/apikey` is the only issuance path. Web dashboard issuance is planned.

**Q. I lost my key.**  
A. Run `/apikey reset` in @deckerclawbot — revokes the old key and issues a new one.

**Q. `operation_gate` is `WATCH` — should I enter?**  
A. No. Only `GO` is an entry signal. `WATCH`/`HOLD` means the engine is observing.

**Q. How do I override the base URL for local testing?**  
A. `Client(api_key="...", base_url="http://localhost:8000")`

**Q. I keep getting 429.**  
A. FREE tier is 100 req/day. Contact via Telegram bot to upgrade to BASIC.

---

*Related: [ONBOARDING_PUBLIC.md](./ONBOARDING_PUBLIC.md) · [AGENT_SKILLS_PUBLIC_SUMMARY.md](./AGENT_SKILLS_PUBLIC_SUMMARY.md)*
