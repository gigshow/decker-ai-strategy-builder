# From Side Project to Signal Engine: I Built a Trading Platform That Costs $0 in LLM Tokens

*Everyone's building AI wrappers around GPT. I ended up building a trading engine where the AI is optional and the core decision path is rule-based.*

---

## The Origin: A Telegram Message

It started with a Telegram message I sent to myself:

> "BTC signal just hit 66%. Should I take partial profit or hold?"

I was asking myself this question five times a day. Different symbols. Different timeframes. Different signals. Always the same question: **how far along is this signal, and what should I do now?**

I kept a spreadsheet. Entry price, target, stop, current price. I'd manually calculate the percentage and look up my own notes on what to do at each stage.

Then the obvious thought: **this is just math and a lookup table. Why am I doing it manually?**

I wrote the first version of what would become Decker AI: a tiny Python script that took entry, target, stop, and current price and returned a percentage plus a strategy recommendation. No database. No API. No LLM.

It worked immediately. Not because the code was clever, but because the problem was always simple — I just hadn't formalized it.

---

## Phase 1: The Script That Became a Service

The 47-line script had one function:

```python
def get_strategy(entry, target, stop, current, direction="long"):
    if direction == "long":
        progress = (current - entry) / (target - entry) * 100
    else:
        progress = (entry - current) / (entry - target) * 100
    
    if progress >= 90:
        return f"{progress:.0f}% — Take 70-80% profit. Almost there."
    elif progress >= 66:
        return f"{progress:.0f}% — Take 30% partial. Hold rest to target."
    elif progress >= 50:
        return f"{progress:.0f}% — Consider 20% partial or hold."
    else:
        return f"{progress:.0f}% — Hold to target."
```

I used this for a month. Every day. It was faster than my spreadsheet and never made an arithmetic error.

Then my trading partner asked: "Can I use that too?"

That's when it became a Telegram bot.

---

## Phase 2: The Telegram Bot

I wrapped the function in a Telegram bot. Send it a message like "BTC 96000 100000 92000" and it'd reply with the progress and strategy.

Within a week, I had 3 people using it. Within a month, 12. They weren't using it because it was smart. They were using it because **it answered the question they actually had**: "What should I do with this position right now?"

Not "what should I buy." Not "is the market going up." Just: **given where I am, what's the move?**

This is when I realized the product wasn't a trading bot. It was a **decision engine for traders who already have positions**.

---

## Phase 3: The LLM Question

Around that time, everyone was building LLM wrappers. "AI trading advisor." "GPT-powered portfolio manager." The pressure to add an LLM was real.

So I added one. Users could ask "What should I do with my BTC position?" in natural language, and Claude would interpret the question, call the state engine, and explain the result conversationally.

It worked great for UX. But it raised an uncomfortable question: **how much of this LLM call is actually necessary?**

Conceptually, the split looked like this:

| Path | What It Does | LLM Tokens | Cost |
|------|-------------|-----------|------|
| **Rule path** | progress_pct → YAML lookup → strategy | 0 | $0 |
| **LLM path** | Same + natural language explanation | variable | non-zero |

The rule path gave the same strategy recommendation for $0 on the core path. The LLM path added a better user experience, but also added cost.

So I made the architecture decision that defines Decker AI: **the core path is LLM-free. The LLM is an optional UX layer.**

```
Core path:          State Engine → RULES.yaml → Strategy
LLM path:           Core path + LLM explanation
```

This means:
- API users get strategies on a rule-based core path
- Telegram users get natural language as an optional UX layer
- The business can scale without LLM costs scaling linearly

---

## Phase 4: The Rulebook

The hardcoded if-else chain was fine for 4 rules. But traders wanted nuance:

- "What about different timeframes?"
- "What if I'm aggressive vs. conservative?"
- "What about market regime — trending vs. ranging?"

I needed a configurable strategy system. The options:

| Approach | Pros | Cons |
|----------|------|------|
| More if-else | Simple | Unmaintainable at 20+ rules |
| ML model | Adaptive | Expensive, opaque, requires retraining |
| DSL / YAML | Readable, auditable, cheap | Requires manual rule design |

I chose YAML. A public rulebook. Each rule is a condition-action pair that a trader or developer can read and modify:

```yaml
- id: progress_80_trend
  progress_min: 80
  market_state: [trend]
  strategy: "Trending, 80%+. Take 50%. Hold rest."
```

The rulebook went through three versions. v1.0 had 8 rules. v1.3 added timeframe-specific rules. v1.4 added market_state conditions. Each version was a few lines of YAML, deployed in seconds.

The important part was not development speed as a bragging point. It was that the strategy layer stayed editable and inspectable as it grew.

---

## Phase 5: The Open Repo

I eventually published the architecture, docs, samples, and rulebook as an open repository: [decker-ai-strategy-builder](https://github.com/gigshow/decker-ai-strategy-builder).

Not the production code — that stays private. But everything a developer needs to understand, integrate, and build on the system:

| What's Public | Why |
|--------------|-----|
| Architecture docs | So developers understand the pipeline |
| RULES.yaml (public rulebook) | So anyone can read and fork the strategy |
| API guide | So developers can integrate |
| Python/curl samples | So developers can start in 5 minutes |
| Concept docs | So the theory is transparent |
| CHANGELOG, CONTRIBUTING | So the project looks alive |
| Signal performance | So the numbers are public |

The repo went from 0 to getting stars within days. Not because the code is revolutionary — but because the **problem framing** resonated. "State Engine, not LLM" is a message that developers understood immediately.

---

## The Cost Structure That Changed Everything

I am intentionally keeping the public story simple here:

- The core state and strategy path does not require LLM tokens
- Optional explanation layers do add cost
- Separating those two paths makes the system easier to operate and easier to price

That architectural split mattered more than any exact monthly bill.

---

## What I'd Do Differently

Building in public means sharing mistakes:

**1. I should have open-sourced earlier.** I waited until the docs were "ready." They were never going to be ready. Publishing imperfect docs generated more feedback than perfecting them in private ever would.

**2. I overcomplicated the first rulebook.** The deeper lesson was that simplicity beats sophistication in strategy execution.

**3. I underestimated the Telegram channel.** Most early users came through Telegram, not the API. If you're building a trading tool, meet users where they already are — and traders live in Telegram.

**4. I should have published performance data from day one.** Waiting to have "perfect" data meant months of "is this thing real?" skepticism. Publishing conservative backtest numbers early would have built trust faster.

---

## The Roadmap: What's Next

| Status | What | Why |
|--------|------|-----|
| ✅ | Telegram bot | Natural language trading assistant |
| ✅ | OpenClaw skill (Slack, Discord) | Team workflow, OpenClaw ecosystem. Slack 제한 시 Telegram 우선 |
| ✅ | Order execution (Binance, HL) | One-command trades |
| ✅ | RULES.yaml v1.4 | Market state awareness |
| ✅ | Public API | Developer ecosystem |
| 🔜 | Progress-based backtest reports | Stronger public performance transparency |
| 🔜 | Strategy marketplace | Community-submitted YAML rules |
| 🔜 | Multi-asset expansion | Broader asset support over time |
| 🔜 | Signal model (DPDP v2) | AI-generated signals from market structure |

The vision: **a platform where signals come from algorithms, lifecycle management is deterministic, strategies are community-driven, and the LLM just makes it all conversational.**

---

## The Numbers So Far

| Metric | Value |
|--------|-------|
| GitHub stars | Growing |
| Signals processed | Internal scale has grown over time |
| Backtest win rate | 55–75% (range to trend) |
| Monthly return (range) | 20–30% |
| Monthly return (trend) | 30–60%+ |
| Max drawdown | 3–4% |
| LLM cost for core path | $0 |
| Time to first API call | a few minutes |

These aren't "I woke up and made $10,000" numbers. They are conservative public-facing numbers from a system you can inspect, fork, and modify.

---

## If You've Read This Far

This series was 8 articles about a single idea: **trading signals have lifecycles, and managing that lifecycle deterministically beats predicting the next price.**

If it resonated:

- **Star the repo**: [github.com/gigshow/decker-ai-strategy-builder](https://github.com/gigshow/decker-ai-strategy-builder)
- **Try the bot**: [@deckerclawbot](https://t.me/deckerclawbot) on Telegram
- **Hit the API**: [api.decker-ai.com/docs](https://api.decker-ai.com/docs)
- **Read the docs**: Architecture, performance, risk management — all public
- **Fork RULES.yaml**: Add your own rules, submit a PR
- **Follow me on Medium**: More articles on deterministic trading, state machines, and building in public

---

## The Series Recap

| # | Title | Core Idea |
|---|-------|-----------|
| 1 | State Engine, Not LLM | Why we don't predict prices |
| 2 | Signal Lifecycle | What happens after entry matters more than entry |
| 3 | Target → Signal → Entry | Reverse the sequence everyone uses |
| 4 | YAML Rulebook | Encode lifecycle strategy in a readable config |
| 5 | Signal API in 5 Minutes | From zero to a working signal workflow quickly |
| 6 | Public Backtest Summary | What the published data suggests about `progress_pct` |
| 7 | State Machines vs ML | Why I prefer deterministic execution layers |
| **8** | **$0 LLM Cost Story** | **How it all came together** |

---

*I started with a spreadsheet and a question. I ended with an engine whose core path uses zero LLM tokens and treats execution as a state machine problem. The market didn't need another AI predictor for every step. It needed clearer lifecycle logic.*

---

**Tags**: `Startup`, `Building in Public`, `AI Trading`, `Algorithmic Trading`, `Cryptocurrency`, `State Machine`, `Open Source`, `Indie Hacker`, `Fintech`, `Python`
