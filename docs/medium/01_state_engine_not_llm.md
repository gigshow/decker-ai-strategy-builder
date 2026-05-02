# I Built a Trading Engine That Doesn't Use AI to Predict Prices — Here's Why

*Every AI trading bot on the market tries to predict where the price will go. I built one that takes a different route: measure state first, then apply rules.*

---

## The Problem with AI Price Prediction

Open any AI trading article on Medium right now. You'll see the same architecture:

1. Feed historical price data into an ML model
2. Train it to predict the next candle / direction / price
3. Generate BUY or SELL signals
4. Hope the model generalizes

I've read dozens of these. I've built some myself. And I kept running into the same wall: **prediction models degrade**. Markets shift. What worked in a bull run fails in a range. What worked in low volatility breaks in high volatility.

The fundamental issue? Prediction is the wrong abstraction for trading.

Here's what I mean. When a doctor checks your blood pressure, they don't *predict* your blood pressure. They *measure* it. Then they look up the reading in a decision table — normal, elevated, stage 1, stage 2 — and each stage has a protocol.

What if we could do the same for trading signals?

---

## The Idea: Measure, Don't Predict

I started with a question: **What if a trading signal has a lifecycle — like a battery draining from 100% to 0% — and the strategy should change based on how far along it is?**

Think about it. A signal is generated with three numbers:
- **Entry price**: where you get in
- **Target price**: where you want to get out
- **Stop loss**: where you cut losses

Once you have those three numbers plus the current price, you can calculate exactly how far the signal has progressed toward its target. No AI needed. No prediction needed. Just arithmetic.

I call this **progress_pct** — the percentage of progress from entry to target.

```
Long:  progress_pct = (current_price - entry) / (target - entry) × 100
Short: progress_pct = (entry - current_price) / (entry - target) × 100
```

A signal at 20% progress is in its early stage. At 66%, it's past the halfway point. At 90%, it's about to hit the target. Each stage demands a completely different strategy.

This is not prediction. This is **measurement**. And the difference matters.

---

## What This Looks Like in Practice

Let's say you have a BTC long signal:
- Entry: $96,000
- Target: $100,000
- Stop loss: $92,000

Current price is $98,640.

```
progress_pct = (98640 - 96000) / (100000 - 96000) × 100 = 66%
```

Now compare what two systems tell you:

| System | Output |
|--------|--------|
| Traditional AI bot | "BUY" or "SELL" |
| **Decker AI** | "BUY + progress 66% → take 30% partial profit, hold the rest to target" |

The traditional bot gives you a binary signal. Decker AI tells you *where you are* in the signal's lifecycle and *exactly what to do* at this stage.

This is the core of what I built: **Decker AI — an AI Market State Engine**.

---

## State Engine, Not LLM

Here's the architecture difference that makes this work:

| Aspect | Typical AI Trading | Decker AI |
|--------|-------------------|--------|
| Signal generation | ML / model-based prediction | **Deterministic state engine** |
| Core output | "BUY" / "SELL" | progress_pct, status, strategy |
| LLM role | Prediction & judgment | **Interface & explanation only** |
| Core-path token cost | Often non-zero | **$0** (rule-based path) |

Every other AI trading system I've seen uses the LLM as the brain. Decker AI uses it as the mouth.

The brain is a deterministic state engine:

```
Time series data
    → [Labeling Algorithm] → Object evaluation, labels (S, T, 1)
    → [State Engine]       → progress_pct, status
    → [Operation Rules]    → Strategy (RULES.yaml, first match)
    → Web / Telegram / API
```

The signal comes from market structure analysis. The state engine computes progress. The operation rulebook matches the right strategy. None of this requires an LLM call.

The LLM only steps in when a user asks "what should I do with this signal?" in natural language — and even then, it's explaining a decision that was already made deterministically.

---

## The Operation Rulebook: A Public YAML Rulebook

Instead of training a model, I wrote a YAML rulebook. Each rule maps a progress range to a specific strategy:

```yaml
- id: progress_66
  progress_min: 66
  status: [in_progress]
  timeframe: [4h, 8h]
  risk_appetite: [medium, high]
  action: "30% partial profit. Hold remaining to target."
  description: "Signal past 66% — lock in gains, ride the rest"

- id: progress_90
  progress_min: 90
  status: [in_progress]
  timeframe: [1h, 4h, 8h]
  risk_appetite: [low, medium, high]
  action: "70-80% partial profit. Tight stop on remainder."
  description: "Signal near target — secure most of the position"
```

The matching logic is simple: scan rules top-to-bottom, return the first match where `progress_pct >= progress_min` and the other conditions (status, timeframe, risk appetite) align.

**No gradient descent. No hyperparameters. No overfitting. No token costs.** Just a deterministic lookup that returns the same answer every time for the same input.

---

## What the Public Backtest Summary Shows

What matters publicly is not "YAML beats ML" as a universal law, but whether the lifecycle framing is useful. The current public performance summary shows a clear pattern.

**Win Rate by progress range:**

| Progress Range | Win Rate | Samples | Notes |
|---------------|----------|---------|-------|
| 33–60% | 55–65% | ~120 | Entry timing sensitive |
| 61–80% | 65–75% | ~90 | Partial profit effect |
| 81–95% | 70–80% | ~70 | Near-target advantage |
| 95–100% / target | 80–90% | ~50 | Full exit zone |

**Win Rate by market regime:**

| Regime | Monthly Return | Win Rate | Signals/Month |
|--------|---------------|----------|---------------|
| Range-bound | 20–30% | 50–70%+ | 8–12 |
| Trending | 30–60%+ | 70%+ | 10–18 |

The key insight: **higher progress = higher completion probability in the published backtest summary**. If a signal has already traveled 80% toward its target, it is generally in a different risk state than a fresh signal. The rulebook reflects that by taking more profit as progress increases.

Average stop loss is listed at 1–2%. Max drawdown is listed at 3–4%. The published risk:reward range increases as progress rises.

---

## Try It Right Now

The API is live and public. No API key required for read endpoints.

**Check any signal's state:**

```bash
curl -s "https://api.decker-ai.com/api/v1/signals/BTCUSDT/state"
```

**Get the strategy recommendation:**

```bash
curl -s "https://api.decker-ai.com/api/v1/signals/BTCUSDT/strategy?timeframe=1h&risk_appetite=medium"
```

**Push your own signal and get a strategy back:**

```bash
curl -s -X POST "https://api.decker-ai.com/api/v1/signals/push" \
  -H "Content-Type: application/json" \
  -d '{"symbol":"BTCUSDT","timeframe":"1h","direction":"long","entry_price":96000,"target_price":100000,"stop_loss":92000}'
```

Or use Python:

```python
import requests

API = "https://api.decker-ai.com/api/v1"

def get_signal_state(symbol: str) -> dict:
    r = requests.get(f"{API}/signals/{symbol}/state", timeout=10)
    r.raise_for_status()
    return r.json()

state = get_signal_state("BTCUSDT")
print(f"progress: {state['progress_pct']}%")
print(f"status: {state['status']}")
```

That's it. No ML pipeline. No model training. No GPU costs. Just a REST call that returns exactly where a signal stands and what to do about it.

---

## Why This Matters Beyond Crypto

I built Decker AI for crypto first, and the public repo is documented from that angle. But the underlying idea is broader: if you have a signal with a defined entry, target, and stop, you can compute progress and manage the lifecycle deterministically.

That is the real bet here: state over prediction for the execution layer. Not because prediction is useless, but because many post-entry decisions can be expressed more clearly as measurement plus policy.

---

## What's Next

This is the first article in a series about building Decker AI. Coming up:

- **#2** — Why Most Trading Bots Fail: The Missing Concept of Signal Lifecycle
- **#3** — Target → Signal → Entry: The Philosophy That Changed How I Think About Trading
- **#4** — How I Encoded a Trading Strategy Engine in YAML

If you want to explore the engine:

- **GitHub**: [decker-ai](https://github.com/gigshow/decker-ai) — architecture, samples, RULES.yaml
- **Telegram Bot**: [@deckerclawbot](https://t.me/deckerclawbot) — try it live
- **API Docs**: [api.decker-ai.com/docs](https://api.decker-ai.com/docs)
- **Website**: [decker-ai.com](https://decker-ai.com)

If this resonated, a ⭐ on GitHub or a follow here helps me keep building in public.

---

*Decker AI doesn't predict where the market will go. It measures where the market already is — and that turns out to be far more useful.*

---

**Tags**: `AI Trading`, `Algorithmic Trading`, `Cryptocurrency`, `State Machine`, `Trading Bot`, `Python`, `API`, `Bitcoin`, `Market Analysis`, `Fintech`
