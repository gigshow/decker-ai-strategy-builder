# Signal LLM — How Decker Uses (and Does Not Use) AI

*State Engine first. LLM as narrator — never as the source of structural truth.*

---

## English summary

Decker does **not** use an LLM to predict prices or to invent signals.

1. **Sequence labeling + state machine** turn candles into structural state (deterministic).
2. **RULES.yaml** matches that state to strategy text and ranked choices (**$0 tokens** on this path).
3. **LLM (optional)** turns the already-computed state + strategy into natural language for chat and consultation.

The LLM receives `progress_pct`, `status`, `operation_gate` (`GO` / `WATCH` / `HOLD`), matched rule output, and label-quality fields. It **explains**; it does **not** override the engine.

| Layer | Role |
|-------|------|
| Engine | Structural state, gate, traceable output |
| RULES | Policy: which strategy and choices apply |
| LLM | Translation and UX only |

Deep dive: [Sequence Engine](sequence_engine.md) · [Article #14 — AI explains, engine decides](../docs/medium/part2/14_ai_explains_engine_decides.md)

---

## State Engine, not LLM

DECKER는 LLM이 가격을 예측하는 서비스가 아닙니다.

시계열 데이터에서 **시퀀스 라벨링·상태 머신**으로 시장 구조를 분석하고, **진행도(progress_pct)**와 **상태(status)**, **운영 게이트(GO/WATCH/HOLD)**를 결정론적으로 계산합니다. (구체 흐름: [Sequence Engine](sequence_engine.md))

```
DECKER does not use traditional ML prediction for signals.

Instead it uses:
  • Price (진입가·목표가·손절가·현재가)
  • Time (시간프레임)
  • Market structure (시퀀스 라벨 → 상태 머신 → 게이트 → 룰북 매칭)

to build a deterministic market state engine.

The LLM layer (when used) interprets
the engine output into natural language — not into new trading decisions.
```

---

## AI 트레이딩 vs DECKER

| 구분 | 일반 AI 트레이딩 | DECKER |
|------|------------------|--------|
| **시그널 생성** | LLM/ML 가격 예측 | **시장 상태 엔진** (시퀀스·FSM) |
| **LLM 역할** | 예측·판단 | **인터페이스·설명** |
| **핵심 출력** | "매수/매도" | progress_pct, status, **operation_gate**, 전략·choices |
| **토큰 비용** | 시그널마다 LLM 호출 | **룰북 경로 $0** |

---

## 왜 다른가

대부분의 AI 트레이딩 서비스는 다음 중 하나입니다.

- **Sentiment AI**: 뉴스·SNS 감성 분석 → 매매 신호
- **Prediction AI**: LLM/ML이 가격 방향 예측 → 매매 신호

DECKER는 **시장 구조 엔진 + (선택) LLM 인터페이스**입니다.

1. 시계열을 **시퀀스 라벨**로 읽고 상태 머신을 전이 ([라벨링 알고리즘](labeling_algorithm.md), [Sequence Engine](sequence_engine.md))
2. 시그널(진입·목표·손절) + 현재가 → progress_pct, status 계산
3. 오퍼레이션 룰북(RULES.yaml)으로 전략 매칭 — **LLM 미사용**
4. LLM은 결과를 자연어로 설명하거나 사용자 질문에 답변 — **엔진 출력을 덮어쓰지 않음**

---

## 핵심 철학: Target → Signal → Entry

대부분의 전략: `signal → entry → target`

DECKER: **`target → signal → entry`**

| 원칙 | 설명 |
|------|------|
| Entry without target → invalid | 목표 없는 진입은 유효하지 않음 |
| Movement without signal → ignored | 시그널 없는 움직임은 무시 |
| Market clears liquidity | 시장은 유동성 청산 방향으로 이동 |

이 구조에서 모든 움직임은 **profit opportunity** 또는 **reverse opportunity**가 됩니다.

---

## LLM 통합 패턴 (Phase 4)

LLM은 코어 엔진 **바깥**에서 **UX/설명** 용도로만 사용합니다.

- 시그널·상의 시: 이미 계산된 `state`, `operation_gate`, RULES 매칭 결과를 자연어로 전달
- 사용자 질문("이 시그널 어떻게 할까?")에 답변할 때도 **동일한 구조적 입력**을 전제로 함
- 코어 연산(라벨링 → 상태 머신 → 게이트 → 룰북)은 전부 결정론적 로직

---

## 참고

- [Sequence Engine](sequence_engine.md) — 시퀀스 엔진 전체 개념 (영문)
- [시장 상태 이론](market_state_theory.md) — progress_pct
- [라벨링 알고리즘](labeling_algorithm.md) — 시퀀스 라벨링
- [Architecture](../docs/architecture.md) — 파이프라인·Phase 4 절
- [Article series Part 2](../docs/medium/part2/README.md) — GO/WATCH/HOLD, AI 경계
