# Signal LLM 개념

---

## State Engine, not LLM

DECKER는 LLM이 가격을 예측하는 서비스가 아닙니다.

시계열 데이터에서 시장 구조(Object, Swing)를 분석하고, **진행도(progress_pct)**와 **상태(status)**를 결정론적으로 계산하는 엔진입니다.

```
DECKER does not use traditional ML prediction for signals.

Instead it uses:
  • Price (진입가·목표가·손절가·현재가)
  • Time (시간프레임)
  • Market structure (시그널 → 진행도 → 상태)

to build a deterministic market state engine.

The LLM layer is used to interpret
market state signals into actionable strategies.
```

---

## AI 트레이딩 vs DECKER

| 구분 | 일반 AI 트레이딩 | DECKER |
|------|------------------|--------|
| **시그널 생성** | LLM/ML 가격 예측 | **시장 상태 엔진** |
| **LLM 역할** | 예측·판단 | **인터페이스·설명** |
| **핵심 출력** | "매수/매도" | progress_pct, status, 전략 |
| **토큰 비용** | 시그널마다 LLM 호출 | **룰북 경로 $0** |

---

## 왜 다른가

대부분의 AI 트레이딩 서비스는 다음 중 하나입니다.

- **Sentiment AI**: 뉴스·SNS 감성 분석 → 매매 신호
- **Prediction AI**: LLM/ML이 가격 방향 예측 → 매매 신호

DECKER는 **시장 구조 엔진 + LLM 인터페이스**입니다.

1. 시계열 데이터를 오브젝트로 평가하여 라벨 부착 ([라벨링 알고리즘](labeling_algorithm.md))
2. 시그널(진입·목표·손절) + 현재가 → 진행도(progress_pct), 상태(status) 계산
3. 오퍼레이션 룰북(RULES.yaml)으로 전략 매칭 — **LLM 미사용**
4. LLM은 결과를 자연어로 설명하거나 사용자 질문에 답변

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

## LLM 통합 패턴

LLM은 코어 엔진 외부에서 **UX/설명** 용도로만 사용합니다.

- 시그널 발생 시 결과 해석을 자연어로 전달
- 사용자 질문("이 시그널 어떻게 할까?")에 답변
- 코어 연산(라벨링 → 상태 계산 → 시그널)은 결정론적 로직

---

## 참고

- [시장 상태 이론](market_state_theory.md) — 진행도(progress_pct) 개념
- [라벨링 알고리즘](labeling_algorithm.md) — 시계열 → 오브젝트 평가
- [Architecture](../docs/architecture.md) — 파이프라인·모듈
