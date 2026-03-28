# Decker AI — Article Series

English Medium articles. State Engine, sequence labeling, progress_pct, Target→Signal→Entry philosophy, and the Context Engine — for developers and traders.

---

## Part 1 — Foundations (Articles 1–10)

*The what and why: State Engine, signal lifecycle, YAML rulebook, multi-timeframe alignment, $0-LLM architecture.*

| # | Title | Core |
|---|-------|------|
| 1 | [I Built a Trading Engine That Doesn't Use AI to Predict Prices](01_state_engine_not_llm.md) | State Engine, not LLM |
| 2 | [Why Most Trading Bots Fail: Signal Lifecycle](02_signal_lifecycle.md) | Signal lifecycle |
| 3 | [Target → Signal → Entry: The Philosophy](03_target_signal_entry.md) | Contrarian philosophy |
| 4 | [How I Replaced 17 Rules with One YAML](04_yaml_rules.md) | Operation Rules / RULES.yaml |
| 5 | [Building a Crypto Signal API in 5 Minutes](05_signal_api_5min.md) | API onboarding |
| 6 | [I Backtested 330 Signals — progress_pct Revealed](06_backtested_330_signals.md) | Backtest & performance |
| 7 | [State Machines in Trading: Deterministic vs ML](07_state_machines_vs_ml.md) | State Engine vs ML |
| 8 | [From Side Project to Signal Engine: $0 LLM Cost](08_zero_llm_cost_story.md) | Building story & cost |
| 9 | [Why Single-Timeframe Signals Fail — And How Multi-TF Alignment Fixes It](09_multi_tf_alignment.md) | Multi-timeframe alignment |
| 10 | [How I Built a Trading Rulebook That Improves Itself](10_self_improving_rulebook.md) | Self-improving RULES |

---

## Part 2 — The Context Engine (Articles 11–15)

*The how and deep: sequence labeling grammar, 5-state machine, GO/WATCH/HOLD gate, AI as translator, versioning across repos.*

→ **[Read Part 2](part2/README.md)**

| # | Title | Core |
|---|-------|------|
| 11 | [Markets Speak in Sequences, Not Signals](part2/11_markets_speak_in_sequences.md) | Candles as grammar. State as meaning. |
| 12 | [I Replaced a Chart Pattern Library with a 5-State Machine](part2/12_five_state_machine.md) | 5 deterministic states, auditable transitions |
| 13 | [GO, WATCH, or HOLD — Why Three Positions, Not Two](part2/13_go_watch_hold.md) | Ternary gate + 9-layer RULES |
| 14 | [I Let an AI Explain My Trades — But I Didn't Let It Make Them](part2/14_ai_explains_engine_decides.md) | AI as translator, engine as author |
| 15 | [Two Repos, One Engine, Zero Drift](part2/15_two_repos_zero_drift.md) | Version tracking, trace IDs, sync infrastructure |

---

## Publication

- **Medium**: Each article published to Medium (Towards Data Science / The Startup / Better Programming)
- **GitHub**: Full drafts available here
- **CTA**: [GitHub](https://github.com/gigshow/decker-ai-strategy-builder) · [Telegram (DeckerClaw)](https://t.me/deckerclawbot) · [API Docs](https://api.decker-ai.com/docs)
