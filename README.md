<!--
  Keywords: AI trading, crypto signal, Bitcoin, Ethereum, market state engine,
  state machine, sequence labeling, algorithmic trading, trading API, Telegram bot,
  deterministic signal, progress_pct, operation rules, GO WATCH HOLD, Kakao channel
-->
<div align="center">

<img src="assets/decker_claw_mascot_v1.png" width="80" alt="DeckerClaw" />

# Decker AI Strategy Builder

**The Market Has Grammar. Decker Reads It.**

*From candles to context. From data to state. From state to decision.*

[![GitHub Stars](https://img.shields.io/github/stars/gigshow/decker-ai-strategy-builder?style=flat-square&color=DAA520)](https://github.com/gigshow/decker-ai-strategy-builder/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/gigshow/decker-ai-strategy-builder?style=flat-square)](https://github.com/gigshow/decker-ai-strategy-builder/network)
[![Monthly Return](https://img.shields.io/badge/range--market_return-20~30%25-brightgreen?style=flat-square)](docs/signal-performance.md)
[![Telegram](https://img.shields.io/badge/Telegram-DeckerClaw-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://t.me/deckerclawbot)
[![Kakao Channel](https://img.shields.io/badge/Kakao-Channel-FEE500?style=flat-square&logo=kakaotalk&logoColor=000000)](https://pf.kakao.com/_RxlxjVX)
[![API Docs](https://img.shields.io/badge/API-Docs-00C853?style=flat-square)](https://api.decker-ai.com/docs)
[![Website](https://img.shields.io/badge/Website-decker--ai.com-6C47FF?style=flat-square)](https://decker-ai.com)

[🌐 Website](https://decker-ai.com) · [🤖 Telegram (DeckerClaw)](https://t.me/deckerclawbot) · [💬 Kakao Channel](https://pf.kakao.com/_RxlxjVX) · [📖 API Docs](https://api.decker-ai.com/docs) · [🚀 Quick Start](docs/quickstart.md) · [📚 Article Series](docs/medium/README.md) · [🗺 Roadmap](docs/roadmap.md)

</div>

---

## The Insight

Most AI trading tools ask: *"Is the price going up or down?"*

Decker asks a different question: ***"Where are we in the current structural cycle — and what can happen next?"***

> A candle is a word. A label is its grammatical role. A sequence of labeled candles is a sentence. **The market state is the meaning of that sentence.**

This shift — from point-in-time scoring to context-aware state parsing — is what makes Decker different. It doesn't predict prices. It reads market structure the way a linguist reads a text: with grammar, sequence, and meaning.

**The result:** not "BUY" or "SELL" — but `GO`, `WATCH`, or `HOLD`, backed by a fully auditable, deterministic structural analysis.

---

## ⚡ Try It Now

| Time | Path | What you get |
|------|------|-------------|
| **30 sec** | API | `curl -s "https://api.decker-ai.com/api/v1/signals/BTCUSDT/state"` |
| **5 min** | Telegram | [@deckerclawbot](https://t.me/deckerclawbot) — ask "Bitcoin signal?" |
| **3 min** | Samples | `./samples/signal-push-strategy.sh BTCUSDT 96000 100000 92000` |
| **10 min** | Full onboarding | [decker-ai.com](https://decker-ai.com) → connect Telegram → start trading |

---

## 🎯 What Decker Does

```
Raw candles (OHLCV)
    ↓  Sequence Labeling  →  Each candle gets a grammatical role (anchor / test / signal)
    ↓  State Machine      →  5 structural states: INIT → C_SET → B_FORMING → B_SET → W_PENDING  
    ↓  Operation Gate     →  GO · WATCH · HOLD  (not binary — three operational modes)
    ↓  RULES Engine       →  9-layer YAML rulebook → strategy + ranked choices
    ↓  AI Consultation    →  LLM translates structural state into natural language
    ↓
You get: "66% progress. B-leg confirmed. Counter-narrative at sub-swing 2.
          Recommended: 30% partial TP or hold to target."
```

**No price prediction. No black box. Every output traces to a formal structural cause.**

---

## 💡 Why This Is Different

| Feature | Typical AI Trading | Decker |
|---------|-------------------|--------|
| Signal source | LLM / ML price prediction | **Deterministic state machine** |
| Core output | BUY / SELL | `progress_pct` + `operation_gate` + strategy choices |
| LLM role | Makes the call | **Explains the structural state** |
| Auditability | ❌ Black box | ✅ Every signal has a `trace_id` |
| LLM cost per signal | High | **$0 on the rules path** |
| Reproduced from same input | ❌ | ✅ Always |

---

## 📐 The progress_pct System

Every signal has a **lifecycle** — from formation (0%) to target (100%). Decker tracks this in real time.

```
Signal birth (0%) ──── Entry zone ──── Midpoint ──── Target (100%)
                              ↑                 ↑
                       "GO: enter now"    "Consider partial TP"
```

**Formula:**
- Long: `(current − entry) / (target − entry) × 100`
- Short: `(entry − current) / (entry − target) × 100`

| progress_pct | State | Recommended posture |
|---|---|---|
| 0–32% | Early | Wait or prepare entry |
| 33–66% | Active | Entry window, risk management begins |
| 67–89% | Late | Partial take-profit, reduce size |
| 90–100% | At target | Prepare full exit |

> Most signal tools give you: **BUY**  
> Decker gives you: **BUY + 67% progress** = *"The move is real, but the easy money is already in"*

---

## 🎭 The Three Analogies

Understanding Decker's engine becomes clearer through three lenses:

**Drama** — Every market session is a story arc. The labeling system identifies which chapter you're in: exposition (C anchor), rising action (B test), climax (confirmation), or resolution (signal). You're not reading a single frame — you're following a narrative.

**Game** — The market has two players: the main trend and the counter-force. The `sub_swing` tracking follows the opponent's moves in real time. Just as in chess, knowing your opponent's current position is as important as knowing your own.

**Go (바둑)** — The outcome is uncertain until the end. But at every moment, there is an objectively best move — the one that maximizes structural advantage given the current state. The `operation_gate` is Decker's version of "the optimal next move."

---

## 🏗 Architecture

```
Sequence Labeler  →  Each candle: role (anchor/test/signal) + direction + quality score
State Engine      →  Session FSM: structural position (see diagrams/system_flow.md for core vs runtime states)  
Operation Gate    →  GO / WATCH / HOLD: three-way operational mode
RULES Engine      →  YAML rulebook: 9 layers, 30+ rules, version-controlled
AI Consultation   →  LLM as translator (not decision-maker): explains state in plain language
Signal Lifecycle  →  progress_pct: real-time position within the signal's journey
```

Full technical detail: [Architecture](docs/architecture.md) · [Algorithm Concepts](concept/labeling_algorithm.md) · [Model & Performance](docs/model.md)

---

## 📊 Performance

Signal model is based on **structural cycle evaluation**, not pattern matching.

| Metric | Result |
|--------|--------|
| **Win Rate** | 61–68% |
| **Avg Profit** | 5–12% |
| **Max Drawdown** | < 9% |
| **Range-market monthly** | 20–30% |
| **Signal Frequency** | 1–3 / day |

*Source: operation rulebook backtest (progress 33–95% range). Past performance does not guarantee future results.*

Details: [Signal Performance](docs/signal-performance.md) · [Model & Algorithm](docs/model.md)

---

## 📚 Article Series

**Part 1 — Foundations (Articles 1–10)**  
State Engine, signal lifecycle, Target→Signal→Entry philosophy, YAML rulebook, multi-timeframe alignment, and the $0-LLM-cost architecture.

**Part 2 — Context Engine (Articles 11–15)**  
How markets speak in sequences, the session state machine, the GO/WATCH/HOLD gate, why AI explains but doesn't decide, and how to version a trading algorithm across two repos.

→ [Read the full series](docs/medium/README.md)

---

## 🤝 Three Ways to Use Decker

| Path | Who | How |
|------|-----|-----|
| **A. Use the service** | Traders, non-developers | [decker-ai.com](https://decker-ai.com) → connect [@deckerclawbot](https://t.me/deckerclawbot) |
| **B. Add as a skill** | OpenClaw / AI agent developers | Add Decker skill → `web_fetch` → API → natural language responses |
| **C. Integrate via API** | Backend developers | [REST API docs](https://api.decker-ai.com/docs) |
| **D. Self-host (turnkey)** | Self-hosters | [turnkey/](turnkey/) — Railway one-click lightweight bot |

---

## 🚀 Quick Start

**30-second API test:**
```bash
curl -s "https://api.decker-ai.com/api/v1/signals/BTCUSDT/state" | python3 -m json.tool
```

**Full onboarding (Telegram):**
1. Sign up at [decker-ai.com](https://decker-ai.com)
2. Get your code at [decker-link-telegram](https://decker-ai.com/decker-link-telegram)
3. Send `/start {code}` to [@deckerclawbot](https://t.me/deckerclawbot)
4. Ask: *"Bitcoin signal?"* / *"What should I do with my ETH position?"*

---

## 📖 Docs

| Document | Purpose |
|----------|---------|
| [Quick Start](docs/quickstart.md) | 3-step guide, try scenarios |
| [Architecture](docs/architecture.md) | Pipeline, modules, State Engine |
| [Model & Algorithm](docs/model.md) | Algorithm story, structure, performance |
| [API Guide](docs/api-guide.md) | Public API (developers) |
| [Operation Rules](operation_rules/RULES.yaml) | YAML rulebook (open) |
| [Article Series (1–15)](docs/medium/README.md) | Medium articles — deep dives |
| [Signal Performance](docs/signal-performance.md) | Backtest & live metrics |
| [Risk Management](docs/risk-management.md) | Risk framework |
| [Roadmap](docs/roadmap.md) | What's coming |
| [Onboarding](docs/ONBOARDING_PUBLIC.md) | By persona: user / skill dev / contributor |
| [Brand Guide](docs/BRAND_GUIDE.md) | Naming and expression rules |
| [llms.txt](llms.txt) | AI discovery manifest (read this first — agents & crawlers) |

**Concepts:**
| Document | Purpose |
|----------|---------|
| [Sequence Engine](concept/sequence_engine.md) | Labeling + FSM + GO/WATCH/HOLD (Context Engine story) |
| [Sequence Labeling](concept/labeling_algorithm.md) | How candles get labeled |
| [Market State Theory](concept/market_state_theory.md) | progress_pct and signal lifecycle |
| [Signal LLM](concept/signal_llm_concept.md) | State Engine + AI consultation layer |

---

## 🏆 Roadmap

| Status | Phase | Feature |
|--------|-------|---------|
| ✅ | Phase 2 | Slack integration (OpenClaw skill, Way B) |
| ✅ | Phase 3 | Order approval flow — "Buy 0.01 BTC → confirm → execute" |
| ✅ | Phase 4 | Proactive signals, smart alerts |
| ✅ | Phase 5 | Member journey, welcome flow |
| ✅ | Operations | RULES.yaml v2.3+, progress/multi-TF/engine conditions |
| ✅ | Agent | Telegram (Way A) + OpenClaw (Way B) + turnkey (Way D) |
| ✅ | Signal LLM | rationale · choices · tf_alignment · entry_timing |
| ✅ | State Engine | Sequence labeling + session FSM + GO/WATCH/HOLD gate ([diagrams](diagrams/system_flow.md)) |
| 🔜 | Backtest report | progress-range profit validation, public results |
| 🔜 | DSL | Strategy expression beyond RULES |

---

## 🔗 Links

| | URL |
|-|-----|
| **Service** | https://decker-ai.com |
| **Telegram bot** | https://t.me/deckerclawbot |
| **Telegram connect** | https://decker-ai.com/decker-link-telegram |
| **API docs** | https://api.decker-ai.com/docs |
| **Kakao channel** | https://pf.kakao.com/_RxlxjVX |

---

> ⚠️ This repository is the public documentation, samples, and community hub for Decker AI. Production application code runs in a private repository.
>
> **Available here**: API call samples, RULES.yaml reference, architecture documentation, concept articles, and the full article series.

