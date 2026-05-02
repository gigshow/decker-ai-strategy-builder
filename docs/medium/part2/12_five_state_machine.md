# I Replaced a Chart Pattern Library with a 5-State Machine — Here's Why It's More Honest

*Part 2, Article #12 — Decker AI Series*

*Chart patterns tell you what a price might be about to do. A state machine tells you exactly where you are. One is a guess dressed as pattern recognition. The other is a proof.*

---

I used to have a folder called `patterns/`. It contained dozens of Python functions with names like `detect_head_and_shoulders`, `detect_double_bottom`, `detect_bull_flag`. Each returned a probability score between 0 and 1.

The folder is gone now.

Not because the patterns were wrong — they were about as reliable as patterns can be. But because they were answering the wrong question. Every function was asking: *"Does this price sequence look like X?"*

The right question is: *"Where are we in the current structural cycle?"*

Those sound similar. They are profoundly different.

---

## The Problem with Pattern Matching

A "head and shoulders" pattern is named after what it looks like on a chart. The name is visual. The detection is visual. The signal — if triggered — is a bet that the visual resemblance correlates with future price movement.

Sometimes it does. Often enough that people keep using it. But there's a silent assumption baked in: that the visual shape is the *cause* of the price behavior, rather than a symptom of an underlying structural dynamic.

The Decker engine inverts this entirely. Instead of asking *"what shape does the price form?"*, it asks *"what structural state is the market in, and what can happen from here?"*

The answer is a **small, auditable session state machine**. And unlike a pattern library, it has no false positives — because it doesn't predict. It **describes**.

> **Implementation note:** The open engine’s `SessionState` enum includes **`A_FORMING`** (signal / break handling after `B_SET`) and **break** states (`BREAK_PLUS` / `BREAK_MINUS` / `NEUTRAL`). The five rows below are the **core narrative** states readers first learn; canonical transitions vs code are in [diagrams/system_flow.md](../../../diagrams/system_flow.md).

---

## The five core states (narrative)

The state engine tracks one session at a time. These five names are the usual mental model:

| State | Name | Meaning |
|-------|------|---------|
| `INIT` | Initialization | No structural anchor yet — watching for the first anchor candle |
| `C_SET` | Anchor Set | A directional anchor has been established |
| `B_FORMING` | Test in Progress | The opposing force is actively testing the anchor |
| `B_SET` | Test Confirmed | The test has completed structurally — resolution is pending |
| `W_PENDING` | Wide Break Pending | A bilateral break occurred — direction is ambiguous, waiting for resolution |

Add **`A_FORMING`** after `B_SET` when the engine moves into signal / outcome handling (see diagram). Every moment the market is in exactly one session state. Transitions follow **labeled events**, not indicator thresholds.

---

## Deterministic, Not Probabilistic

Here's the core design decision that makes this different from any ML-based approach:

> Transitions between states are **deterministic**. The same candle event, in the same state, always produces the same transition. There is no probability — only structure.

Conceptually, the transition table looks like this:

| Current State | Event (trigger) | Next State |
|---|---|---|
| `INIT` | Anchor candle appears | `C_SET` |
| `C_SET` | Test begins | `B_FORMING` |
| `C_SET` | Bilateral break | `W_PENDING` |
| `B_FORMING` | Test confirmed | `B_SET` |
| `B_SET` | Signal pending / confirmed | `A_FORMING` |
| `A_FORMING` | Failed break / cycle reset | `C_SET` |
| `A_FORMING` | Wide pending enter | `W_PENDING` |
| `W_PENDING` | Resolved / rebind | `C_SET` |

*Narrative-only shortcuts* (e.g. “test invalidated” straight to `C_SET`) appear in prose and higher-level pipelines; the **minimal** `TRANSITION_RULES` tuple in code is what regression tests lock — see [system_flow.md](../../../diagrams/system_flow.md).

The transition graph is finite and closed. You can draw it on a napkin. Every possible market evolution maps to a path through this graph.

When you're in `B_SET`, the next **named** core step is into `A_FORMING` when a signal path arms; outcomes then reset or branch into wide-pending or break states. That's not a guess. That's a constraint. And constraints are more useful than predictions.

---

## The C → B → A Cycle

The states map to a structural cycle:

```
     C (Anchor)
      ↓
     B (Test — the opposing force challenges the anchor)
      ↓
     A (Confirmation — the anchor direction prevails)
      ↓
  [Signal Emitted] → New Cycle
```

But the interesting part isn't the happy path. It's the exits:

- **Test invalidated**: The opposing force wins. The anchor loses. Return to `C_SET` — a new anchor must be found.
- **Wide break** (`W_PENDING`): Neither direction can claim the move. A bilateral break creates structural ambiguity. Resolution is required before any signal is valid.
- **Sequence reanchor**: The signal confirmed — but the same direction fires again immediately. This isn't a new cycle; it's a reinforcement. The engine continues tracking from a re-anchored position rather than resetting entirely.

These aren't edge cases. They're the majority of what markets actually do. The engine's value comes from tracking them precisely.

---

## A Real Evaluation Trace

Here's what the engine output looks like after evaluating a structural cycle:

```json
{
  "state": "INIT",
  "last_event": "signal_confirmed",
  "signal": {
    "direction": "+",
    "signal_price": 3240.50,
    "structural_reference": 3198.20
  },
  "operation_gate": "GO",
  "label_quality": {
    "confidence": 0.91,
    "stability": 0.88
  }
}
```

`state: "INIT"` after a `signal_confirmed` event means: *the structural cycle just completed. A new cycle begins.*  
`operation_gate: "GO"` is the downstream indicator. The state machine just completed a verified cycle. The operation layer can now evaluate whether to act.

The signal isn't a score. It's an event: *the structural cycle just completed in the bullish direction*.

---

## Why "5 States" Is the Right Number

States represent **structural positions**, not market conditions. And structurally, there are exactly these positions:

1. No anchor yet (`INIT`)
2. Anchor established, not being tested (`C_SET`)
3. Test in progress, not yet confirmed (`B_FORMING`)
4. Test confirmed, awaiting resolution (`B_SET`)
5. Bilateral ambiguity, awaiting directional resolution (`W_PENDING`)

Market *conditions* (volatility, volume, trend strength) are measured separately — by the label quality metrics. The state machine doesn't mix these concerns. Structure is structure. Quality is quality. They are separate axes.

This means you can have a high-quality `B_SET` state (the test was structurally clean, high confidence) or a low-quality `B_SET` state (structurally valid but noisy, lower stability). The state is the same; the quality flag tells you how much to trust it.

Pattern libraries can't make this distinction. A detected pattern is either present or absent.

---

## The Determinism Advantage

Here's what determinism gives you that probabilistic detection doesn't:

**Reproducibility**: Given the same candle sequence, the engine produces the same state history. Always. There's no "this model was trained differently" or "the feature weights shifted."

**Debuggability**: When a signal fires unexpectedly, you can trace exactly which candle transition triggered it. The audit trail is complete.

**Testability**: The entire state machine can be expressed as a matrix of (state, event) → (new_state) pairs. You can write exhaustive unit tests covering every valid and invalid transition.

**Composability**: Because state is explicit, you can run multiple state machines simultaneously — for different timeframes, different swing lanes — and combine them without interference. This is how sub-swing tracking works: a separate state machine instance tracks the counter-narrative in parallel with the main swing.

---

## The Honest Part

Pattern libraries make implicit claims: *"this looks like a reversal pattern, therefore a reversal might occur."* The confidence is implied, and the failure mode is silent.

The state machine makes no predictive claim. It says: *"the market is in state X. From state X, only Y and Z transitions are structurally possible."* It doesn't tell you which one will happen. It tells you what is structurally coherent and what is not.

When the state is `B_SET` and a signal confirmation event arrives, the engine doesn't say "this will go up." It says "a structurally complete cycle just occurred." The operation layer — RULES, the trader, the AI consultation — then decides what to do with that fact.

That's not a limitation. That's intellectual honesty. The engine knows what it knows.

---

## What's Next

We now have two layers: the labeling grammar (Article #11) and the structural state machine (this article). Together, they produce a structured object capturing exactly where the market is in its current cycle.

The next article goes one layer higher: the **Operation Gate** — the three-way decision that takes all of this structure and collapses it into `GO`, `WATCH`, or `HOLD`.

Why three? Because binary is a lie.

---

*← [Article 11: Markets Speak in Sequences](11_markets_speak_in_sequences.md) · [Article 13: GO, WATCH, or HOLD →](13_go_watch_hold.md)*

*API: [api.decker-ai.com/docs](https://api.decker-ai.com/docs) · GitHub: [decker-ai](https://github.com/gigshow/decker-ai)*
