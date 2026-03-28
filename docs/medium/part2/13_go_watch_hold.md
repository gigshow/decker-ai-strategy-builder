# GO, WATCH, or HOLD — Why My Trading Agent Has Three Positions, Not Two

*Part 2, Article #13 — Decker AI Series*

*Most trading systems give you two answers: buy or don't buy. That's not a signal. That's a coin flip with extra steps.*

---

Here's a question that took me a long time to answer properly:

What should a well-designed trading system tell you when it doesn't have a clear signal?

The naive answer is "nothing." If there's no signal, the system is silent. This is how most indicator-based systems work: they fire when they fire, and they're quiet the rest of the time.

The problem is that "quiet" and "no signal" mean very different things. A system that has analyzed the market and determined that the current state is structurally inconclusive should tell you that. Loudly. That's information. That's actionable.

That's the difference between binary and ternary signal design. And it's why the Decker engine uses three operation states instead of two: `GO`, `WATCH`, and `HOLD`.

---

## The Problem with Binary

Every binary signal system has the same design flaw: the signal is either present or absent. But the absence of a signal carries no information about *why* it's absent.

- Was there insufficient data?
- Did the pattern fail to complete?
- Is the market actively in a state that contradicts entry?
- Is the market in a state where entry would be premature but might become valid soon?

Binary can't distinguish these cases. They all look the same: silence.

The `WATCH` state is the explicit representation of "don't act, but don't look away." It's silence with context.

---

## Three States, One Gate

The operation gate holds one of three values:

| Gate | Meaning | Appropriate Response |
|------|---------|---------------------|
| `GO` | Structural cycle completed, conditions met | Evaluate entry/action |
| `WATCH` | Signal incomplete or test still in progress | Monitor, prepare |
| `HOLD` | Active structural risk present | Stay flat or exit existing |

These are **operational modes** — discrete positions in a decision space designed to capture the three situations a trader actually faces. Not scores. Not probabilities. States.

---

## How the Gate Gets Its Value

The gate value is set through a two-layer process:

**Layer 1 — Engine evaluation**: After processing the candle sequence through the state machine, the operation context builder sets an initial gate value based on structural state:
- `B_SET` + signal confirmation → `GO`
- `B_FORMING` (test in progress) → `WATCH`
- `W_PENDING` (bilateral break, directional ambiguity) → `HOLD`

**Layer 2 — RULES evaluation**: The RULES engine then evaluates the full signal context against the YAML rulebook. Rules can refine or override the gate based on additional context:

```yaml
# Example RULES.yaml conditions
- id: signal_fully_aligned
  entry_timing: signal
  tf_alignment: fully_aligned
  strategy: "Standard position. All TFs aligned. Strong hold recommended."

- id: counter_trend_exit_fast
  tf_alignment: counter_trend
  progress_min: 60
  strategy: "Counter-trend signal at 60%+. High resistance zone. Take 65% profit."

- id: sub_swing_scope_attention
  progress_min: 40
  progress_max: 65
  sub_swing_min: 2
  strategy: "Sub-swing scope 2+. Multi-front risk active. Review before adding size."
```

The RULES system evaluates nine layers in priority order:

1. **Status** (target reached, stop hit — always wins)
2. **Portfolio** (position sizing and weight)
3. **Entry Timing** (predictive, signal, confirmation)
4. **TF Alignment** (multi-timeframe direction)
5. **Swing State** (A/B/C position in cycle)
6. **Market State** (breakout, pullback, range, trend)
7. **TF Specific** (timeframe-specific conditions)
8. **Progress** (33%, 50%, 66%, 80%, 90%+)
9. **Portfolio Default + Fallback**

The first matching rule wins. It provides both a strategy text and a ranked set of structured action choices.

---

## `WATCH` Is Not a Failure State

Most systems treat "no action" as failure — something to minimize. Either the system fires or it doesn't.

In Decker's design, `WATCH` is a first-class output. It communicates a specific structural situation: **the signal formation is in progress but not complete**. This is the `B_FORMING` state — the test swing is actively in progress, the counter-force is building, and the outcome hasn't resolved.

`WATCH` says: *"Something is happening. It matters. Stay close."*

The operational difference between `WATCH` and `HOLD` is directional:

- `WATCH`: "No signal yet, but one might be developing. Conditions are favorable. Don't act prematurely."
- `HOLD`: "There's an active structural reason to stay out. A bilateral break or RULES-triggered risk condition is in effect."

All three are useful outputs. All three tell you something.

---

## Multi-Timeframe Layering

The gate logic becomes especially interesting with multiple timeframes.

The RULES system includes a `tf_alignment` layer capturing the relationship between the signal timeframe and higher timeframes:

- **fully_aligned**: All timeframes moving in the same direction. Standard position size. Strong hold.
- **counter_trend**: Signal on the lower TF, opposing direction on higher TF. Smaller size. Pre-plan exit before higher-TF resistance.
- **transition**: Higher TF undergoing directional change. Cautious scaling. Wait for confirmation before adding size.

When a 1h signal is `GO` but the 4h is `counter_trend`, the RULES don't produce a simple "GO" recommendation — they produce a downgraded posture: take partial profit early, keep size small, watch for higher-TF structural resolution.

The ternary gate plus the 9-layer RULES system produce a nuanced operational picture that binary signals cannot represent.

---

## The Consultation Output

When the engine and RULES produce a state, the consultation service packages it into human-readable form:

```
📍 BTCUSDT  1h
Gate: GO
Rule: signal_fully_aligned
Progress: 42%
Sub-swing: 1

[Strategy] Standard position. All TFs aligned. Strong hold recommended.

[Your options]
  ① Hold to target
  ② 30% partial take-profit  
  ③ Full exit
```

When the sub-swing scope is at its second attempt or higher, an additional context line appears — not an alarm, but information. The trader sees that the counter-force is building.

---

## Why Three Is the Right Number

You could argue for more states. `MAYBE-GO`? `CONDITIONAL-WATCH`?

The problem is that each additional gate value requires more calibration, creates more edge cases, and provides diminishing returns on clarity. The goal is to capture the three **operationally distinct** situations, not every nuance.

Every additional nuance is better expressed in the RULES layer (9 layers, 30+ conditions) or the consultation's rationale text — not in the gate value itself.

The gate is a dispatcher. The RULES are the policy. The consultation is the explanation. Separation of concerns.

---

## The Honest Admission

The gate value isn't always right. The engine can output `GO` and the trade can fail. It can output `WATCH` indefinitely because the structural cycle never completes. It can output `HOLD` while a large move happens.

This is intentional design. The engine doesn't predict outcomes. It describes structural states. A `GO` gate with high label confidence doesn't mean "this trade will profit" — it means "the structural conditions for this signal type are present and high quality."

What you do with that information is your decision. The RULES system helps structure the decision. The consultation service explains it. But the responsibility remains with the trader or agent acting on the signal.

Engine states structure. RULES apply policy. Human or AI makes the call. That separation — maintained deliberately — is the core architectural principle.

---

## What's Coming Next

We've covered three layers: labeling (Article #11), state machine (Article #12), and operation gate (this article). Together they produce a structural state, operation context, and action gate.

But there's a fourth layer: the AI consultation service that takes all of this and explains it in natural language. And that's where the design gets philosophically interesting — because the AI's role is specifically *not* to make decisions.

That's the next article.

---

*← [Article 12: 5-State Machine](12_five_state_machine.md) · [Article 14: AI Explains, Engine Decides →](14_ai_explains_engine_decides.md)*

*Try the operation gate live: `curl "https://api.decker-ai.com/api/v1/signals/BTCUSDT/strategy"` · Full RULES.yaml: [operation_rules/RULES.yaml](../../../operation_rules/RULES.yaml)*
