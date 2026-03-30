# Engine recipe — from narrative to runnable output

**Audience**: You read the public **concept** docs and want to see **real OHLCV → same evaluate path as production** (not a toy mock).

This repository is **documentation, RULES, and samples**. The **runnable pipeline** (CCXT fetch → L1 normalize → `evaluate_engine_request_body`) lives in the **platform monorepo** — by design, so the open “recipe” stays explainable while the implementation stays testable and versioned with CI.

---

## 1. What “recipe” means here

| Layer | Public where | What you learn |
|-------|----------------|----------------|
| Sequence labeling | [labeling_algorithm.md](../concept/labeling_algorithm.md) | Roles, grammar, quality |
| Session FSM + gate | [sequence_engine.md](../concept/sequence_engine.md), [system_flow.md](../diagrams/system_flow.md) | States, GO/WATCH/HOLD |
| Progress + RULES | [architecture.md](architecture.md), [RULES.yaml](../operation_rules/RULES.yaml) | `progress_pct`, rule matching |
| **Runnable bridge** | **This page + monorepo `scripts/`** | Live candles → engine JSON |

---

## 2. Run with real market data (monorepo)

**Prerequisites**: Clone the Decker platform repo that contains `services/decker-engine` and `scripts/smoke_live_l1_engine_evaluate.py`. Python 3.11+ recommended. Network access (public exchange OHLCV via CCXT; no trading keys).

From the **monorepo root**:

```bash
# One-line health: fetch ~2h of 1h bars (Binance public API) → L1 policies → embedded evaluate
python scripts/smoke_live_l1_engine_evaluate.py --exchange binance --symbol ETHUSDT --timeframe 1h --limit 120 --json-log
```

You should see one JSON line with `"event": "b1_live_engine_evaluate"`, candle counts, `engine_mode_used`, and `l1_preprocess` (gap policy summary).

**Full engine response** (large):

```bash
python scripts/smoke_live_l1_engine_evaluate.py --exchange binance --limit 120 --pretty
```

**Same body via HTTP** (when your API is up):

```bash
python scripts/smoke_live_l1_engine_evaluate.py --http http://127.0.0.1:8001 --limit 120 --json-log
```

**YAML / env overrides** (monorepo `docs/B1_LIVE_ENGINE_CONFIG.md`, `config/b1_live_engine.example.yaml` — same CLI as the Korean recipe page):

```bash
python scripts/smoke_live_l1_engine_evaluate.py --config config/b1_live_engine.example.yaml --json-log
```

Script reference: `scripts/smoke_live_l1_engine_evaluate.py` (docstring). Implementation detail: `src/decker/api/app/services/engine_core/l1_ccxt_adapter.py` (CCXT → L1 → evaluate body). Roadmap: internal `DECKER_MARKET_AGENT_LOOP_ROADMAP.md` — B1 / loop #0.

---

## 3. What you do *not* get from this repo alone

- No long-running exchange **streaming** worker (batch fetch per run).
- No hosted **engine binary** — you run embedded or your own `internal/engine/evaluate` deployment.
- **Operational** alerting, cron, and DB persistence are platform concerns, not this docs tree.

---

## 4. Related

- [API Guide](api-guide.md) — product REST (`/state`, `/strategy`, …), different slice than raw engine evaluate.
- [Quick start](quickstart.md) — end-user paths (Telegram, API curl).
