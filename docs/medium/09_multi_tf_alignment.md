# Why Single-Timeframe Signals Fail — And How Multi-Timeframe Alignment Fixes It

*Your 1h signal is up 73%. Should you hold? It depends on what the 4h and 1d are doing — and most trading systems have no idea.*

---

## The Uncomfortable Question

Imagine this scenario:

You have a BTC long signal on the 1h chart.
- Entry: $96,000
- Target: $100,500
- Stop: $92,000
- Current: $99,300

Progress: **73%**. Almost there.

Every rule in your playbook says: *hold, let it run.*

But here's what your signal engine doesn't know:

```
1h:  A+ (upswing — your signal)     ← the signal you see
4h:  A- (downswing — in progress)   ← the wall you can't see
1d:  A- (downswing — in progress)   ← the bigger wall
```

You're 73% of the way to a target that sits right at a 4h resistance zone. The larger timeframes are actively working against you.

**Should you hold?**

Most trading engines say yes. The math says yes. The rule says hold at 73%.

I say: not without knowing what the 4h and 1d are doing.

---

## The Problem Nobody Talks About

Every trading system I've seen — from basic bots to sophisticated quant stacks — evaluates signals in isolation. One signal. One timeframe. One set of rules.

This works fine for simple setups. But markets are multi-layered. Price moves on every timeframe simultaneously. A 1h signal that looks strong can be swimming upstream against a 4h or daily trend.

I call this the **single-timeframe blindspot**: your signal engine measures where *you* are, but not where *the market* is.

Here's the practical consequence:

| Scenario | What a single-TF engine says | What actually happens |
|----------|------------------------------|-----------------------|
| 1h long, 4h/1d long | "Hold to target" | Signal runs to target ✅ |
| 1h long, 4h/1d short | "Hold to target" | Price reverses at 4h resistance ❌ |
| 1h long, 4h transitioning | "Hold to target" | Target reached if 4h confirms, fails if it doesn't |

The same rule. Completely different outcomes. **The difference is the multi-timeframe context** — which the engine is ignoring.

---

## The Solution: tf_alignment

After backtesting this problem across hundreds of signals, I added a single field to Decker's state engine output: `tf_alignment`.

It has five values:

| `tf_alignment` | Meaning | What it means for your signal |
|---|---|---|
| `fully_aligned` | Signal TF + all higher TFs same direction | Strongest setup. Hold to target. |
| `lower_aligned` | Signal + 1–2 higher TFs aligned, larger TF against | Good setup. Take partial at 4h resistance. |
| `counter_trend` | Most higher TFs against the signal direction | Weak setup. Exit at 50–70%. Don't push to target. |
| `transition` | A higher TF is testing a direction change (C swing) | Uncertain. Small entry, scale in if it confirms. |
| `mixed` | No clear pattern | Reduce position size. Treat as higher risk. |

The calculation is pure logic — no ML, no prediction:

```python
def compute_tf_alignment(signal_tf, signal_direction, all_tf_directions):
    # Get all timeframes higher than the signal TF
    higher_tfs = {
        tf: direction
        for tf, direction in all_tf_directions.items()
        if timeframe_is_higher(tf, signal_tf)
    }
    
    if not higher_tfs:
        return "fully_aligned"  # no higher context = proceed normally
    
    aligned = sum(1 for d in higher_tfs.values() if d == signal_direction)
    total = len(higher_tfs)
    
    if aligned == total:
        return "fully_aligned"
    elif aligned >= round(total * 0.6):
        return "lower_aligned"
    elif aligned == 0:
        return "counter_trend"
    else:
        return "mixed"
```

One function. No model. No training data. Just logic applied to the signals you already have.

---

## The Four Scenarios in Practice

### Scenario A: Counter-Trend Bounce

```
15m or 1h: A+ (upswing signal)   ← your entry
4h:        A- (downswing)
1d:        A- (downswing)

tf_alignment = counter_trend
```

**What's happening**: You're buying a bounce inside a larger downtrend. The market maker on 4h is likely selling into your upswing. Your 1h target sits at the 4h resistance price.

**Without tf_alignment**: Hold to 100%. Hit resistance at 70–75%. Price reverses. You give back gains.

**With tf_alignment = counter_trend**:
```yaml
- id: counter_trend_exit_fast
  tf_alignment: counter_trend
  progress_min: 60
  strategy: "Counter-trend signal past 60%. Exit 60–70% immediately.
             4h resistance likely nearby. Tighten stop on remainder."
```

You exit most of the position before the wall. Keep a small runner for a potential 4h breakout.

---

### Scenario B: Transition (The Best Trade Setup)

```
1h: A+ (upswing signal)
4h: C swing (direction change test — neither A+ nor A- confirmed)
1d: A- (downswing)
```

**What's happening**: The 4h just flipped from A- to a C swing — meaning it's *testing* a direction change. If 4h confirms A+, your 1h signal has a 4h tailwind. If 4h fails, you're still in a counter-trend.

**Without tf_alignment**: Same rule as before. Hold to target or don't. Binary.

**With tf_alignment = transition**:
```yaml
- id: transition_scale_in
  tf_alignment: transition
  progress_min: 30
  strategy: "4h direction change in progress. Start small (3–5%).
             Add position on 4h A+ confirmation. Target = 1d resistance."
```

This is where the best risk/reward setups come from: entering during a potential trend change at 1h, scaling in as 4h confirms, with 1d resistance as the natural target.

---

### Scenario C: Lower Aligned

```
1h: A+ (upswing)
4h: A+ (upswing)   ← aligned
1d: A- (downswing) ← against
```

**What's happening**: You have 1h and 4h working together, but the 1d is still in a downswing. The signal has real momentum, but the 1d puts a ceiling on the upside.

**Strategy**: Mid-sized position (4–6%). Take partial at 50–66% progress. The 1d resistance is likely to cap the move.

---

### Scenario D: Fully Aligned

```
1h: A+ (upswing)
4h: A+ (upswing)
1d: A+ (upswing)
```

**What's happening**: All timeframes moving the same direction. The "intentions" stack up — small TF aligning with large TF momentum.

**Strategy**: Full position (5–8%). Let it run. The progress-based rules apply without the override.

---

## The Code: Where It Lives

In Decker's architecture, `tf_alignment` flows from signal storage through to the rule matching layer:

```
judgment_signals (DB)
    ↓ multiple TFs for same symbol
build_tf_alignment_context()
    ↓
user_context = {
    "tf_alignment": "counter_trend",
    "swing_state": "B",
    "entry_timing": "signal",
    ...
}
    ↓
RULES.yaml matching
    ↓ first rule that matches all conditions
strategy text returned to user
```

The key insight: `tf_alignment` is **just another field in the context dictionary**. The YAML rulebook already knows how to match on it. No new architecture needed — just a new dimension of state.

---

## What Changed in the Rulebook

Before multi-TF alignment, our RULES.yaml had 17 rules based on `progress_pct`, `status`, and `timeframe`.

After, it has 35+ rules organized in layers:

```
Layer 1: Status (target_reached, stop_hit)         — always first
Layer 2: Portfolio weight                          — when portfolio context exists
Layer 3: Entry timing (predictive/signal/confirm)  — when entry_timing is set
Layer 4: TF Alignment (fully_aligned → counter_trend) — when tf_alignment is set
Layer 5: Swing state (A/B/C)                       — when swing_state is set
Layer 6: Market state (trend, range)               — always evaluated
Layer 7: Timeframe-specific                        — 4h, 1h overrides
Layer 8: Progress (66%, 80%, 90%+)                 — the baseline
Layer 9: Fallback default                          — always matches
```

The important rule: **if a layer's field is missing from user_context, that layer is skipped entirely**. A signal with no `tf_alignment` data gets served the baseline progress rules, exactly as before.

This is backward-compatible by design. Existing signals work. New signals with multi-TF data get richer context.

---

## The Response Difference

Same signal, same progress. Different context.

**Before (no tf_alignment)**:
```
BTCUSDT long 73% — Signal at 66%+. Take 30% partial profit.
Hold remainder to target.
```

**After (tf_alignment = counter_trend)**:
```
BTCUSDT long 73% — [Counter-Trend Bounce]
1h A+ signal, but 4h/1d downswing active.
73% progress = likely near 4h resistance zone.
Exit 60–70% immediately. Tighten stop on remainder.
Do not target the original target — that's inside 4h resistance.
```

**After (tf_alignment = fully_aligned)**:
```
BTCUSDT long 73% — [All TF Aligned Trend]
1h, 4h, 1d all in upswing. Strong trend structure.
Take 30% partial at 73%. Hold remainder with confidence.
Target remains valid — no higher-TF resistance in the way.
```

The math is the same. The signal is the same. The action is completely different.

---

## Implementation: What You Actually Need

To implement this in your own system, you need:

1. **Store signals per timeframe** — you need 1h, 4h, and 1d signals for the same symbol in your database.

2. **Compute tf_alignment at query time** — call `compute_tf_alignment()` using the current directions across all timeframes.

3. **Pass it to your rule engine** — add it to whatever context dict or state object feeds your decision layer.

4. **Add conditional rules** — write rules that fire only when `tf_alignment` matches. Rules without the field are unaffected.

That's it. Four steps. No ML pipeline. No new model. No training data.

The utility is [open source](https://github.com/gigshow/decker-ai-strategy-builder/blob/main/utils/tf_alignment_utils.py) in the repo.

---

## The Deeper Point

Markets are a hierarchy of timeframes. Every participant — from retail traders on the 5m to institutional desks on the weekly — is simultaneously interacting with price.

A 1h signal is an event at one layer of that hierarchy. Whether it succeeds depends heavily on what the larger layers are doing. Counter-trend signals can work, but they need different management. Aligned signals can run further. Transition setups offer the best R/R if you manage size correctly.

The traditional approach: ignore the hierarchy, apply the same rule to every signal.

The multi-TF approach: **know where your signal sits in the hierarchy, and let that change how you manage it.**

No prediction required. Just awareness.

---

## What's Next

This article covered the concept and scenarios. The next article in this series covers how Decker's rulebook *learns from real trade outcomes* — using win rates segmented by `tf_alignment`, `entry_timing`, and `swing_state` to automatically propose rulebook patches.

State machine + learning loop. Still no ML. Still deterministic. But now the rules improve over time.

---

*If this resonated, the full rulebook, utils, and signal format are documented at the [Decker AI Strategy Builder repo](https://github.com/gigshow/decker-ai-strategy-builder). The Telegram bot is at [@DeckerClawBot](https://t.me/deckerclawbot).*
