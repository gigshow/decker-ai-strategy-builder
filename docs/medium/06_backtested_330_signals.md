# What Decker's Public Backtest Summary Suggests About `progress_pct`

*It wasn't RSI. It wasn't MACD. It wasn't sentiment. It was a percentage the public docs make central: `progress_pct`.*

---

## The Question

I had a simple hypothesis: **the further a trading signal has progressed toward its target, the more likely it is to complete.**

That sounds obvious, but most trading content still focuses on entries alone. The more useful question for execution is **where the signal is when you make the decision**.

The public repo currently shares bucketed backtest summaries rather than a full raw dataset dump. So this article should be read as an interpretation of those published summaries, not as a fully released research paper.

The single variable I want to focus on is **progress_pct**: how far the signal has traveled from entry toward target at the time of a decision.

---

## The Published Summary

| Parameter | Value |
|-----------|-------|
| Scope | Public backtest summary in `signal-performance.md` |
| Asset framing | Crypto / spot-oriented public documentation |
| Timeframes | Multiple timeframes discussed in public docs and API |
| Signal type | Signals with defined entry / target / stop |
| Strategy | `RULES.yaml` progress-based lifecycle strategy |

The published material includes:
- Progress buckets with win-rate ranges
- Market-regime summaries for range-bound and trending conditions
- Drawdown, average stop-loss, and risk:reward summaries

---

## Finding #1: Higher Progress Buckets Show Higher Completion Rates

This is the core published pattern:

| Progress Range | Win Rate | Sample Size |
|---------------|----------|-------------|
| 33–60% | 55–65% | ~120 signals |
| 61–80% | 65–75% | ~90 signals |
| 81–95% | 70–80% | ~70 signals |
| 95–100% | 80–90% | ~50 signals |

**The higher the progress bucket, the higher the published completion probability.**

At first glance, this might seem circular. But for execution, it matters because not all in-flight signals should be managed the same way.

Most traders make the same mistake: they treat a signal at 40% the same as a signal at 80%. Same position size. Same stop. Same exit plan. The data says this is wrong. **A signal at 80% is a fundamentally different trade than one at 40%.** The risk profile, the optimal exit strategy, and the expected outcome are all different.

This is exactly what progress_pct quantifies — and what the RULES.yaml rulebook acts on.

---

## Finding #2: Market Regime Still Matters

The public docs split the summary by market regime:

| Regime | Monthly Return | Win Rate | Signals/Month | Avg Duration |
|--------|---------------|----------|---------------|-------------|
| **Range-bound** | 20–30% | 50–70%+ | 8–12 | 6–18h |
| **Trending** | 30–60%+ | 70%+ | 10–18 | 4–48h |

In range-bound markets — the kind that kills most momentum strategies — Decker AI still produced 20–30% monthly returns. Why?

Because in a range, signals bounce between structural highs and lows. Each bounce creates a new signal with a defined target. The progress_pct tracks each bounce independently. While momentum traders sit idle waiting for a breakout, the lifecycle approach trades each range swing.

In trending markets, the numbers get better. Signals move faster toward targets, spend less time in risky early stages, and complete at higher rates. The public rulebook now also includes market-state-aware branches, so the lifecycle framework and the regime-aware rules work together rather than being in conflict.

---

## Finding #3: The Risk:Reward Curve Is Not Flat

Most traders assume a fixed risk:reward ratio. "I always aim for 2:1." The backtest showed something more nuanced:

| Progress Range | Avg Profit (win) | Avg Loss (loss) | Realized R:R |
|---------------|------------------|-----------------|-------------|
| 33–60% | 3–5% | -1–2% | 1.5–2.5 |
| 61–80% | 4–7% | -1–2% | 2.0–3.5 |
| 81–95% | 5–10% | -1–2% | 2.5–5.0 |
| Target reached | 8–15% | — | — |

The loss side is consistent: 1–2% per trade, because the stop loss is tight and fixed. But the **profit side scales with progress.** Signals that reach 80%+ before you take action have already proven they're moving in the right direction. The remaining 20% to target is high-probability, low-risk.

This creates an asymmetric payoff:
- **Downside**: capped at 1–2% (tight stop)
- **Upside**: scales from 3% to 15% depending on progress

The implication? **You should be more aggressive when progress is high, not less.** Most traders do the opposite — they get scared when profits are large and exit too early. The data says: let progress_pct guide your conviction.

---

## Finding #4: Drawdown Stays Controlled in the Public Summary

| Metric | Value |
|--------|-------|
| Max drawdown | 3–4% |
| Average stop loss | 1–2% |
| Worst single trade | -4.1% |
| Recovery time (avg) | 2–3 signals |

A 3–4% max drawdown with 1–2% average stop loss is one of the strongest points in the public performance summary.

The reason is structural: **tight stops + partial exits = controlled risk.** When a signal is already advanced and you take a partial, a later reversal affects a smaller remaining position.

```
Signal at 66% progress, 30% partial taken:
- Partial profit: +2.6% on 30% of position = +0.78%
- Stop hit on remaining 70%: -2% × 0.7 = -1.4%
- Net worst case: -0.62%

vs. No partial, full stop:
- Stop hit on 100%: -2%
- Net worst case: -2%
```

The lifecycle approach turns a -2% worst case into a -0.62% worst case. Across hundreds of trades, this difference compounds massively.

---

## Finding #5: Early Progress Is a Different Risk Zone

Not all progress ranges are equal. The public rulebook is cautious in the earliest range:

| Progress | Behavior | Risk |
|----------|----------|------|
| 0–15% | Signal just generated | High — no confirmation yet |
| 15–33% | Early movement | Medium — could be noise |
| **33%+** | Signal confirmed | Lower — momentum established |

The `RULES.yaml` does not activate most partial-exit logic below 33%. That suggests the early stage is treated as a confirmation zone rather than an action-heavy zone.

This is counterintuitive. Most traders feel the urge to "do something" when a trade is new. The public lifecycle framing suggests patience early and more active management later.

---

## Why This Matters

The article does not need a synthetic comparison table to make the point. The published summary already shows the important thing:

- Progress changes the risk profile of a signal
- Regime changes the operating environment
- Partial exits and tight stops appear to keep drawdown controlled
- A deterministic rulebook can express that logic clearly

---

## What I Got Wrong

Transparency requires admitting what surprised me:

1. **I expected trend markets to dominate.** They do have better absolute returns, but the edge over range-bound was smaller than expected. The lifecycle approach adapts naturally to ranges.

2. **I underestimated the 80%+ zone.** I assumed signals near target were "almost done" and low value. In reality, the 80–95% zone is where the highest risk-adjusted profits live.

3. **I overestimated the value of complexity.** The more useful insight was not "more rules win," but "clearer lifecycle policies are easier to trust and operate."

---

## Live Performance Note

These are the numbers currently reflected in the public docs.

There may be stronger internal observations, but the right public standard is simple: publish what readers can inspect today, and label anything else as unpublished.

When the data is ready for public release, it will appear in the [signal-performance docs](https://github.com/gigshow/decker-ai-strategy-builder/blob/main/docs/signal-performance.md).

---

## Reproduce It Yourself

You can inspect the current public materials directly:

```bash
# Check any signal's current progress
curl -s "https://api.decker-ai.com/api/v1/signals/BTCUSDT/state"

# See what the rulebook recommends
curl -s "https://api.decker-ai.com/api/v1/signals/BTCUSDT/strategy?timeframe=4h&risk_appetite=medium"

# Browse active signals
curl -s "https://api.decker-ai.com/api/v1/judgment/signals/public?symbol=BTCUSDT"

# Coverage map — what's being tracked
curl -s "https://api.decker-ai.com/api/v1/judgment/coverage"
```

The `RULES.yaml` is open source and the API surface is public. Track a signal from birth to completion and compare the experience against the published lifecycle thesis yourself.

---

## Coming Up Next

- **#7** — State Machines in Trading: Why I Prefer Deterministic Execution Layers
- **#8** — From Side Project to Signal Engine: How We Built Decker AI with $0 in LLM Costs

Full data and methodology:
- **GitHub**: [decker-ai-strategy-builder](https://github.com/gigshow/decker-ai-strategy-builder)
- **Performance docs**: [signal-performance.md](https://github.com/gigshow/decker-ai-strategy-builder/blob/main/docs/signal-performance.md)
- **Risk management**: [risk-management.md](https://github.com/gigshow/decker-ai-strategy-builder/blob/main/docs/risk-management.md)
- **Telegram**: [@deckerclawbot](https://t.me/deckerclawbot)

---

*The most useful idea in the public performance docs is not a hidden feature. It's a visible percentage that tells you how far the signal has already traveled.*

---

**Tags**: `Backtesting`, `AI Trading`, `Algorithmic Trading`, `Cryptocurrency`, `Data Analysis`, `Trading Strategy`, `Risk Management`, `Bitcoin`, `Quantitative Trading`, `Fintech`
