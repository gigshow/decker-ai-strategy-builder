# The Sequence Engine — How Decker Reads Market Structure

*The concept behind the Context Engine: sequence labeling, state tracking, and the GO/WATCH/HOLD gate.*

---

## The Core Idea

Most trading tools analyze price data as isolated points. Is the RSI high? Is the MACD crossing? Is this candle bigger than the last?

Decker's Sequence Engine analyzes price data as **structured sequences** — the same way a linguist reads text rather than counting individual letters.

> **A candle is a word. A label is its grammatical role. A sequence is a sentence. The market state is the meaning of that sentence.**

This shift from point-in-time scoring to context-aware state parsing is what distinguishes the Sequence Engine from indicator-based systems.

---

## Layer 1: Sequence Labeling

Every candle receives a label that describes its **structural role** in the current price sequence:

| Role | What it means |
|------|---------------|
| **Anchor** (C) | The directional starting point — the market has committed to a direction |
| **Test** (B) | The opposing force is challenging the anchor — outcome undecided |
| **Confirmation** (A) | The anchor direction prevails — the cycle is structurally complete |
| **Connector** | Transitional candle — bridge between anchor and test, or test and resolution |
| **Signal** (S) | A directional resolution event — the sequence grammar just completed |
| **Wide break** (W) | Bilateral break — both directions attempted simultaneously, resolution pending |

Labels are assigned based on **candle relationships**, not candle values. The label doesn't ask "is this candle bullish?" — it asks "what role does this candle play in the current sequence, given what came before it?"

### The Grammar Rules

Labels follow strict grammatical constraints:

- A **signal** only appears after the second leg of a sequence. No shortcutting.
- **Connectors** bridge but never resolve. Maximum two consecutive connectors per swing.
- A **backward break** (market moves against the anchor) resets the entire sequence. New anchor. New cycle. New grammar.

These constraints make the labeling system formally verifiable — violations are errors, not signals.

---

## Layer 2: Three Simultaneous Lanes

Markets run multiple narratives simultaneously. The Sequence Engine tracks three:

```
Main swing:   ─────────────────────────────────────────▶  The dominant cycle
Sub-swing:       ──────────    ──────────                  The counter-narrative
Connector:                ────           ────              Bridge / pause phases
```

| Lane | Question it answers |
|------|---------------------|
| **Main swing** | Who's winning the current cycle? |
| **Sub-swing** | What is the counter-force building toward? |
| **Connector** | Are we in a pause, a bridge, or a trap? |

The **sub-swing counter** is particularly important. When the sub-swing is on its second attempt (or more), it means the opposing force has made multiple structural pushes — the kind of situation that warrants caution even when the main direction appears clear.

*Think of it as the "opponent's hand" in a card game. Even when you're winning, tracking what the opponent is building matters.*

---

## Layer 3: The 5-State Machine

The labeled sequence events drive a **finite state machine** with five discrete states:

```
INIT
 │ anchor appears
▼
C_SET ──────────── bilateral break ──────────▶ W_PENDING
 │ test begins                                      │ direction resolves
▼                                                   ▼
B_FORMING ── test invalidated ──────────────▶ C_SET
 │ test confirmed
▼
B_SET ─── signal confirmed ────▶ INIT (new cycle)
 │ test invalidated
▼
C_SET
```

Every market moment is in exactly one of these states. And from each state, only specific transitions are possible — based on which labeled event just arrived.

This is the key property: **determinism**. The same candle sequence always produces the same state history. No model weights. No training data. No probabilistic uncertainty about what state you're in.

The state machine can be fully expressed as a table of (current state, event) → (next state) pairs. It can be exhaustively tested. It can be reproduced identically on any machine at any time.

---

## Layer 4: The Operation Gate (GO / WATCH / HOLD)

The structural state and label quality are combined to produce a **three-way operation gate**:

| Gate | Structural situation | Meaning |
|------|---------------------|---------|
| `GO` | Cycle completed, conditions met | Evaluate and potentially act |
| `WATCH` | Test in progress (`B_FORMING`) | Monitor, don't act prematurely |
| `HOLD` | Bilateral ambiguity (`W_PENDING`) or active risk rule | Stay flat, risk is elevated |

### Why Three, Not Two

Binary systems (`buy / don't buy`) treat "no signal" as silence. But silence carries no information about *why* there's no signal.

- Was there insufficient data?
- Is the test actively in progress?
- Is there a structural risk condition blocking entry?

`WATCH` and `HOLD` are different states with different implications. `WATCH` means "something is developing, stay close." `HOLD` means "there's a structural reason to stay out."

All three are actionable. All three are informative.

---

## Layer 5: The RULES Engine

The operation gate and signal context are passed through a **9-layer YAML rulebook** that maps structural conditions to specific strategies and action choices:

```
Layer 1: Status conditions (target reached, stop hit)
Layer 2: Portfolio weight conditions  
Layer 3: Entry timing (predictive / signal / confirmation)
Layer 4: Multi-timeframe alignment (fully aligned / counter-trend / transition)
Layer 5: Swing state (A/B/C position in cycle)
Layer 6: Market state (breakout / pullback / range / trend)
Layer 7: Timeframe-specific conditions
Layer 8: Progress thresholds (33% / 50% / 66% / 80% / 90%+)
Layer 9: Portfolio default + fallback
```

The first matching rule produces: a strategy sentence + a ranked list of action choices. The RULES engine runs without an LLM — no tokens, no latency, no unpredictability.

The rulebook is version-controlled, open-source, and available at [operation_rules/RULES.yaml](../operation_rules/RULES.yaml).

---

## Layer 6: AI Consultation (The Narrator)

After the structural analysis is complete, an AI consultation layer translates the structured output into natural language.

The AI receives:
- Current structural state
- Operation gate value
- Matched RULES strategy and choices
- Signal quality metrics
- Sub-swing scope

The AI's job is **translation**, not judgment. It explains what the structural data means — it does not re-evaluate, override, or add its own assessment.

```
Engine (author)           →  Structural state, gate, choices
AI Consultation (narrator) →  "The 1h cycle is in its test phase. Counter-narrative
                               at second attempt. Gate is WATCH. Key levels: [...]"
Human / Agent (actor)     →  Decides whether and how to act
```

This separation is deliberate. The engine's output is deterministic and auditable. The AI's output is explanation. Mixing these roles creates a system that's neither reproducible nor trustworthy.

---

## The Full Pipeline

```
Raw OHLCV candles
    │
    ▼  Sequence Labeling
Each candle: role + direction + quality score (confidence / stability / regime)
    │
    ▼  State Machine
Current state: INIT / C_SET / B_FORMING / B_SET / W_PENDING
Sub-swing counter: which attempt is the counter-narrative on?
    │
    ▼  Operation Gate
GO / WATCH / HOLD
    │
    ▼  RULES Engine (9 layers, YAML, version-controlled)
Matched rule → strategy text + ranked action choices
    │
    ▼  AI Consultation (translation, not judgment)
Natural language explanation of structural state
    │
    ▼  Output
"66% progress. B-leg confirmed. Sub-swing 2 active.
 Recommended: 30% partial TP or hold to target."
```

---

## What Makes This Different

| Aspect | Traditional indicators | ML/prediction models | Decker Sequence Engine |
|--------|----------------------|---------------------|----------------------|
| Signal source | Point-in-time scores | Trained predictions | Structural cycle position |
| Reproducibility | ✅ (same math) | ❌ (model drift) | ✅ (deterministic FSM) |
| Auditability | Partial | ❌ | ✅ (full trace per signal) |
| Context awareness | ❌ | Partial | ✅ (3-lane sequence tracking) |
| "Why this signal?" | Score threshold | Black box | Explicit state transition |
| Works in ranging markets | Limited | ❌ | ✅ (independent per-cycle tracking) |

---

## Learn More

The deep-dive article series covers each layer in detail:

- [Article #11 — Markets Speak in Sequences, Not Signals](../docs/medium/part2/11_markets_speak_in_sequences.md) — Sequence labeling and grammar
- [Article #12 — I Replaced a Chart Pattern Library with a 5-State Machine](../docs/medium/part2/12_five_state_machine.md) — State machine design
- [Article #13 — GO, WATCH, or HOLD](../docs/medium/part2/13_go_watch_hold.md) — Ternary gate + RULES
- [Article #14 — AI Explains, Engine Decides](../docs/medium/part2/14_ai_explains_engine_decides.md) — The consultation architecture
- [Article #15 — Two Repos, Zero Drift](../docs/medium/part2/15_two_repos_zero_drift.md) — Versioning and audit trail

**Try it:**
```bash
curl "https://api.decker-ai.com/api/v1/signals/BTCUSDT/state"
```

Or ask [@deckerclawbot](https://t.me/deckerclawbot): *"What's the structural state of Bitcoin right now?"*
