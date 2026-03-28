# Decker AI — Article Series, Part 2: The Context Engine

*Articles #11–15 — Phase 4 of the Decker series*

---

**Part 1** (Articles 1–10) covered the foundations: what the State Engine is, how `progress_pct` works, the Target→Signal→Entry philosophy, YAML rulebook, multi-timeframe alignment, and the $0-LLM-cost architecture.

**Part 2** goes deeper into the engine that generates those signals — the Context Engine: how markets are read as sequences, how a 5-state machine tracks structural position, and how the GO/WATCH/HOLD gate produces actionable decisions.

---

## Articles

| # | Title | Core Idea |
|---|-------|-----------|
| 11 | [Markets Speak in Sequences, Not Signals](11_markets_speak_in_sequences.md) | Candles as grammar tokens. Market state as sentence meaning. |
| 12 | [I Replaced a Chart Pattern Library with a 5-State Machine](12_five_state_machine.md) | Deterministic state: INIT→C_SET→B_FORMING→B_SET→W_PENDING |
| 13 | [GO, WATCH, or HOLD — Why Three Positions, Not Two](13_go_watch_hold.md) | Ternary operation gate + 9-layer RULES engine |
| 14 | [I Let an AI Explain My Trades — But I Didn't Let It Make Them](14_ai_explains_engine_decides.md) | AI as translator. Engine as decision-maker. Hard separation. |
| 15 | [Two Repos, One Engine, Zero Drift](15_two_repos_zero_drift.md) | Version tracking: engine, schema, and RULES across two repos |

---

## The Core Arc

**The Insight**: Most trading tools ask "is price going up or down?" Decker asks "where are we in the current structural cycle, and what can happen next?"

**Article 11** → The market has grammar. Labels are tokens. Sequences carry meaning.  
**Article 12** → Five deterministic states track every structural position. No prediction needed.  
**Article 13** → Three operation modes (not two) because "silent" and "structurally blocked" are different things.  
**Article 14** → The AI explains the structural analysis. It never generates it.  
**Article 15** → Every signal is versioned. Every version is auditable.

---

## Three Analogies

**Drama**: Every market session is a story arc with acts, characters, and climaxes. The labeling system tells you which chapter you're in.

**Game**: Two players — the main trend and the counter-force. The sub-swing tracker follows the opponent's moves in real time.

**Go (바둑)**: The outcome is uncertain until the end. But there is always an objectively best move — the one that maximizes structural advantage. The operation gate is Decker's version of that move.

---

## Try It

```bash
# Current structural state
curl "https://api.decker-ai.com/api/v1/signals/BTCUSDT/state"

# Strategy + choices
curl "https://api.decker-ai.com/api/v1/signals/BTCUSDT/strategy"
```

Or ask [@deckerclawbot](https://t.me/deckerclawbot): *"What's the Bitcoin structural state?"*

---

← [Part 1 — Foundations (Articles 1–10)](../README.md)
