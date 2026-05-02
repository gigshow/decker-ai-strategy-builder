# Decker API Guide

Base URL: `https://api.decker-ai.com`  
OpenAPI spec: [api.decker-ai.com/docs](https://api.decker-ai.com/docs)

---

## Authentication

All `/api/v1/public/*` endpoints require an `X-API-Key` header.

```
X-API-Key: dk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Get your key via Telegram:**
1. Open [@deckerclawbot](https://t.me/deckerclawbot) → send `/start`
2. Send `/apikey` → receive your key
3. Lost it? `/apikey reset` revokes and reissues

> Keys are issued via Telegram only. Web dashboard issuance is planned.

---

## Rate Limits

| Tier | Price | Daily Limit | Headers |
|------|-------|-------------|---------|
| **FREE** | $0 (forever) | 30 calls/day | `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` |
| **PRO** | $20 / month · 7d trial | 10,000 calls/day | same |
| **ENTERPRISE** | Contact us | 100,000+ calls/day · custom | same |

> **Beta**: all authenticated users get **PRO full access** for free during beta (`BETA_TIER_OVERRIDE=PRO`).

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

### Structural Narrative

```
GET /api/v1/public/signals/{symbol}/narrative?timeframe=1h
```

Returns a rule-based plain-language summary of the current structural state.  
Powered by the deterministic state machine — $0 LLM cost.

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

### MTF Signal — 멀티 타임프레임 조합

```
GET /api/v1/public/signals/{symbol}/mtf
```

Returns the multi-timeframe signal combination from the latest snapshot.  
Shows 4h (structure) × 1h (judgment) × 30m (entry) state plus the final assembled decision.  
Source: `consumer_signal_snapshot` (DB-cached, updated every 4h boundary).

```bash
curl "https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/mtf" \
  -H "X-API-Key: dk_live_xxx"
```

```json
{
  "symbol": "BTCUSDT",
  "symbol_trait": "trending",
  "generated_at": "2026-04-27T12:00:00Z",
  "decision": "ENTER",
  "direction": "+",
  "size_factor": 0.8,
  "mtf_quality_by_tf": {
    "4h": "ENTER",
    "1h": "WAIT",
    "30m": "ENTER"
  },
  "entry_price": 94200.0,
  "entry_basis": "close",
  "target_t1": 97500.0,
  "stop_price": 92800.0,
  "stop_note": "structural reference only — not an exchange stop order",
  "risk_reward_ratio": 2.18,
  "progress_pct": 75.0,
  "status": "ACTIVE",
  "current_pnl_pct": 1.24,
  "by_tf": {
    "4h": {
      "timeframe": "4h",
      "direction": "+",
      "action_gate": "GO",
      "c_state": "A_FORMING",
      "signal_quality": "ENTER",
      "cba_energy": "FULL",
      "entry_price": 94200.0,
      "trigger_ts": "2026-04-27T08:00:00Z"
    },
    "1h": {
      "timeframe": "1h",
      "direction": "+",
      "action_gate": "WATCH",
      "c_state": "B_SET",
      "signal_quality": "WAIT",
      "cba_energy": "LOW",
      "entry_price": null,
      "trigger_ts": null
    },
    "30m": {
      "timeframe": "30m",
      "direction": "+",
      "action_gate": "GO",
      "c_state": "A_FORMING",
      "signal_quality": "ENTER",
      "cba_energy": "HIGH",
      "entry_price": 94350.0,
      "trigger_ts": "2026-04-27T11:30:00Z"
    }
  }
}
```

**Fields:**

| Field | Meaning |
|---|---|
| `decision` | Final MTF assembly result: `ENTER` / `WAIT` / `SKIP` |
| `size_factor` | Position size hint: 0.0–1.0. **Contract**: `qty = size_factor × base_qty(symbol)` where `base_qty` is the SDK-defined per-symbol default (BTCUSDT=0.001, ETHUSDT=0.05, SOLUSDT=0.5, BNBUSDT=0.05, XRPUSDT=50.0, default=0.01). `size_factor ≤ 0` → no order. `size_factor > 1` is clamped to 1.0. |
| `mtf_quality_by_tf` | Per-TF signal quality summary |
| `progress_pct` | Lifecycle progress 0–100%: PENDING=CBA stage, ACTIVE=(current−entry)/(target−entry)×100 |
| `stop_price` | Structural reference stop — **not** an exchange stop order |
| `by_tf[tf].c_state` | CBA cycle state: `C_SET` / `B_FORMING` / `B_SET` / `A_FORMING` / `BREAK_±` |
| `by_tf[tf].cba_energy` | Remaining cycle energy: `FULL` / `HIGH` / `MEDIUM` / `LOW` |
| `by_tf[tf].signal_quality` | TF-level decision: `ENTER` / `WAIT` / `SKIP` |

**`progress_pct` interpretation:**

| Range | Stage | Meaning |
|---|---|---|
| 0–32% | Early | Signal just fired, full range ahead |
| 33–66% | Active | Entry window open |
| 67–89% | Late | Consider partial take-profit |
| 90–100% | Target | Near full exit |

---

### Engine State (Live)

```
GET /api/v1/public/state/live?symbol=BTCUSDT&timeframe=1h
```

Returns the raw engine structural state for a symbol and timeframe.  
Includes `c_state`, `action_gate`, `key_direction`, `key_price`, `break_state`, and an optional MTF snapshot.

```bash
curl "https://api.decker-ai.com/api/v1/public/state/live?symbol=BTCUSDT&timeframe=1h" \
  -H "X-API-Key: dk_live_xxx"
```

```json
{
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "c_state": "A_FORMING",
  "action_gate": "GO",
  "key_direction": "+",
  "key_price": 95800,
  "break_state": "BREAK_PLUS",
  "active_trigger": {
    "direction": "+",
    "entry_price": 96000,
    "target_price": 100000,
    "stop_loss": 92000
  },
  "mtf_snapshot": {
    "4h": { "c_state": "B_FORMING", "action_gate": "GO", "key_direction": "+" },
    "1h": { "c_state": "A_FORMING", "action_gate": "GO", "key_direction": "+" },
    "15m": { "c_state": "C_SET",    "action_gate": "WATCH", "key_direction": "+" }
  },
  "generated_at": "2026-04-23T10:00:00Z"
}
```

**MTF query params**: `?include_tfs=15m,1h,4h` (comma-separated, default: 15m,1h,4h)

---

### Market Reading (AI Synthesis)

```
GET /api/v1/public/reading/{symbol}/{primary_tf}?include_tfs=1h,4h,1d
```

Returns a structured AI-readable synthesis view (`reading_view_v0.2`) combining directional bias, bidirectional targets, momentum signals, MTF alignment, execution hint, and engine anomalies.  
Engine core unchanged — read-only synthesis layer above `/state/live`.

```bash
curl "https://api.decker-ai.com/api/v1/public/reading/BTCUSDT/4h?include_tfs=1h,1d" \
  -H "X-API-Key: dk_live_xxx"
```

```json
{
  "schema_version": "reading_view_v0.2",
  "symbol": "BTCUSDT",
  "primary_tf": "4h",
  "bar_ts": "2026-04-23T08:00:00Z",
  "close": 96500,
  "narrative": "BTCUSDT·4h — MTF 정합 · 매수 강",
  "current_state": {
    "c_state": "A_FORMING",
    "key_direction": "+",
    "key_price": 95800,
    "action_gate": "GO"
  },
  "directional_bias": {
    "long_score": 0.72,
    "short_score": 0.18,
    "dominant": "long_strong",
    "confidence": 0.72,
    "reasons": ["4h_structural_+_CONFIRMED", "1d_key_+"]
  },
  "bidirectional_targets": {
    "on_plus_break": { "trigger_close": 97000, "t1": 100000, "distance_pct_t1": 3.63 },
    "on_minus_break": { "trigger_close": 94000, "t1": 90000, "distance_pct_t1": 6.74 }
  },
  "mtf_view": {
    "verdict": "ALIGNED",
    "alignment_score": 0.85,
    "tfs": {
      "4h": { "c_state": "A_FORMING", "key": "+", "bias": "bullish_confirmed" },
      "1h": { "c_state": "B_FORMING", "key": "+", "bias": "bullish_probe" },
      "1d": { "c_state": "C_SET",     "key": "+", "bias": "bullish_continuation" }
    }
  },
  "execution_hint": {
    "stance": "ENTER_LONG",
    "preferred_direction": "long",
    "long_setup": { "entry_trigger": "close > 97000", "t1": 100000, "stop": 94200, "rr": 1.9 },
    "rationale": "MTF 정합 + directional_bias long_strong"
  },
  "engine_anomalies_detected": []
}
```

**Valid timeframes**: `15m` `30m` `1h` `4h` `8h` `1d` `1w`

---

### Market Reading — LLM Explain

```
GET /api/v1/public/reading/{symbol}/{primary_tf}/explain?provider=claude
```

Passes `reading_view_v0.2` to an LLM (Claude or OpenAI) and returns a Korean-language Q1–Q4 narrative.  
Falls back to rule-based rendering if LLM is unavailable.

```bash
curl "https://api.decker-ai.com/api/v1/public/reading/BTCUSDT/4h/explain" \
  -H "X-API-Key: dk_live_xxx"
```

```json
{
  "reading_view": { "...": "reading_view_v0.2 전체" },
  "narrative": "BTCUSDT 4h — MTF 정합, 매수 우세...\n\n**Q1 매수/매도**: ...\n**Q4 권장 행동**: ...",
  "source": "claude",
  "model": "claude-opus-4-7",
  "cache_hit": true
}
```

**Query params**:
- `provider`: `claude` | `openai` | `auto` (default: `auto` — prefers Claude if available)
- `include_tfs`: comma-separated TFs for MTF context
- `extra`: additional instructions appended to the prompt

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

### Signal Stats (No Auth)

```
GET /api/v1/public/stats
```

No auth required. Returns 30-day engine signal activity across symbols and timeframes.  
60-second cache.

```bash
curl https://api.decker-ai.com/api/v1/public/stats
```

```json
{
  "period_days": 30,
  "symbols": [
    {
      "symbol": "BTCUSDT",
      "total_evaluations": 720,
      "action_gate_distribution": { "GO": 312, "WATCH": 264, "HOLD": 144 },
      "last_evaluation": "2026-04-23T10:00:00Z"
    }
  ],
  "covered_combinations": 12
}
```

---

### Demo (No Auth)

```
GET /api/v1/public/demo
```

No API key required. IP rate limit: 10 req/IP/day.  
Returns live BTCUSDT 1h signal for quick exploration.

```bash
curl https://api.decker-ai.com/api/v1/public/demo
```

```json
{
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "direction": "long",
  "entry_price": 96000,
  "target_price": 100000,
  "stop_loss": 92000,
  "progress_pct": 66,
  "operation_context": { "action_gate": "GO" },
  "narrative": "B-leg confirmed. Structural bias long."
}
```

---

## Python SDK

```bash
pip install decker-client    # Python 3.9+
```

```python
from decker_client import Client, RateLimitError

with Client(api_key="dk_live_xxx") as client:
    # Structural narrative (rule-based)
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

### `action_gate`

Three modes from the structural state machine:

| Gate | Meaning |
|------|---------|
| `GO` | Structural conditions favorable — entry or hold |
| `WATCH` | Transition — wait for confirmation |
| `HOLD` | Counter-trend risk — reduce or exit |

### `c_state` (CBA cycle)

The engine tracks a C → B → A cycle for each structural swing:

| c_state | Meaning |
|---------|---------|
| `C_SET` | New cycle started — C leg set |
| `B_FORMING` | B leg forming |
| `B_SET` | B leg complete |
| `A_FORMING` | A leg forming — trigger zone |
| `BREAK_PLUS` | Upward structural break confirmed |
| `BREAK_MINUS` | Downward structural break confirmed |

### `mtf_view.verdict`

| verdict | Meaning |
|---------|---------|
| `ALIGNED` | All TFs in same key direction |
| `CONFLICT` | Upper and lower TFs in opposite directions |
| `MIXED` | Partial agreement across TFs |
| `NEUTRAL` | Insufficient data |

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
