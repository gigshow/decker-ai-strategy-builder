<!--
  Keywords: AI trading signal, crypto market state engine, structural analysis,
  algorithmic trading API, Telegram trading bot, Python SDK, decker-client,
  deterministic signal, progress_pct, operation rules, GO WATCH HOLD
-->
<div align="center">

<img src="assets/decker_claw_mascot_v1.png" width="80" alt="DeckerClaw" />

# Decker AI Strategy Builder

**Crypto market state engine. Not "buy/sell" — structural context.**

*Signal → State → Strategy. Every output is traceable, reproducible, $0-LLM-cost on the rules path.*

[![GitHub Stars](https://img.shields.io/github/stars/gigshow/decker-ai-strategy-builder?style=flat-square&color=DAA520)](https://github.com/gigshow/decker-ai-strategy-builder/stargazers)
[![API Docs](https://img.shields.io/badge/API-docs-00C853?style=flat-square)](https://api.decker-ai.com/docs)
[![PyPI](https://img.shields.io/badge/PyPI-decker--client-3775A9?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/decker-client/)
[![Telegram](https://img.shields.io/badge/Telegram-DeckerClaw-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://t.me/deckerclawbot)
[![Kakao Channel](https://img.shields.io/badge/Kakao-Channel-FEE500?style=flat-square&logo=kakaotalk&logoColor=000000)](https://pf.kakao.com/_RxlxjVX)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[📖 API Docs](https://api.decker-ai.com/docs) · [🔑 Get API Key](https://decker-ai.com) · [📦 PyPI](https://pypi.org/project/decker-client/) · [🤖 Telegram Bot](https://t.me/deckerclawbot) · [🗺 Roadmap](docs/roadmap.md)

</div>

---

## ⚡ 60-second quickstart

```bash
pip install decker-client
```

```python
from decker_client import Client

client = Client(api_key="dk_live_xxx")   # get your key → decker-ai.com

# Get the LLM narrative for BTCUSDT 1h
narr = client.signals.get_narrative("BTCUSDT", "1h")
print(narr.text)
# → "B-leg confirmed at 66% progress. Counter-swing absorbed.
#    Recommend: 30% partial TP or hold to target."

# Latest signal
sig = client.signals.get_latest("BTCUSDT")
print(sig.direction, sig.entry_price, sig.target_price)
# → long  96000  100000
```

**Or with curl:**
```bash
curl -X POST https://api.decker-ai.com/api/v1/public/auth/verify \
  -H "X-API-Key: dk_live_xxx"
# → {"valid": true, "tier": "free", "rate_limit": 100}

curl https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/narrative?timeframe=1h \
  -H "X-API-Key: dk_live_xxx"
```

[**Get your API key →**](https://decker-ai.com) · [Full API reference →](https://api.decker-ai.com/docs)

---

## What is Decker?

Most signal tools ask: *"Up or down?"*  
Decker asks: ***"Where are we in the current structural cycle — and what's the optimal next move?"***

```
Raw OHLCV candles
  ↓  Sequence Labeler  →  every candle: role (anchor / test / signal)
  ↓  State Machine     →  session FSM: C_SET → B_FORMING → B_SET → A_FORMING → W_PENDING
  ↓  Operation Gate    →  GO · WATCH · HOLD  (not binary — three modes)
  ↓  RULES Engine      →  9-layer YAML rulebook → strategy + ranked choices
  ↓  AI Consultation   →  LLM translates structural state → plain language
  ↓
"66% progress. B-leg confirmed. Recommended: 30% partial TP or hold."
```

**No price prediction. No black box. Every output traces to a formal structural cause.**

---

## API Reference

Full OpenAPI spec at [api.decker-ai.com/docs](https://api.decker-ai.com/docs).

### Public endpoints (require `X-API-Key` header)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/public/auth/verify` | Verify API key + get tier info |
| `GET` | `/api/v1/public/health` | Service liveness (no auth) |
| `GET` | `/api/v1/public/signals/{symbol}/narrative` | LLM structural narrative |
| `GET` | `/api/v1/public/signals/{symbol}/latest` | Latest signal (direction, entry, target, stop) |

### Other endpoints (beta — key optional)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/signals/{symbol}/state` | Signal state + `progress_pct` + `operation_gate` |
| `GET` | `/api/v1/signals/{symbol}/strategy` | Strategy from rulebook |
| `GET` | `/api/v1/signals/{symbol}/consultation` | AI consultation (rationale + choices) |
| `GET` | `/api/v1/llm/opportunities` | LLM insight feed (conviction, choices, tf_alignment) |
| `GET` | `/api/v1/judgment/coverage` | 20 symbols × 6 timeframes coverage |

---

## Auth & Rate Limits

All `/api/v1/public/*` endpoints require:

```
X-API-Key: dk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Get your key at [decker-ai.com](https://decker-ai.com) → Settings → API Keys.

| Tier | Daily limit | Response headers |
|------|------------|-----------------|
| **FREE** | 100 req/day | `X-RateLimit-Remaining` · `X-RateLimit-Reset` |
| **BASIC** | 10,000 req/day | same |
| **PREMIUM** | 100,000 req/day | same |

When the limit is exceeded → `HTTP 429` + `Retry-After` header.

---

## Python SDK

> **New here?** If `pip install decker-client` fails, the **PyPI package may not be published yet** (roadmap: public SDK + PyPI). Use **[REST + curl](docs/quickstart.md#path-b--rest-api)** or **[samples](samples/README.md)** with your API key first — they track production today.

```bash
pip install decker-client    # Python 3.9+  (when available on PyPI)
```

```python
from decker_client import Client, RateLimitError

with Client(api_key="dk_live_xxx") as client:

    # Narrative
    narr = client.signals.get_narrative("BTCUSDT", "1h")
    print(narr.text, narr.generated_at)

    # Latest signal
    sig = client.signals.get_latest("ETHUSDT")
    print(f"{sig.direction} | entry={sig.entry_price} target={sig.target_price}")

    # Health
    health = client.health.check()
    print(health.ok)  # True

    # Rate limit info after any request
    rl = client.last_rate_limit
    print(f"{rl.remaining}/{rl.limit} remaining today")

    # Handle limits
    try:
        narr = client.signals.get_narrative("SOLUSDT", "4h")
    except RateLimitError as e:
        print(f"Retry in {e.retry_after}s")
```

SDK source: private platform monorepo `sdk/python/decker_client` (not vendored in this public repo). PyPI: [decker-client](https://pypi.org/project/decker-client/) when published — see [roadmap](docs/roadmap.md).

---

## What Makes Decker Different

| | Typical AI Signal | Decker |
|---|---|---|
| Signal source | ML / LLM price prediction | **Deterministic state machine** |
| Output | BUY / SELL | `progress_pct` + `operation_gate` + ranked choices |
| LLM role | Makes the call | **Explains the structural state** |
| Auditability | ❌ Black box | ✅ Every signal has a `trace_id` |
| LLM cost per signal | High | **$0 on the rules path** |
| Reproducibility | ❌ | ✅ Same input → same output, always |

---

## The `progress_pct` System

Every signal has a lifecycle — from formation (0%) to target (100%).

```
Signal birth (0%) ────── Entry zone ────── Midpoint ────── Target (100%)
                                ↑                    ↑
                         "GO: enter now"     "Consider partial TP"
```

| progress_pct | State | Recommended posture |
|---|---|---|
| 0–32% | Early | Wait or prepare entry |
| 33–66% | Active | Entry window, risk management begins |
| 67–89% | Late | Partial take-profit, reduce size |
| 90–100% | At target | Prepare full exit |

> Typical tool: **BUY**  
> Decker: **BUY + 67% progress** = *"The move is real, but the easy money is already in"*

---

## Three Ways to Use Decker

| Path | Who | How |
|------|-----|-----|
| **A. Python SDK** | API / backend developers | `pip install decker-client` → 60 sec start |
| **B. REST API** | Any language | `X-API-Key` header → [api.decker-ai.com/docs](https://api.decker-ai.com/docs) |
| **C. Telegram bot** | Traders | [@deckerclawbot](https://t.me/deckerclawbot) → natural language |
| **D. OpenClaw skill** | AI agent devs | Add Decker skill → `web_fetch` → API responses |
| **E. Self-host** | Self-hosters | [turnkey/](turnkey/) — Railway one-click |

---

## Docs

| Document | |
|----------|-|
| [Developer API Guide](docs/DEVELOPER_API_GUIDE.md) | Auth · Rate Limits · SDK · FAQ — **start here if you're building** |
| [API Guide](docs/api-guide.md) | Full endpoint reference |
| [Quick Start](docs/quickstart.md) | 3-step guide |
| [Architecture](docs/architecture.md) | Pipeline, state engine, modules |
| [Model & Algorithm](docs/model.md) | How the signal engine works |
| [Operation Rules](operation_rules/RULES.yaml) | Open YAML rulebook (v2.4.7+) |
| [Signal Performance](docs/signal-performance.md) | Backtest & live metrics |
| [Article Series (1–15)](docs/medium/README.md) | Deep dives |
| [Roadmap](docs/roadmap.md) | What's next |
| [llms.txt](llms.txt) | AI/LLM discovery manifest |

**Concepts:** [Sequence Engine](concept/sequence_engine.md) · [Labeling Algorithm](concept/labeling_algorithm.md) · [Market State Theory](concept/market_state_theory.md)

---

## Performance

| Metric | Result |
|--------|--------|
| Win Rate | 61–68% |
| Avg Profit | 5–12% |
| Max Drawdown | < 9% |
| Range-market monthly | 20–30% |
| Signal Frequency | 1–3 / day |

*Structural cycle evaluation, not pattern matching. Past performance does not guarantee future results.*  
Details: [Signal Performance](docs/signal-performance.md) · [Model & Algorithm](docs/model.md)

---

## Article Series

**Part 1 — Foundations (Articles 1–10):** State Engine, signal lifecycle, YAML rulebook, multi-TF alignment, $0-LLM-cost architecture.

**Part 2 — Context Engine (Articles 11–15):** How markets speak in sequences, session state machine, GO/WATCH/HOLD gate, AI as explainer vs decision-maker.

→ [Read the full series](docs/medium/README.md)

---

## Links

| | |
|-|-|
| **Service** | https://decker-ai.com |
| **API Docs** | https://api.decker-ai.com/docs |
| **Telegram bot** | https://t.me/deckerclawbot |
| **Kakao channel** | https://pf.kakao.com/_RxlxjVX |

---

> This repository is the public documentation, samples, SDK, and community hub for Decker AI.  
> Production application code runs in a private monorepo.  
> **Available here**: Python SDK, API samples, RULES.yaml, architecture docs, article series.
