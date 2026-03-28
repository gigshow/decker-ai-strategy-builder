# Sequence Labeling — How Decker Reads Market Structure

*The algorithm that turns raw price candles into a structured, grammatically-aware sequence.*

> For the full conceptual overview of the engine: [Sequence Engine](sequence_engine.md)  
> For the deep-dive article: [Article #11 — Markets Speak in Sequences, Not Signals](../docs/medium/part2/11_markets_speak_in_sequences.md)

---

## The Core Idea

Most systems analyze price data as isolated numbers: "Is the RSI high? Did the MACD cross?" These are point-in-time scores with no memory of what came before.

Decker's labeling algorithm analyzes price as **structured sequences** — the same way natural language processing reads text: with grammar, context, and role.

> **A candle is a word. A label is its grammatical role. A sequence is a sentence.**

---

## What Each Candle Receives

Every candle gets a label that describes its **structural role** in the current price sequence:

| Label | Role | Meaning |
|-------|------|---------|
| **Anchor (C)** | Foundation | The market has committed to a direction. This candle establishes the structural starting point. |
| **Test (B)** | Challenge | The opposing force is challenging the anchor. Outcome undecided. |
| **Confirmation (A / Signal)** | Resolution | The anchor direction prevails. The cycle is structurally complete. |
| **Connector (T, T2)** | Bridge | Transitional candle. Maximum two consecutive connectors per swing. |
| **Wide Break (W)** | Ambiguity | Both directions attempted simultaneously. Resolution required. |

The label is determined by **candle relationships** — not candle values. The question is not "is this candle bullish?" but "what role does this candle play given what came before it?"

---

## The Grammar Rules

The labeling system follows strict grammatical constraints that make it formally verifiable:

**Rule 1 — Signal placement**: A confirmation (signal) label only appears after the second leg of a sequence. No premature resolution.

```
Valid:   Anchor → Connector → Connector → Second leg → Signal
Invalid: Anchor → Signal (missing legs)
```

**Rule 2 — Connector limits**: Connectors bridge but never resolve. A maximum of two consecutive connectors per swing cycle. After two connectors, the sequence must resolve into a positional label.

**Rule 3 — Reset on backward break**: When the market breaks in the opposite direction (overwriting a previous high or low), the entire labeling context resets. New anchor. New sequence. New grammar.

---

## Three Simultaneous Lanes

The labeling algorithm tracks three structural lanes simultaneously:

```
Time →

Main swing:   ═══════════════════════════════════════
                  ↑ The dominant cycle

Sub-swing:          ───────    ───────────
                    ↑ The counter-narrative (opponent's moves)

Connector:               ──          ──
                         ↑ Bridge / pause phases
```

| Lane | What it tracks | Why it matters |
|------|---------------|----------------|
| **Main** | Dominant structural cycle | Who's winning right now |
| **Sub-swing** | Counter-narrative attempts | What the opposition is building |
| **Connector** | Transition phases | Bridge, pause, or trap |

The **sub-swing count** is particularly significant. A sub-swing on its second attempt means the counter-force has made multiple structural pushes. The engine tracks this as a number — `sub_swing_count: 2` — which propagates to the RULES engine for risk-adjusted strategy recommendations.

---

## Label Quality Metrics

Each labeling event includes quality metrics:

| Metric | Range | Meaning |
|--------|-------|---------|
| `confidence` | 0–1 | How structurally clean is this label assignment? |
| `stability` | 0–1 | How stable is the current sequence? |
| `regime_consistency` | 0–1 | Is the current label consistent with the broader market regime? |

High quality does not mean "will profit." It means "the structural conditions for this signal type are present and well-defined." A `confidence: 0.91` signal with `action_gate: WATCH` means: structurally clean, but not yet resolved.

---

## Output Format

After processing a candle sequence, the labeling algorithm produces:

```json
{
  "last_label": {
    "role": "test",
    "direction": "+",
    "position_in_cycle": "b_leg_confirmed"
  },
  "state": "B_SET",
  "sub_swing_count": 2,
  "in_connector_phase": false,
  "label_quality": {
    "confidence": 0.87,
    "stability": 0.91,
    "regime_consistency": 0.84
  },
  "label_mode": "sequence_v2"
}
```

This output feeds directly into the [State Machine](sequence_engine.md#layer-2-the-5-state-machine) and [Operation Gate](sequence_engine.md#layer-4-the-operation-gate-go--watch--hold).

---

## Why This Produces Better Signals

| Aspect | Indicator-based | Decker Sequence Labeling |
|--------|----------------|--------------------------|
| Input | Candle values (price, volume) | Candle relationships (sequence position) |
| Memory | None (point-in-time) | Full sequence context |
| Reproducibility | ✅ | ✅ (deterministic FSM) |
| "Which chapter are we in?" | ❌ | ✅ |
| Works in ranging markets | Limited | ✅ (independent per-cycle) |
| Sub-swing (counter-force) tracking | ❌ | ✅ |

---

## What the Algorithm Outputs (for downstream systems)

The labeling output is consumed by:

1. **State Machine** — Transitions between the 5 structural states based on label events
2. **Operation Gate** — Determines `GO` / `WATCH` / `HOLD` based on the current state
3. **RULES Engine** — Applies policy rules using label quality and state fields
4. **AI Consultation** — Explains the structural state in natural language

Full pipeline: [Sequence Engine concept](sequence_engine.md) · [System flow diagrams](../diagrams/system_flow.md)

---

## Try It

```bash
# Get the current structural state for BTC
curl "https://api.decker-ai.com/api/v1/signals/BTCUSDT/state"
```

Or ask [@deckerclawbot](https://t.me/deckerclawbot): *"What's the structural state of Bitcoin?"*

---

*한국어 설명이 필요하신 분: [시장 상태 이론](market_state_theory.md)에서 progress_pct 개념을, [라벨링 알고리즘 기초](signal_llm_concept.md)에서 한국어 기초 설명을 확인하세요.*
