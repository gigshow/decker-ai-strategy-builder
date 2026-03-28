# Signal → State → Strategy Example

*A complete walkthrough: from signal input through structural state evaluation to operation gate and strategy output.*

---

## 1. Signal Input

A signal is pushed to the engine with entry, target, and stop-loss levels:

```json
{
  "symbol": "BTCUSDT",
  "timeframe": "4h",
  "direction": "long",
  "entry_price": 96000,
  "target_price": 100000,
  "stop_loss": 92000
}
```

---

## 2. Signal state on the API (`GET /api/v1/signals/{symbol}/state`)

Production `signals[].state` is built from **`build_signal_state`** (progress layer) plus optional DB enrich **`engine_trace_id`**, **`engine_sub_swing_id`**, **`engine_connector_swing_id`** when stored on `judgment_signals`. It does **not** always include sequence labels, `operation_gate`, or `label_quality` — those appear when the engine evaluate path is **merged** into `signal_state` (consultation / internal merge; see monorepo `SIGNAL_STATE_ENGINE_MERGE.md`). Merged payloads may expose gate info under **`operation_context.action_gate`** as well as branded **`operation_gate`** in some serializers — cross-check [api-guide](../docs/api-guide.md).

**Typical `state` object (price + signal leg known):**

```json
{
  "symbol": "BTCUSDT",
  "direction": "long",
  "signal_at": 96000,
  "target": 100000,
  "stop_loss": 92000,
  "current": 98400,
  "progress_pct": 60.0,
  "remaining_pct": 40.0,
  "to_target_pct": 1.6,
  "status": "in_progress",
  "state_quality": "full",
  "risk_reward_ratio": 2.0,
  "engine_trace_id": "01HQ…",
  "engine_sub_swing_id": 1
}
```

**Illustrative composite (engine + gate narrative — not guaranteed on raw `/state`):**

```json
{
  "engine_c_state": "B_SET",
  "operation_gate": "GO",
  "label_quality": {
    "confidence": 0.88,
    "stability": 0.84,
    "regime_consistency": 0.91
  }
}
```

**Reading the typical block:**
- `progress_pct` / `status` — Signal lifecycle vs current price (same formulas as [Architecture § State Engine](../docs/architecture.md)).
- `state_quality` — `full` | `partial` | `unknown` (whether the entry→target leg is well-defined).
- `engine_*` keys — Present when the row has been linked to an engine run; absent does not mean “no sequence engine,” only that this response slice is progress-first.

---

## 3. Progress Calculation

With the signal live and current price at **98,400**:

```
progress_pct = (98,400 − 96,000) / (100,000 − 96,000) × 100 = 60%
```

| progress_pct | Status | Meaning |
|---|---|---|
| 0–32% | Early | Wait or prepare |
| **33–66%** | **Active** | **Entry window, risk management begins** |
| 67–89% | Late | Partial take-profit |
| 90–100% | At target | Prepare exit |

At 60% progress, we're in the active phase — the move has proven itself but hasn't exhausted its potential.

---

## 4. RULES Engine Match

The RULES engine evaluates 9 layers and matches the first applicable rule:

```
Matched rule: progress_66
Tier:         standard
Condition:    progress_min: 60, progress_max: 79

Strategy: "66% progress. 30% partial take-profit or hold. 
           Risk management: tighten stop-loss."

Choices:
  ① 30% partial take-profit
  ② Hold to target
  ③ Full exit
```

---

## 5. AI Consultation Output

The consultation service translates the structural state into natural language:

```
📍 BTCUSDT  4h
Gate: GO
Progress: 60%
Sub-swing: 1 (counter-narrative first attempt — manageable)
Confidence: 88%

[Strategy] B-leg confirmed. Signal at 60% progress. 
Counter-narrative is at its first structural attempt, not yet threatening.
Recommended: consider 30% partial TP to lock gains, 
hold remainder to target with stop tightened to entry.

[Your options]
  ① 30% partial take-profit (lock 60% of expected gain)
  ② Hold to target (full position, tighter stop)
  ③ Full exit (crystallize current profit)
```

---

## 6. API Call

```bash
# Get the current state for a signal
curl "https://api.decker-ai.com/api/v1/signals/BTCUSDT/state"

# Get the full strategy (state + RULES match + choices)
curl "https://api.decker-ai.com/api/v1/signals/BTCUSDT/strategy"
```

Or ask [@deckerclawbot](https://t.me/deckerclawbot): *"What should I do with my BTCUSDT signal?"*

---

## Understanding the States

| State | Structural Situation | Gate (typical) |
|-------|---------------------|----------------|
| `INIT` | No anchor yet | WATCH |
| `C_SET` | Anchor established | WATCH |
| `B_FORMING` | Test in progress | WATCH |
| `B_SET` | Test confirmed, resolution pending | GO |
| `A_FORMING` | Signal / outcome handling (after `B_SET`) | WATCH / varies |
| `W_PENDING` | Bilateral break, direction unclear | HOLD |

*Gates are product-facing summaries; runtime keys may use `operation_context.action_gate` when merged.*

---

## References

- [Sequence Engine concept](../concept/sequence_engine.md)
- [System flow diagrams](../diagrams/system_flow.md)
- [RULES.yaml](../operation_rules/RULES.yaml)
- [API Guide](../docs/api-guide.md)
- [Article #13: GO, WATCH, or HOLD](../docs/medium/part2/13_go_watch_hold.md)

---

*한국어 설명: 시그널 데이터(진입가·목표가·손절가)와 현재가를 기반으로 progress_pct를 계산하고, 오퍼레이션 룰북(RULES.yaml)으로 전략을 매칭합니다. `이 시그널 지금 어떻게 할까?` 라고 @deckerclawbot에 물어보면 자연어로 설명해줍니다.*
