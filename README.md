<!--
  Keywords: AI trading signal, crypto market state engine, structural analysis,
  algorithmic trading API, Telegram trading bot, Python SDK, decker-client,
  deterministic signal, progress_pct, operation rules, GO WATCH HOLD
-->
<div align="center">

<img src="assets/decker_claw_mascot_v1.png" width="80" alt="DeckerClaw" />

# Decker AI

**Crypto market state engine. Not "buy/sell" — structural context.**

*Signal → State → Strategy → **Skill Overlay** (per-user). Every output is traceable, reproducible, zero-LLM-cost on the rules path.*

[![GitHub Stars](https://img.shields.io/github/stars/gigshow/decker-ai?style=flat-square&color=DAA520)](https://github.com/gigshow/decker-ai/stargazers)
[![API Docs](https://img.shields.io/badge/API-docs-00C853?style=flat-square)](https://api.decker-ai.com/docs)
[![MCP Server](https://img.shields.io/badge/MCP-server-4D9FFF?style=flat-square)](https://api.decker-ai.com/api/v1/mcp/health)
[![SDK](https://img.shields.io/badge/SDK-sdk%2Fpython-3775A9?style=flat-square&logo=python&logoColor=white)](sdk/python/)
[![Telegram](https://img.shields.io/badge/Telegram-DeckerClaw-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://t.me/deckerclawbot)
[![Kakao Channel](https://img.shields.io/badge/Kakao-Channel-FEE500?style=flat-square&logo=kakaotalk&logoColor=000000)](https://pf.kakao.com/_RxlxjVX)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[📖 API Docs](https://api.decker-ai.com/docs) · [🤖 Telegram Bot](https://t.me/deckerclawbot) · [🧠 MCP Server](#mcp-server-way-e) · [📦 Python SDK](sdk/python/) · [🗺 Roadmap](docs/roadmap.md)

</div>

---

## Start here

| You are | Best path |
|---------|-----------|
| **Crypto trader** — want signals on your phone | [Telegram Bot](https://t.me/deckerclawbot) → type `/btc` |
| **Developer** — building a bot, app, or script | [3-step quickstart below](#-quickstart-3-steps) |
| **AI agent user** — adding Decker to Claude / Cursor / Codex | [MCP Server (Way E)](#mcp-server-way-e) |
| **AI agent builder** — adding Decker as a skill | [OpenClaw skills](docs/openclaw_skills/) |
| **Self-host / deploy your own** | [turnkey/](turnkey/) — Railway one-click |

---

## ⚡ Try it right now (no sign-up)

```bash
curl https://api.decker-ai.com/api/v1/public/demo
```

Returns live BTCUSDT 1h signal — no API key needed.

---

## ⚡ Quickstart (3 steps)

### Step 1 — Get your API key (30 seconds)

1. Open Telegram → [@deckerclawbot](https://t.me/deckerclawbot)
2. Send `/start`
3. Send `/apikey` → receive `dk_live_xxxxxxxxxxxxxxxxxxxxxxxx`

> **Lost your key?** Run `/apikey reset` in the bot — revokes and reissues.

### Step 2 — First call

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
  "progress_pct": 67.3,
  "operation_gate": "GO",
  "generated_at": "2026-04-23T05:00:00Z"
}
```

### Step 3 — Python SDK (optional)

```bash
git clone https://github.com/gigshow/decker-ai.git
pip install -e decker-ai/sdk/python/
```

> `pip install decker-client` (PyPI) — 배포 준비 중.

```python
from decker_client import Client

with Client(api_key="dk_live_xxx") as client:
    sig = client.signals.get_latest("BTCUSDT", timeframe="1h")
    print(f"{sig.direction} | entry={sig.entry_price} | progress={sig.progress_pct}%")

    narr = client.signals.get_narrative("BTCUSDT", "4h")
    print(narr.text)
```

> `pip install decker-client` (PyPI) is planned — not yet published. Use the local install above until then.  
> Full SDK docs: [sdk/python/README.md](sdk/python/README.md)

---

## What is Decker?

Most signal tools ask: *"Up or down?"*  
Decker asks: ***"Where are we in the current structural cycle — and what's the next optimal move?"***

```
Raw OHLCV candles
  ↓  Sequence Labeler  →  every candle gets a role (anchor / test / signal)
  ↓  State Machine     →  C_SET → B_FORMING → B_SET → A_FORMING → W_PENDING
  ↓  Operation Gate    →  GO · WATCH · HOLD  (not binary — three modes)
  ↓  RULES Engine      →  9-layer YAML rulebook → strategy + ranked choices
  ↓  AI Consultation   →  LLM translates structural state → plain language
  ↓
"67% progress. B-leg confirmed. Recommended: 30% partial TP or hold to target."
```

**No price prediction. No black box. Every output traces to a formal structural cause.**

---

## The `progress_pct` System

Every signal has a lifecycle — from formation (0%) to target (100%).

```
Entry                                                           Target
  │                                                                │
  0%──────────33%──────────50%──────────67%──────────83%────────100%
  │           │            │            │             │            │
 Wait       Entry        Active       Late TP      Final TP     Exit
```

**Example: progress_pct = 67%**

```
[████████████████████████████████████████████░░░░░░░░░░░░░░░░░░░] 67%
```

```
Typical tool: BUY
Decker:       BUY + 67% progress
              → "The move is real, but 2/3 of the range is already done.
                 Consider partial entry or wait for a pullback."
```

| progress_pct | Stage | Recommended posture |
|---|---|---|
| 0–32% | Early | Wait or prepare entry |
| 33–66% | Active | Entry window, manage risk |
| 67–89% | Late | Partial take-profit, reduce size |
| 90–100% | At target | Prepare full exit |

---

## GO · WATCH · HOLD

Unlike binary BUY/SELL signals, Decker has three operation gates:

| Gate | Meaning | What to do |
|------|---------|------------|
| **GO** | Structure confirmed, entry conditions met | Enter (if within progress window) |
| **WATCH** | Signal forming, not yet confirmed | Monitor — no entry yet |
| **HOLD** | Active position, no new entry signal | Hold current position |

> **WATCH ≠ SELL.** It means "the engine is observing — not ready to signal an entry yet."  
> This is the gate that most signal tools skip. It's why users enter too early.

---

## What Makes Decker Different

| | Typical AI Signal | Decker |
|---|---|---|
| Signal source | ML / LLM price prediction | **Deterministic state machine** |
| Output | BUY / SELL | `progress_pct` + `operation_gate` + ranked choices |
| LLM role | Makes the call | **Explains the structural state** |
| Auditability | ❌ Black box | ✅ Every signal has a `trace_id` |
| LLM cost per signal | High (every call) | **$0 on the rules path** |
| Reproducibility | ❌ | ✅ Same input → same output, always |

---

## API Reference

Full OpenAPI spec at [api.decker-ai.com/docs](https://api.decker-ai.com/docs).

**Supported symbols**: `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `BNBUSDT`, `XRPUSDT`, `DOGEUSDT`  
**Supported timeframes**: `30m`, `1h`, `4h`, `1d`

> Symbols or timeframes outside this list return `404`. More symbols expanding.

### Public endpoints (require `X-API-Key` header)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/public/auth/verify` | Verify API key + get tier |
| `GET` | `/api/v1/public/health` | Liveness check (no auth) |
| `GET` | `/api/v1/public/signals/{symbol}/latest` | Latest signal (direction, entry, target, stop, progress) |
| `GET` | `/api/v1/public/signals/{symbol}/narrative` | Rule-based / LLM structural narrative |
| `GET` | `/api/v1/public/signals/{symbol}/mtf` | MTF consumer signal + Skill Overlay applied |
| `GET` | `/api/v1/public/state/live` | Engine state (c_state · gate · MTF) |
| `GET` | `/api/v1/public/reading/{sym}/{tf}` | AI reading view v0.2 (8 blocks) |
| `GET` | `/api/v1/mcp/sse` | **MCP server SSE handshake** ([Way E](#mcp-server-way-e)) |
| `POST` | `/api/v1/mcp/messages` | MCP JSON-RPC 2.0 (4 tools) |

### Auth

```
X-API-Key: dk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Keys are issued via Telegram `/apikey` — **not** from the web UI. See [DEVELOPER_API_GUIDE.md](docs/DEVELOPER_API_GUIDE.md).

### Rate Limits

| Tier | Daily limit |
|------|------------|
| FREE | 100 req/day |
| BASIC | 10,000 req/day |
| PREMIUM | 100,000 req/day |

Every response includes `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.  
Exceeded → HTTP 429 + `Retry-After`.

---

## Python SDK

The SDK is included in this repository at [`sdk/python/`](sdk/python/).

```bash
git clone https://github.com/gigshow/decker-ai.git
pip install -e decker-ai/sdk/python/
```

```python
from decker_client import Client, RateLimitError, AuthError, NotFoundError

with Client(api_key="dk_live_xxx") as client:
    # Latest signal
    sig = client.signals.get_latest("BTCUSDT", timeframe="1h")
    print(f"{sig.direction} | entry={sig.entry_price} | target={sig.target_price}")
    print(f"progress: {sig.progress_pct}% | gate: {sig.operation_gate}")

    # Narrative
    narr = client.signals.get_narrative("BTCUSDT", "4h")
    print(narr.text)

    # Rate limit info
    rl = client.last_rate_limit
    print(f"{rl.remaining}/{rl.limit} remaining today")
```

**Error handling:**

```python
try:
    sig = client.signals.get_latest("BTCUSDT")
except AuthError:
    print("Invalid API key — run /apikey reset in Telegram")
except NotFoundError:
    print("No active signal for this symbol/timeframe")
except RateLimitError as e:
    print(f"Rate limited — retry in {e.retry_after}s")
```

> `pip install decker-client` (PyPI) is planned — not yet published.  
> Full SDK reference: [sdk/python/README.md](sdk/python/README.md) · [Developer API Guide](docs/DEVELOPER_API_GUIDE.md)

---

## Performance

*Backtest results, rules-path evaluation. Past performance does not guarantee future results.*

| Metric | Result | Condition |
|--------|--------|-----------|
| Win Rate | 61–75% | Ranging market |
| Win Rate | 70%+ | Trending market |
| Avg Profit | 4–10% | Per signal |
| Avg Loss | 1–2% | Tight stop-loss |
| Max Drawdown | < 9% | Capital preservation |
| Signal Frequency | 1–3 / day | Per symbol |

Details: [Signal Performance](docs/signal-performance.md)

---

## Five Ways to Use Decker AI

All five ways share the same data, auth, and **Skill Overlay** (per-user trading strategy: `conservative_v0` / `standard_v0` / `aggressive_v0` + custom). Whatever channel you use, the same skill applies — Telegram alerts, REST responses, MCP tool results stay aligned.

| Way | Who | How |
|------|-----|-----|
| **Way 1. Telegram Bot** | Traders | [@deckerclawbot](https://t.me/deckerclawbot) → natural language |
| **Way 2. OpenClaw skill** | AI agent devs | Add Decker skill → `web_fetch` → API responses |
| **Way C. REST API + SDK** | Any language / Python | `X-API-Key` header → [api.decker-ai.com/docs](https://api.decker-ai.com/docs) · `pip install -e sdk/python/` |
| **Way D. Self-host** | Self-hosters | [turnkey/](turnkey/) — Railway one-click |
| **Way E. MCP Server** ⭐ NEW | Claude / Cursor / Codex users | [MCP handshake](#mcp-server-way-e) → 4 tools, JSON-RPC 2.0, SSE transport |

---

## MCP Server (Way E)

Add Decker AI to any [MCP-compatible](https://modelcontextprotocol.io/) AI agent (Claude Desktop, Cursor, Codex). Same `X-API-Key`, same Skill Overlay, same rulebook.

**Endpoint** (live · 2026-05-02):

```
GET  https://api.decker-ai.com/api/v1/mcp/sse           (SSE handshake)
POST https://api.decker-ai.com/api/v1/mcp/messages      (JSON-RPC 2.0)
GET  https://api.decker-ai.com/api/v1/mcp/health        (monitoring)
```

**4 tools** (auto-includes per-user Skill Overlay):

| Tool | Purpose |
|------|---------|
| `decker.get_signals` | Active MTF consumer signals (filter by symbol / min progress / gate) |
| `decker.get_reading` | AI reading view v0.2 (8 blocks: state · MTF · risk · narrative) |
| `decker.get_user_skills` | Catalog of trading skills + currently active overlay |
| `decker.set_skill_overlay` | Switch overlay on the fly (`conservative_v0` → `aggressive_v0`) |

**Quick test** (Claude Desktop config snippet):

```json
{
  "mcpServers": {
    "decker-ai": {
      "url": "https://api.decker-ai.com/api/v1/mcp/sse",
      "headers": { "X-API-Key": "dk_live_xxx" }
    }
  }
}
```

Spec: [docs/mcp-server.md](docs/mcp-server.md) (in monorepo: `docs/MCP_SERVER_SPEC_2026-05-02.md`)

---

## Docs

| Document | |
|----------|-|
| [Developer API Guide](docs/DEVELOPER_API_GUIDE.md) | Auth · Rate Limits · SDK · FAQ — **start here if you're building** |
| [Quick Start](docs/quickstart.md) | 3-step guide for each path |
| [API Guide](docs/api-guide.md) | Full endpoint reference |
| [Architecture](docs/architecture.md) | Pipeline, state engine, modules |
| [Model & Algorithm](docs/model.md) | How the signal engine works |
| [Operation Rules](operation_rules/RULES.yaml) | Open YAML rulebook (v2.4.7+) |
| [Signal Performance](docs/signal-performance.md) | Backtest & live metrics |
| [Article Series (1–15)](docs/medium/README.md) | Deep dives |
| [Roadmap](docs/roadmap.md) | What's next |
| [llms.txt](llms.txt) | LLM/AI agent discovery manifest |

**Concepts:** [Sequence Engine](concept/sequence_engine.md) · [Labeling Algorithm](concept/labeling_algorithm.md) · [Market State Theory](concept/market_state_theory.md)

---

## Article Series

**Part 1 — Foundations (1–10):** State Engine, signal lifecycle, YAML rulebook, multi-TF alignment, $0-LLM-cost architecture.

**Part 2 — Context Engine (11–15):** How markets speak in sequences, session state machine, GO/WATCH/HOLD gate, AI as explainer vs decision-maker.

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

> This repository is the public documentation, SDK, samples, and community hub for Decker AI.  
> Production application code runs in a private monorepo.  
> **Available here**: [Python SDK](sdk/python/) · [API samples](samples/) · [RULES.yaml](operation_rules/RULES.yaml) · [Architecture docs](docs/architecture.md) · [Article series](docs/medium/README.md)
