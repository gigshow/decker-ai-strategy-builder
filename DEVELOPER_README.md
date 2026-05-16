<div align="center">

<img src="assets/decker_claw_owl_v1.svg" width="72" alt="DeckerClaw" />

# Decker AI — Developer Guide

Build with Decker: REST API · MCP server · Python SDK · OpenClaw skill.

[Main README](README.md) · [API docs](https://api.decker-ai.com/docs) · [DEVELOPER_API_GUIDE.md](docs/DEVELOPER_API_GUIDE.md)

</div>

---

## Contents

- [API quickstart (3 steps)](#api-quickstart-3-steps)
- [Endpoints](#endpoints)
- [Auth](#auth)
- [Rate limits](#rate-limits)
- [MCP server (Way E) — full guide](#mcp-server-way-e)
- [Python SDK](#python-sdk)
- [OpenClaw skill (Way 2)](#openclaw-skill-way-2)
- [Self-host (Way D)](#self-host-way-d)
- [Supported symbols & timeframes](#supported-symbols--timeframes)
- [FAQ](#faq)

---

## API quickstart (3 steps)

### 1. Get your API key — 30 seconds

1. Open Telegram → [@deckerclawbot](https://t.me/deckerclawbot)
2. Send `/start`
3. Send `/apikey` → receive `dk_live_xxxxxxxxxxxxxxxxxxxxxxxx`

> **Lost your key?** Run `/apikey reset` in the bot — revokes and reissues.

### 2. First call

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

### 3. Try without auth

```bash
curl https://api.decker-ai.com/api/v1/public/demo
```

Returns a live BTCUSDT 1h signal — no API key needed. Useful for smoke testing.

---

## Endpoints

Full OpenAPI spec: **[api.decker-ai.com/docs](https://api.decker-ai.com/docs)**.

### Public — `X-API-Key` required (except `/health` and `/demo`)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/public/auth/verify` | Verify API key + get tier |
| `GET`  | `/api/v1/public/health` | Liveness (no auth) |
| `GET`  | `/api/v1/public/demo` | Live demo signal (no auth) |
| `GET`  | `/api/v1/public/signals/{symbol}/latest` | Latest signal (direction, entry, target, stop, progress) |
| `GET`  | `/api/v1/public/signals/{symbol}/narrative` | Rule-based / LLM structural narrative |
| `GET`  | `/api/v1/public/signals/{symbol}/mtf` | MTF consumer signal + Skill Overlay applied |
| `GET`  | `/api/v1/public/state/live` | Engine state (c_state · gate · MTF) |
| `GET`  | `/api/v1/public/reading/{sym}/{tf}` | AI reading view v0.2 (8 blocks) |

### KRX (Beta — free)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/public/krx/signals` | KOSPI + KOSDAQ batch with 4 actions (ADD/HOLD/REDUCE/EXIT) |
| `GET` | `/api/v1/public/krx/market` | Market macro + signal summary |

```bash
curl -H "X-API-Key: $KEY" \
  'https://api.decker-ai.com/api/v1/public/krx/signals?gate=GO&market=KOSPI&limit=10'
```

Korean-market context: DART filing recency · KOSPI200 RS · price-limit lock state · foreign net-buy*.
*Foreign / market-cap / fundamentals = KIS Open API integration in Q3–Q4 2026.

KRX details: [`docs/krx/KRX_BUSINESS_MODEL_AND_ROADMAP_2026-05-09.md`](docs/krx/KRX_BUSINESS_MODEL_AND_ROADMAP_2026-05-09.md).

### MCP

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/api/v1/mcp/sse` | SSE handshake ([Way E](#mcp-server-way-e)) |
| `POST` | `/api/v1/mcp/messages` | JSON-RPC 2.0 (4 tools) |
| `GET`  | `/api/v1/mcp/health` | MCP server health |

---

## Auth

```
X-API-Key: dk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Keys are issued via Telegram `/apikey` — **not** from the web UI. See [DEVELOPER_API_GUIDE.md](docs/DEVELOPER_API_GUIDE.md) for full auth flow, scopes, and rotation.

---

## Rate limits

Every response includes:

```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 17
X-RateLimit-Reset: 1735689600
```

Exceeded → HTTP `429` with `Retry-After`.

| Tier | Daily limit | MCP | Auto-trade |
|------|-------------|-----|-----------|
| **FREE** | 30 calls / day | read-only (1d cache) | ❌ |
| **PRO** | 10,000 / day | full (4 tools) | virtual + real |
| **ENTERPRISE** | 100,000+ / day · custom | full + per-org skill catalog | + custom integration |

> **Beta (now):** authenticated users get **PRO for free** via `BETA_TIER_OVERRIDE=PRO`. No payment required.

---

## MCP Server (Way E)

Add Decker AI to any [MCP-compatible](https://modelcontextprotocol.io/) AI agent — Claude Desktop, Cursor, Codex, or your own MCP client. Same `X-API-Key`, same Skill Overlay, same rulebook.

### Endpoints (live · 2026-05-02)

```
GET  https://api.decker-ai.com/api/v1/mcp/sse           (SSE handshake)
POST https://api.decker-ai.com/api/v1/mcp/messages      (JSON-RPC 2.0)
GET  https://api.decker-ai.com/api/v1/mcp/health        (monitoring)
```

### Claude Desktop config

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

Drop into `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or the equivalent path on Windows / Linux, then restart Claude Desktop. Decker tools appear in the tool picker.

### Cursor / Codex / generic MCP client

Same URL + headers. Most MCP clients accept an HTTP-SSE transport definition; consult your client's docs. The handshake is plain SSE — no custom transport required.

### 4 tools (auto-applies your active Skill Overlay)

| Tool | Purpose | Key params |
|------|---------|-----------|
| `decker.get_signals` | Active MTF consumer signals | `symbol?`, `min_progress?`, `gate?` (GO/WATCH/HOLD) |
| `decker.get_reading` | AI reading view v0.2 (8 blocks: state · MTF · risk · narrative) | `symbol`, `timeframe` |
| `decker.get_user_skills` | Catalog of trading skills + active overlay | — |
| `decker.set_skill_overlay` | Switch overlay on the fly | `overlay` (`conservative_v0` \| `standard_v0` \| `aggressive_v0`) |

All tool calls inherit the API key's tier (FREE = read-only with cache, PRO = full). Tool responses are JSON-RPC 2.0; errors return standard `{ "error": { "code": ..., "message": ... } }`.

### Smoke test (curl)

```bash
# 1. Handshake (will hang — Ctrl+C after seeing "endpoint")
curl -N -H "X-API-Key: dk_live_xxx" \
  https://api.decker-ai.com/api/v1/mcp/sse

# 2. List tools
curl -X POST https://api.decker-ai.com/api/v1/mcp/messages \
  -H "X-API-Key: dk_live_xxx" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# 3. Call a tool
curl -X POST https://api.decker-ai.com/api/v1/mcp/messages \
  -H "X-API-Key: dk_live_xxx" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"decker.get_signals","arguments":{"symbol":"BTCUSDT"}}}'
```

Full spec: [docs/mcp-server.md](docs/mcp-server.md).

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
    sig = client.signals.get_latest("BTCUSDT", timeframe="1h")
    print(f"{sig.direction} | entry={sig.entry_price} | progress={sig.progress_pct}%")

    narr = client.signals.get_narrative("BTCUSDT", "4h")
    print(narr.text)

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

> `pip install decker-client` (PyPI) is planned — not yet published. Use the local install above until then.
> Full reference: [sdk/python/README.md](sdk/python/README.md).

---

## OpenClaw skill (Way 2)

Add Decker as a skill to your OpenClaw agent — `web_fetch` against the REST API, with the rulebook applied server-side.

Skill packages live in [`docs/openclaw_skills/`](docs/openclaw_skills/).

---

## Self-host (Way D)

One-click Railway deploy of the API + worker stack lives in [`turnkey/`](turnkey/). Bring your own database; the rulebook ships in `operation_rules/RULES.yaml`.

---

## Supported symbols & timeframes

**Crypto (GA):** `BTCUSDT` · `ETHUSDT` · `SOLUSDT` · `BNBUSDT` · `XRPUSDT` · `DOGEUSDT`
**Timeframes:** `30m`, `1h`, `4h`, `1d`

**KRX (Beta, free):** KOSPI 948 + KOSDAQ 1,822 = **2,770 tickers**. Universe = top 200 by trading value ∪ user watchlist ∪ momentum spike ∪ volume spike. Timeframe `1d` only (1w expanding). Daily evaluation at 16:30 KST.

Symbols / timeframes outside this list return `404`. More symbols expanding.

---

## FAQ

**Where do I get an API key?**
Telegram only: [@deckerclawbot](https://t.me/deckerclawbot) → `/apikey`. Not from the web UI.

**Why no `pip install decker-client`?**
PyPI publish is planned; not yet shipped. Until then, install from this repo with `pip install -e sdk/python/`.

**Why is `WATCH` a separate gate?**
Most tools collapse the "signal forming but not confirmed" state into either `BUY` (too early) or `nothing` (silent). Decker keeps it explicit so you can monitor without acting.

**Does the LLM ever override the rules path?**
No. The LLM only **explains** the structural state produced by the deterministic engine. The rules path runs at `$0` LLM cost; the explanation layer is opt-in.

**How is auto-trade gated?**
PRO tier + per-symbol skill enabled in your Strategy preset + execution_mode (`paper` vs `live`) set per channel. See [DEVELOPER_API_GUIDE.md](docs/DEVELOPER_API_GUIDE.md) for the full execution-mode contract.

**Can I use Decker for backtesting?**
The same rulebook (`operation_rules/RULES.yaml`) drives backtest and live evaluation. See [docs/signal-performance.md](docs/signal-performance.md) for our internal backtest methodology.

---

## More docs

| | |
|--|--|
| [Developer API Guide](docs/DEVELOPER_API_GUIDE.md) | Full auth · rate limits · SDK · FAQ |
| [Quick Start](docs/quickstart.md) | 3-step per path |
| [API Guide](docs/api-guide.md) | Endpoint reference (long form) |
| [Architecture](docs/architecture.md) | Pipeline, state engine, modules |
| [Model & Algorithm](docs/model.md) | How the signal engine works |
| [Operation Rules](operation_rules/RULES.yaml) | Open YAML rulebook (v2.4.7+) |
| [llms.txt](llms.txt) | LLM / AI agent discovery manifest |

---

> Building with Decker? Issues + PRs welcome at [github.com/gigshow/decker-ai](https://github.com/gigshow/decker-ai/issues).
> For the user-facing intro, see the [main README](README.md).
