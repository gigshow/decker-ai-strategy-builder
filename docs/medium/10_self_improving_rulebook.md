# How I Built a Trading Rulebook That Improves Itself

*Every rule I wrote was based on intuition. Then I started collecting trade outcomes — and the data started telling me where the rules were wrong.*

---

## The Rules Were Mine

In [article 4](04_yaml_rules.md), I described how Decker AI replaced a complex decision tree with a YAML rulebook. Simple conditions. Human-readable strategies. No ML.

It worked. Users liked it. The rules made sense.

But there was a nagging problem: **I wrote those rules myself.**

Every `progress_min`, every partial exit percentage, every exit multiplier — those were my instincts formalized into YAML. And instincts, by definition, are unverified.

What if the 66% partial exit should actually be at 60%? What if counter-trend signals should exit at 55% instead of 66%? What if my "take 30% at 66%" rule is wrong for fully-aligned setups but right for counter-trend ones?

I had no way to know. Until I started collecting the data.

---

## The Learning Feedback Loop

The architecture is simple. Every time a trade closes — whether it hits the target, the stop, or a partial exit — Decker now logs a row to a `trade_outcomes` table:

```sql
CREATE TABLE trade_outcomes (
    execution_id        INTEGER,
    symbol              TEXT,
    timeframe           TEXT,
    direction           TEXT,
    entry_timing        TEXT,          -- predictive | signal | confirmation
    tf_alignment        TEXT,          -- fully_aligned | lower_aligned | counter_trend | transition | mixed
    swing_state         TEXT,          -- A | B | C
    entry_progress_pct  FLOAT,
    outcome             TEXT,          -- win | loss | partial
    actual_rr           FLOAT,
    rule_matched        TEXT,
    executed_at         TIMESTAMPTZ
);
```

Notice the dimensions: `entry_timing`, `tf_alignment`, `swing_state`. Not just "did it win?" — but "did it win *in this specific market context*?"

That's the key. Aggregate win rates are meaningless. Win rates by context are actionable.

---

## Why Aggregate Win Rates Lie

Consider this: your system has a 57% win rate on BTC longs. Sounds decent.

Now break it down:

| `tf_alignment` | `entry_timing` | Win Rate |
|---|---|---|
| `fully_aligned` | `signal` | 71% |
| `lower_aligned` | `signal` | 61% |
| `counter_trend` | `signal` | 38% |
| `fully_aligned` | `predictive` | 52% |
| `counter_trend` | `predictive` | 29% |

Your 57% aggregate is the average of a 71% win-rate setup and a 29% win-rate setup. You've been treating them identically. You've been applying the same "take 30% at 66%" rule to both.

**The aggregate hides what the segments reveal.**

The first question the segmented data answers: which contexts should have which rules?

---

## The Three Signal Dimensions

Decker now segments every trade outcome across three axes:

### 1. `tf_alignment`
How aligned is the signal with higher timeframes?

- `fully_aligned` — all higher TFs same direction
- `lower_aligned` — 1–2 higher TFs aligned, not all
- `counter_trend` — most higher TFs in opposite direction
- `transition` — a higher TF is in a direction-change test (C swing)
- `mixed` — no clear pattern

### 2. `entry_timing`
At what stage was the signal generated?

```
Prediction zone  [─────0-20%]   Signal predicted before it forms
Signal zone      [────20-45%]   Signal confirmed, entry opens
Confirmation     [───45-70%]   Late entry — signal well-underway
```

- `predictive`: entered 0–20% of the signal's progress — before confirmation
- `signal`: standard entry window, 20–45%
- `confirmation`: late entry, 45–70%, signal already extended

### 3. `swing_state`
What part of the market's swing cycle is this signal in?

- `A`: main swing — the dominant move (upswing or downswing)
- `B`: sub-swing — a correction within A (countermovement)
- `C`: transition — testing a direction change, high uncertainty

These three dimensions combine to describe the context of any given signal entry. And the data is already there — these fields are stored in `judgment_signals` and flow through to `trade_outcomes` when a trade closes.

---

## The Aggregator

A nightly job runs this query:

```python
async def aggregate_signal_performance(db, days_back=90):
    rows = await db.fetch("""
        SELECT
            tf_alignment,
            entry_timing,
            swing_state,
            timeframe,
            COUNT(*) as total,
            SUM(CASE WHEN outcome = 'win' THEN 1 ELSE 0 END) as wins,
            AVG(actual_rr) as avg_rr,
            ARRAY_AGG(DISTINCT rule_matched) as rules_used
        FROM trade_outcomes
        WHERE created_at > NOW() - INTERVAL '$1 days'
        GROUP BY tf_alignment, entry_timing, swing_state, timeframe
        HAVING COUNT(*) >= 10
        ORDER BY wins::float / COUNT(*) DESC
    """, days_back)
    
    return [dict(r) for r in rows]
```

The `HAVING COUNT(*) >= 10` clause ensures we don't draw conclusions from insufficient samples.

The output is a ranked table: every observed context bucket, with its win rate and average R/R.

---

## What the Data Looks Like After 90 Days

Early results from real signal data (abbreviated for illustration):

```
tf_alignment=fully_aligned, entry_timing=signal, swing_state=A
  total=47, win_rate=68%, avg_rr=1.34
  rules_used=[progress_66, progress_80_trend]
  → Performing well. No change needed.

tf_alignment=counter_trend, entry_timing=signal, swing_state=B
  total=31, win_rate=39%, avg_rr=0.71
  rules_used=[progress_66, progress_80]
  → Problem: applying same 66% hold rule to counter-trend B swing
  → Suggested patch: exit at 55% for counter_trend + B combo

tf_alignment=transition, entry_timing=predictive, swing_state=C
  total=12, win_rate=58%, avg_rr=1.67
  rules_used=[progress_33]
  → High R/R when it works. Sample too small.
  → Flag for monitoring. Don't patch yet.
```

The system doesn't patch automatically. It proposes. A human reviews and approves.

---

## From Data to Rule Patch

When a context bucket consistently underperforms, the system generates a proposed patch:

```
[PATCH PROPOSAL — 2026-03-18]

Observation:
  counter_trend + signal + B-swing
  win_rate: 39% (31 trades, 90 days)
  avg_rr: 0.71
  current rule: progress_66 → "Take 30% partial at 66%"

Proposed Patch:
  id: counter_trend_b_swing_exit
  tf_alignment: counter_trend
  swing_state: B
  entry_timing: signal
  progress_min: 50
  strategy: "Counter-trend B-swing signal at 50%+.
             Sub-swing bounce likely near peak.
             Exit 60% at first resistance. Do not target original price."

Expected Effect:
  Earlier exit captures available profit before B-swing exhaustion.
  Reduces loss_rate on B-swing counter-trend from 61% → estimated 44%.
```

The patch adds a new YAML rule that fires *before* the generic `progress_66` rule for this specific context. It doesn't break anything — it narrows the context.

This is the key architectural decision: **rules are ordered, and more specific rules win**. Adding a counter_trend + B-swing rule doesn't change behavior for fully_aligned signals. The rulebook is additive, not destructive.

---

## The Architecture: How It All Fits Together

```
                      ┌───────────────────────────┐
  Signal fires        │   judgment_signals (DB)   │
  ─────────────────→  │   + tf_alignment           │
                      │   + entry_timing           │
                      │   + swing_state            │
                      └───────────┬───────────────┘
                                  │
                      ┌───────────▼───────────────┐
  Trade executes      │  strategy_builder_executions│
  ─────────────────→  │  (entry, stop, target)    │
                      └───────────┬───────────────┘
                                  │
                      ┌───────────▼───────────────┐
  Trade closes        │     trade_outcomes         │
  ─────────────────→  │  (outcome + all context)  │
                      └───────────┬───────────────┘
                                  │
                      ┌───────────▼───────────────┐
  Nightly job         │  signal_performance_       │
  ─────────────────→  │  aggregator.py             │
                      │  (win_rate per segment)   │
                      └───────────┬───────────────┘
                                  │
                      ┌───────────▼───────────────┐
  Human review        │  RULES.yaml patch proposal │
  ─────────────────→  │  (add/update specific rule)│
                      └───────────────────────────┘
```

No automated rule updates. No reinforcement learning. No gradient descent.

Just: observe → measure → propose → human decides → update.

The learning loop is slow. But it's auditable, reversible, and builds compound knowledge over time.

---

## The Snowball Effect

After 3 months, this is what the rulebook evolution looks like:

**Version 1.0**: 17 rules, all based on `progress_pct`
**Version 1.4**: 25 rules, added `timeframe` and `market_state` conditions
**Version 2.0**: 35+ rules, added `tf_alignment`, `entry_timing`, `swing_state` layers

Each addition narrows the context in which a rule fires. The newer rules don't replace the old ones — they sit in front of them for specific conditions.

The underlying logic: **as you collect more data, you can make more distinctions**. A rule that applies to all signals gives way to rules that apply to fully_aligned signals, which give way to rules that apply to fully_aligned + signal-timing + A-swing signals.

The more data you have, the more specific you can be, the better the outcomes.

And crucially: **you can trace every recommended action back to a specific rule, which traces back to a specific segment of historical outcomes**. The entire system is explainable end-to-end.

---

## What This Is Not

This is not ML. There is no model. There are no embeddings. No tokenization.

The "learning" is:
1. Collect labeled outcomes
2. Aggregate by context buckets
3. Identify underperforming contexts
4. Propose rule patches
5. Human approves
6. YAML file updated

It's closer to what a doctor does when reviewing a treatment protocol: look at outcomes by patient type, update the protocol for subgroups that aren't responding. Not AI. Just organized empiricism.

The reason this works in trading is that market context is finite and repeatable:
- Timeframe alignments recur
- Swing states recur
- Entry timings recur

The combinations are bounded. You can enumerate them, measure outcomes per combination, and write rules that differentiate between them.

---

## What's Still Missing

The feedback loop has one gap: **the exit context**. We record `entry_progress_pct` but we don't yet track `exit_progress_pct` — where the position was when it actually exited.

This matters because some trades close at 90% progress due to a partial exit rule, while others at the same progress close because the stop was hit after a reversal. Same `entry_progress_pct`. Very different stories.

The next phase: store the full position lifecycle. Not just entry state → outcome, but entry → partial exits → final close, with price context at every step.

Once you have that, you can answer questions like: "For counter_trend + signal + B-swing setups, at what exact progress% do most winners turn into losers?"

That's the precision level where the rulebook becomes genuinely systematic, not just experientially tuned.

---

## The Bigger Picture

Trading strategy is usually treated as art or science. Either you have "feel" for the market (art) or you run an ML model (science).

I think there's a third path: **structured empiricism with human judgment in the loop**.

You observe systematically. You measure carefully. You propose changes based on evidence. You review them with your own knowledge. You update deliberately.

The rules don't decide themselves. You decide — but with better information than you had before.

That's what Decker's feedback loop is. Not AI replacing judgment. **Data sharpening it.**

---

*The signal schema, RULES format, and rule structure are open source in the [Decker AI Strategy Builder repo](https://github.com/gigshow/decker-ai-strategy-builder). The trade outcome collector and aggregator are part of the core pipeline; the concept and schema are documented in [strategy-dsl](https://github.com/gigshow/decker-ai-strategy-builder/blob/main/docs/strategy-dsl.md) and this article.*
