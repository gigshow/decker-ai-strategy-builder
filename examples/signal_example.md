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

## 2. Structural State Evaluation

The engine evaluates the candle sequence around the signal and returns:

```json
{
  "state": "B_SET",
  "last_event": "b_leg_confirmed",
  "direction": "+",
  "sub_swing_count": 1,
  "in_connector_phase": false,
  "operation_gate": "GO",
  "label_quality": {
    "confidence": 0.88,
    "stability": 0.84,
    "regime_consistency": 0.91
  }
}
```

**Reading this output:**
- `state: "B_SET"` — The B-leg (test swing) is structurally confirmed. Resolution is pending.
- `last_event: "b_leg_confirmed"` — The test phase just completed.
- `sub_swing_count: 1` — Counter-narrative is at its first attempt. Manageable risk.
- `operation_gate: "GO"` — Structural conditions are met. Evaluate entry.

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

| State | Structural Situation | Gate |
|-------|---------------------|------|
| `INIT` | No anchor yet | WATCH |
| `C_SET` | Anchor established | WATCH |
| `B_FORMING` | Test in progress | WATCH |
| `B_SET` | Test confirmed, resolution pending | GO |
| `W_PENDING` | Bilateral break, direction unclear | HOLD |

---

## References

- [Sequence Engine concept](../concept/sequence_engine.md)
- [System flow diagrams](../diagrams/system_flow.md)
- [RULES.yaml](../operation_rules/RULES.yaml)
- [API Guide](../docs/api-guide.md)
- [Article #13: GO, WATCH, or HOLD](../docs/medium/part2/13_go_watch_hold.md)

---

*한국어 설명: 시그널 데이터(진입가·목표가·손절가)와 현재가를 기반으로 progress_pct를 계산하고, 오퍼레이션 룰북(RULES.yaml)으로 전략을 매칭합니다. `이 시그널 지금 어떻게 할까?` 라고 @deckerclawbot에 물어보면 자연어로 설명해줍니다.*
