# How I Encoded a Trading Strategy Engine in YAML

*No neural networks. No training loop. No model serving. Just a readable rulebook for the execution layer.*

---

## The Strategy Engine Problem

Every trading system eventually faces the same question: **how do you encode strategy?**

The industry's answer has been: throw machine learning at it.

- Train a neural network on 5 years of candle data
- Fine-tune hyperparameters for weeks
- Deploy the model, pray it generalizes
- Retrain every month when the market shifts
- Pay for GPU time, data pipelines, model serving

I explored that path for a while. What bothered me was not just cost, but complexity: training, monitoring, deployment, and then explaining why the output changed when the market regime changed.

Then I asked: **what if I wrote down what I actually do when I trade, in a format a machine could read?**

---

## A Small Rulebook, $0 in Core-Path Token Costs

This is a representative excerpt from Decker AI's public rulebook:

```yaml
version: "1.4.0"
rules:
  - id: target_reached
    status: target_reached
    strategy: "Target reached. Full exit."

  - id: stop_hit
    status: stop_hit
    strategy: "Stop zone. Exit or hold."

  - id: progress_95
    progress_min: 95
    strategy: "Near target (95%+). Take 80% or full exit."

  - id: progress_90
    progress_min: 90
    risk_appetite: [low, medium]
    strategy: "90%+ progress. Take 70% partial. Hold rest to target."

  - id: progress_80_trend
    progress_min: 80
    market_state: [trend]
    strategy: "Trending market, 80%+. Take 50%. Hold rest to target."

  - id: progress_80
    progress_min: 80
    risk_appetite: [low, medium]
    strategy: "80%+ progress. Take 50% partial. Hold to target."

  - id: progress_66_4h
    progress_min: 66
    timeframe: "4h"
    strategy: "4h timeframe, 66%. Take 40% partial. Larger TF = conservative."

  - id: progress_66_1h
    progress_min: 66
    timeframe: "1h"
    strategy: "1h timeframe, 66%. Take 35% partial. Short TF = faster exit."

  - id: progress_66
    progress_min: 66
    strategy: "66% progress. Take 30% partial. Hold rest to target."

  - id: progress_50
    progress_min: 50
    strategy: "50% progress. Take 20% or hold. Risk-dependent."

  - id: progress_33
    progress_min: 33
    risk_appetite: [low]
    strategy: "33% progress. Take 5% early profit or hold."

  - id: default
    strategy: "In progress. Hold to target."
```

The important point is not the exact line count. It's that the strategy layer is readable and explicit.

No model weights. No training loop. No inference server. **Just a YAML file that a junior developer could read and understand in 5 minutes.**

---

## How the Matching Works

The logic is deliberately simple. Top-to-bottom scan, first match wins:

```
Input:
  progress_pct = 72%
  timeframe = 4h
  risk_appetite = medium
  market_state = range
  status = in_progress

Scan rules:
  ❌ target_reached → status doesn't match
  ❌ stop_hit → status doesn't match
  ❌ progress_95 → 72 < 95
  ❌ progress_90 → 72 < 90
  ❌ progress_80_trend → 72 < 80
  ❌ progress_80 → 72 < 80
  ✅ progress_66_4h → 72 ≥ 66 AND timeframe = 4h → MATCH!

Output:
  "4h timeframe, 66%. Take 40% partial profit."
```

Time complexity is O(n) over the rule count. In practice, it is lightweight because it is doing rule matching rather than model inference.

The first-match approach means **rule ordering is the priority system**. Rules at the top are checked first. `target_reached` and `stop_hit` always take precedence — because if you've hit your target or your stop, nothing else matters.

---

## Why YAML Beats ML for This Problem

I'm not anti-ML. I use machine learning where it makes sense. But for strategy execution — deciding what to do at each stage of a signal — YAML has structural advantages:

### 1. Transparency

```yaml
- id: progress_80
  progress_min: 80
  strategy: "Take 50% partial. Hold rest to target."
```

Every user can read this. Every developer can audit this. Try explaining what a 12-layer neural network decided and why.

When a user asks "why did the bot take profit at 80%?", the answer is: "Because rule `progress_80` says so, and you can see it right here." No black box.

### 2. Determinism

Same input → same output. Always. No randomness, no floating point drift, no model version differences.

This matters enormously for:
- **Debugging**: reproduce any decision by replaying the input
- **Backtesting**: results are perfectly reproducible
- **Trust**: users know the system is consistent

### 3. Zero Cost

ML inference costs money. LLM calls cost money. Fine-tuning costs money.

YAML matching is cheap. The strategy path in Decker AI uses zero LLM tokens on the core rule-based path.

At scale, that changes the economics of the product because explanation cost and decision cost are no longer the same thing.

### 4. Instant Iteration

Want to add a new rule for 1-day timeframes?

```yaml
  - id: progress_80_1d
    progress_min: 80
    timeframe: "1d"
    strategy: "Daily timeframe, 80%. Take 30% conservative partial."
```

Add 4 lines. Deploy. Done. No retraining, no validation set, no hyperparameter tuning, no A/B testing the model. The rule is live in seconds.

### 5. Market-State Awareness

Version 1.4.0 added `market_state` conditions:

```yaml
  - id: progress_80_trend
    progress_min: 80
    market_state: [trend]
    strategy: "Trending market. Take 50%. Hold rest."

  - id: progress_66_range
    progress_min: 60
    progress_max: 75
    market_state: [range]
    strategy: "Range market near 66%. Take 40% partial. Scalping response."
```

Same progress level, different strategy based on market regime. An ML model would need to learn this from data. In YAML, it's two rules that a trader can write from experience.

---

## The Tier System: Free, Standard, Premium

Not all rules are created equal. Decker AI uses tiers to differentiate:

| Tier | Rules | Who Gets It |
|------|-------|-------------|
| **Basic** | `target_reached`, `stop_hit`, `default` | Everyone (Free) |
| **Standard** | `progress_50`, `progress_66`, `progress_80`, `progress_90`, `progress_80_trend` | Pro subscribers |
| **Premium** | `progress_33`, `progress_40`, `progress_66_4h`, `progress_66_1h`, `progress_80_1d`, `progress_66_range`, portfolio rules | Trader/API tier |

Free users get the essentials: exit at target, exit at stop, hold otherwise. Paying users get the nuanced mid-lifecycle strategies that make the difference between a good return and a great one.

This is also a business model insight: **the value isn't in the signal — it's in knowing what to do at each stage of the signal.** The signal is the appetizer. The lifecycle strategy is the main course.

---

## But Can YAML Really Replace ML?

Fair question. Here's my honest take:

**YAML replaces ML for strategy execution.** Given a known market state (progress_pct, status, timeframe, regime), the optimal action is a lookup, not a prediction.

**YAML does not replace ML for signal generation.** Identifying structural targets, evaluating market objects, detecting swing patterns — this is where algorithms (though not necessarily ML) add value.

Decker AI's architecture separates these concerns:

```
Signal generation → Labeling algorithm (algorithmic, not ML)
State computation → State engine (deterministic math)
Strategy execution → YAML rulebook (zero-cost lookup)
User interface → LLM (optional, explanation only)
```

Each layer uses the tool best suited for the job. ML for pattern recognition if needed. Math for state computation. YAML for strategy. LLM for conversation. No layer does more than it should.

---

## Fork It. Modify It. Make It Yours.

The entire RULES.yaml is open source. You can:

1. **Fork the repo** and modify rules for your risk profile
2. **Add timeframe-specific rules** for your preferred trading style
3. **Create market_state rules** for trending vs range conditions
4. **Submit a PR** with rules that worked for you

```bash
# See the full rulebook
curl -s "https://raw.githubusercontent.com/gigshow/decker-ai-strategy-builder/main/operation_rules/RULES.yaml"

# Test it live — what strategy does BTCUSDT get right now?
curl -s "https://api.decker-ai.com/api/v1/signals/BTCUSDT/strategy?timeframe=4h&risk_appetite=medium"
```

The goal is to build a community-driven rulebook. The public rulebook is a starting point, not a finish line. Each added rule should make the system more transparent, auditable, and deterministic.

---

## Coming Up Next

- **#5** — Building a Crypto Signal API in 5 Minutes — No ML Degree Required
- **#6** — What the Public Backtest Summary Suggests About `progress_pct`

Full resources:
- **GitHub**: [decker-ai-strategy-builder](https://github.com/gigshow/decker-ai-strategy-builder)
- **Telegram**: [@deckerclawbot](https://t.me/deckerclawbot)
- **API**: [api.decker-ai.com/docs](https://api.decker-ai.com/docs)
- **Web**: [decker-ai.com](https://decker-ai.com)

---

*The best strategy engine isn't the smartest. It's the one you can read, trust, and modify in under a minute.*

---

**Tags**: `YAML`, `Trading Bot`, `Algorithmic Trading`, `AI Trading`, `Cryptocurrency`, `State Machine`, `Open Source`, `Python`, `DevOps`, `Fintech`
