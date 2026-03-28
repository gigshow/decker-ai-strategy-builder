# Strategy prompt example — consultation flow

*How chat turns engine output into natural language. Structural fields come from the API; the LLM does not invent them.*

---

## "이 시그널 지금 어떻게 할까?"

Telegram·웹(또는 OpenClaw 스킬)에서 사용자가 이렇게 물으면, DECKER는 다음 흐름으로 응답합니다.

1. 사용자 컨텍스트(종목, 포지션, 리스크 선호) 수집
2. `/signals/{symbol}/state` → `progress_pct`, `status`, **structural state** (시퀀스·FSM·`operation_gate` 등, 스키마는 [api-guide](../docs/api-guide.md) 기준)
3. `/signals/{symbol}/strategy` → 오퍼레이션 룰북 매칭 결과 (`rationale`, `choices` 등)
4. LLM(선택): 위 구조를 자연어로 다듬어 전달 — **엔진 수치·게이트·첫 매칭 룰을 바꾸지 않음**

---

## 예시 프롬프트

### 사용자

- "비트코인 시그널 알려줘"
- "이 시그널 지금 어떻게 할까?"
- "ETH 4시간봉 66% 됐는데 익절할까?"

### 시스템 입력 (LLM에 전달되는 컨텍스트 — Phase 4 스타일)

```
[State]
symbol: BTCUSDT
timeframe: 4h
direction: long
progress_pct: 66
status: in_progress
operation_gate: GO
structural_state: B_SET
label_quality:
  confidence: 0.82
  stability: stable
  regime_consistency: aligned

entry_price: 96000
target_price: 100000
current_price: 98640

[Strategy] (RULES.yaml first-match)
rationale: "4h progress 66%; partial take-profit band per rule X."
choices:
  - rank: 1
    label: "30% partial TP, hold remainder to target"
    score: 0.91
```

### 예시 응답

"BTC 4시간봉이 목표까지 66% 진행 중이고, 운영 게이트는 GO입니다. 룰북에 따라 30% 부분 익절을 우선 제안하고, 나머지는 목표가(100,000)까지 홀드하는 선택지가 1순위로 매칭되었습니다."

---

## Target → Signal → Entry 적용

이 응답의 기반은 **Target → Signal → Entry** 철학입니다:

| 단계 | 이 예시에서 |
|------|------------|
| Target | 100,000 (목표 구조 사전 정의) |
| Signal | 시퀀스·상태 머신이 확인한 진입 구간 + 진입가 |
| Entry | 96,000 (기대값·손절이 정의된 상태에서 진입) |

목표 구조가 먼저 정의되었기 때문에, 66% 진행 시점에서 **정량적 익절 판단**이 가능합니다.

---

## 룰북 경로 vs LLM 경로

| 경로 | 토큰 비용 | 용도 |
|------|-----------|------|
| **룰북** | $0 | progress_pct, status, 게이트, tf_alignment 등 기반 전략 매칭 |
| **LLM** | 유료 | 결과 자연어 설명, 사용자 질문 답변 (구조적 입력 유지) |

---

## 참고

- [Quick Start](../docs/quickstart.md)
- [Signal LLM 개념](../concept/signal_llm_concept.md)
- [Sequence Engine](../concept/sequence_engine.md)
- [시그널 예시](signal_example.md)
- [Strategy DSL](../docs/strategy-dsl.md)
