# I Built a Trading Signal API in 5 Minutes — With Zero Machine Learning

*No TensorFlow. No training data. No GPU. Just 3 API calls and a small Python loop.*

---

## The Fastest Way to a Working Signal System

Most "build your own trading bot" tutorials start like this:

1. Install TensorFlow / PyTorch
2. Download 5 years of historical data
3. Preprocess, normalize, feature-engineer
4. Train an LSTM / transformer model
5. Evaluate, tune hyperparameters
6. Deploy model server
7. Build API around it
8. Handle inference latency
9. Schedule retraining

For many developers, that turns into a multi-week project before the first useful output.

Here's what I'm going to show you: **a working signal workflow in 3 API calls and a few minutes.**

No ML. No training. No infrastructure. Just a REST API that already knows the market state.

---

## Step 1: Push a Signal (30 seconds)

You have a trade idea. BTC long, entry at $96,000, target $100,000, stop at $92,000.

Push it to Decker AI:

```bash
curl -s -X POST "https://api.decker-ai.com/api/v1/signals/push" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTCUSDT",
    "timeframe": "4h",
    "direction": "long",
    "entry_price": 96000,
    "target_price": 100000,
    "stop_loss": 92000
  }'
```

That's it. Your signal is now in the system. No authentication required.

The public docs are crypto-first, and the examples in this article use crypto symbols such as `BTCUSDT` and `ETHUSDT`.

---

## Step 2: Check the State (30 seconds)

Now ask: **where is this signal in its lifecycle?**

```bash
curl -s "https://api.decker-ai.com/api/v1/signals/BTCUSDT/state"
```

Response:

```json
{
  "symbol": "BTCUSDT",
  "signals": [
    {
      "state": {
        "progress_pct": 66.0,
        "status": "in_progress",
        "risk_reward_ratio": 2.0,
        "market_state": "range"
      }
    }
  ]
}
```

You now know:
- **progress_pct: 66%** — two-thirds of the way to target
- **status: in_progress** — still active
- **risk_reward_ratio: 2.0** — $2 potential gain for every $1 risk
- **market_state: range** — the public docs also expose the market regime when available

No model predicted this. It was *calculated* from the prices you provided. Deterministic, reproducible, instant.

---

## Step 3: Get the Strategy (30 seconds)

Ask the operation rulebook what to do at this progress level:

```bash
curl -s "https://api.decker-ai.com/api/v1/signals/BTCUSDT/strategy?timeframe=4h&risk_appetite=medium"
```

Response:

```json
{
  "symbol": "BTCUSDT",
  "timeframe": "4h",
  "strategy": "4h timeframe, 66%. Take 40% partial profit. Hold rest to target."
}
```

The exact text comes from the rulebook — timeframe-specific rules (e.g. 4h vs 1h) return different partial percentages.

**In a short setup flow**, you went from a trade idea to a strategy recommendation with progress tracking and risk metrics.

---

## Now Build a Bot: 40 Lines of Python

Let's turn those 3 calls into an automated strategy bot:

```python
import requests
import time

API = "https://api.decker-ai.com/api/v1"

WATCHLIST = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"]

def get_state(symbol):
    r = requests.get(f"{API}/signals/{symbol}/state", timeout=10)
    r.raise_for_status()
    return r.json()

def get_strategy(symbol, tf="4h", risk="medium"):
    r = requests.get(f"{API}/signals/{symbol}/strategy",
                     params={"timeframe": tf, "risk_appetite": risk}, 
                     timeout=10)
    r.raise_for_status()
    return r.json()

def scan():
    print(f"\n{'='*60}")
    print(f"Decker AI Signal Scanner — {time.strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")
    
    for symbol in WATCHLIST:
        try:
            state = get_state(symbol)
            strat = get_strategy(symbol)
            
            signals = state.get("signals", [])
            if not signals:
                print(f"  {symbol}: No active signal")
                continue
            
            s = signals[0].get("state", {})
            progress = s.get("progress_pct", 0)
            status = s.get("status", "unknown")
            rr = s.get("risk_reward_ratio", 0)
            action = strat.get("strategy", "Hold")
            
            emoji = "🟢" if progress > 60 else "🟡" if progress > 30 else "⚪"
            print(f"  {emoji} {symbol}")
            print(f"     Progress: {progress:.1f}% | Status: {status} | R:R {rr:.1f}")
            print(f"     → {action}\n")
            
        except Exception as e:
            print(f"  ❌ {symbol}: {e}\n")

if __name__ == "__main__":
    scan()
```

Run it:

```bash
pip install requests
python scanner.py
```

Output:

```
============================================================
Decker AI Signal Scanner — 2025-03-17 14:30
============================================================

  🟢 BTCUSDT
     Progress: 66.0% | Status: in_progress | R:R 2.0
     → 4h timeframe, 66%. Take 40% partial profit.

  🟡 ETHUSDT
     Progress: 42.0% | Status: in_progress | R:R 1.8
     → 50% progress. Hold. Risk-dependent.

  🟢 SOLUSDT
     Progress: 81.0% | Status: in_progress | R:R 3.2
     → 80%+ progress. Take 50% partial. Hold to target.

  ⚪ BNBUSDT: No active signal
```

**40 lines.** A multi-asset signal scanner with progress tracking, risk metrics, and strategy recommendations. No ML degree. No GPU. No training pipeline.

---

## Add Alerts: Telegram Notification (10 more lines)

Want alerts when a signal hits a critical level?

```python
import requests

TELEGRAM_TOKEN = "your_bot_token"
CHAT_ID = "your_chat_id"

def alert(message):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": message}
    )

# Inside your scan loop:
if progress > 80:
    alert(f"🔥 {symbol} at {progress:.0f}%! → {action}")
```

Or skip building your own bot entirely — just talk to [@deckerclawbot](https://t.me/deckerclawbot) on Telegram. Say "BTC signal" and get the same data conversationally.

---

## The Full Endpoint Map

Here's everything you can do, all without authentication:

| Endpoint | What It Does |
|----------|-------------|
| `POST /signals/push` | Register your own signal |
| `GET /signals/{symbol}/state` | progress_pct, status, R:R |
| `GET /signals/{symbol}/strategy` | Rule-based strategy for current state |
| `GET /judgment/signals/public` | Browse existing signals |
| `GET /judgment/coverage` | 20 symbols × 6 timeframes coverage map |
| `GET /market/prices` | Real-time prices |
| `GET /judgment/compare` | Compare multiple assets side by side |
| `GET /judgment/market-status` | Liquidations, funding rates |
| `GET /system/health` | API health check |

Interactive docs: [api.decker-ai.com/docs](https://api.decker-ai.com/docs)

---

## What You Can Build With This

People have used these endpoints to build:

- **Portfolio dashboards** — track progress_pct across all positions
- **Alert systems** — notify when signals cross 80% or hit stop
- **Telegram bots** — relay strategies to group chats
- **Backtesting scripts** — replay signals and evaluate rule performance
- **Multi-timeframe scanners** — compare 1h vs 4h vs 1d signals
- **Risk monitors** — flag positions where R:R drops below 1.5

The API is the building block. What you build on top is up to you.

---

## Why I Made It Free

The read endpoints are free because **adoption beats monetization at this stage**. The more developers building on Decker AI's API, the stronger the ecosystem.

The revenue model is clear:
- **Free**: 5 symbols, basic rules, 500 calls/month
- **Pro** ($29/mo): 20 symbols, standard rules, real-time alerts
- **Trader** ($99/mo): Unlimited, premium rules, auto-execution
- **API** ($299/mo): Full API access, webhooks, custom integrations

But right now? Right now it's free. Go build something.

---

## Recap: What We Built in 5 Minutes

| Step | Time | What |
|------|------|------|
| 1 | 30s | Pushed a signal via `POST /signals/push` |
| 2 | 30s | Checked state via `GET /signals/{symbol}/state` |
| 3 | 30s | Got strategy via `GET /signals/{symbol}/strategy` |
| 4 | 3min | Built a 40-line multi-asset scanner |
| 5 | 1min | Added Telegram alerts |

**Total: a few minutes.** From zero to a working signal workflow with progress tracking, risk metrics, strategy recommendations, and push notifications.

The main point is not "APIs beat ML in every case." It's that you can prototype the execution layer very quickly when the state computation and rulebook already exist.

---

## Coming Up Next

- **#6** — What the Public Backtest Summary Suggests About `progress_pct`
- **#7** — State Machines in Trading: Why Deterministic Beats Probabilistic

All code from this article:
- **GitHub**: [decker-ai-strategy-builder/samples](https://github.com/gigshow/decker-ai-strategy-builder/tree/main/samples)
- **Telegram**: [@deckerclawbot](https://t.me/deckerclawbot)
- **API**: [api.decker-ai.com/docs](https://api.decker-ai.com/docs)
- **Web**: [decker-ai.com](https://decker-ai.com)

---

*The best API is one you can use before you finish reading the docs.*

---

**Tags**: `API`, `Python`, `Trading Bot`, `AI Trading`, `Cryptocurrency`, `REST API`, `Tutorial`, `Algorithmic Trading`, `Bitcoin`, `Fintech`
