# Decker 모델: 알고리즘과 성과

**대상**: 심층 고객 — 알고리즘의 탄생, 구조, 차별점, 성과를 알고 싶은 분

---

## 1. 핵심 철학

### Target → Signal → Entry

대부분의 전략은 `signal → entry` 순서입니다. 시그널이 발생하면 진입하고, 이후에 목표를 설정합니다.

DECKER는 **`target → signal → entry`** 순서입니다.

1. **Target first** — 목표 구조가 먼저 확인됩니다.
2. **Signal confirmation second** — 시그널이 목표를 확인합니다.
3. **Entry last** — 기대값과 리스크가 정의된 상태에서 진입합니다.

이 구조에서 모든 거래에 **사전 정의된 기대값과 리스크 구조**가 존재합니다.

### 모든 움직임은 기회

- 목표가 없이 움직이면 → 반대로 찬스
- 물렸거나 수익이면 → 반대 청산 기회
- 시장은 항상 유동성을 청산하는 방향으로 이동

따라서 모든 움직임은 **profit opportunity** 또는 **reverse opportunity**가 됩니다.

---

## 2. 알고리즘 스토리

### 탄생 배경

시그널·진행도 기반 전략은 **"상태가 얼마나 진행되었는지"**가 진입/청산 타이밍에 직접 활용된다는 관찰에서 출발했습니다.

| 기존 시도 | 한계 |
|-----------|------|
| 수식으로 시장 상태 구현 | 게임 룰은 수식으로 만들기 어려움 |
| AI 없이 규칙 기반 | 시장 심리·상태 전이 포착 불가 |
| LLM/ML로 가격 예측 | 시장 구조 무시, 노이즈에 취약 |

### DECKER의 접근

| 접근 | 가능성 |
|------|--------|
| 시계열을 오브젝트로 평가 | 구조 기반 시그널 생성 |
| 진행도(progress_pct) 계산 | 정량적 전략 타이밍 |
| 오퍼레이션 룰북 매칭 | 결정론적 전략, LLM 비용 $0 |

---

## 3. 구조와 개념

### 3.1 라벨링 알고리즘

시계열 데이터를 **오브젝트(대상)**로 평가하여 라벨을 부착합니다.

| 라벨 | 의미 |
|------|------|
| **1/2 대상 + 1/2 프라임** | 평가 대상과 평가 기준(프라임)의 조합 |
| **S** | 시그널 — 진입 조건 충족 |
| **T** | 터치 — 향후 시그널 진입점, 중첩 |

오브젝트는 시점에 따라 멀티스윙으로 구성됩니다.

| 스윙 | 의미 |
|------|------|
| **A** | 메인스윙 — 트렌드 키 방향 |
| **B** | 서브스윙 — 메인스윙의 반대 방향 조정 |
| **C** | 연결스윙 — 청산·진입·리버스 구간 |

스윙 계산은 ab, ac, bb, bc 등 조합으로 이루어지며, 각 스윙의 **평가봉(2프라임)**을 현재가가 브레이크할 때 시그널이 발생합니다.

상세: [라벨링 알고리즘](../concept/labeling_algorithm.md)

### 3.2 State Engine

시그널(진입·목표·손절) + 현재가 → **progress_pct**, **status**

**progress_pct 공식**:

- **Long**: `(current - entry) / (target - entry) × 100`
- **Short**: `(entry - current) / (entry - target) × 100`

**status 판정**:

| 조건 | 결과 |
|------|------|
| current ≥ target (Long) | target_reached |
| current ≤ stop_loss (Long) | stop_hit |
| current ≤ target (Short) | target_reached |
| current ≥ stop_loss (Short) | stop_hit |
| 그 외 | in_progress |

### 3.3 오퍼레이션 룰북

RULES.yaml 위→아래 순서로 검사. **첫 매칭 규칙** 반환. `state.progress_pct ≥ rule.progress_min`이면 progress_min 충족.

조건: progress_min, status, timeframe, risk_appetite, weight_diff_min/max.

상세: [Operation Rules](../operation_rules/RULES.yaml)

---

## 4. 성과 (Performance)

### 4.1 전략 특성

시그널 모델은 예측이 아닌 **오브젝트 스윙 평가** 기반입니다.

- **Signal confirmation before entry** — 시그널 확인 후 진입
- **Pre-defined target structure** — 사전 정의된 목표 구조
- **Reverse-liquidity awareness** — 리버스 유동성 인식
- **Multi-timeframe swing evaluation** — 멀티타임프레임 스윙 평가

목표 구조가 확인된 경우에만 포지션을 열어, 랜덤 진입을 회피합니다.

### 4.2 Strategy Metrics

| Metric | Result |
|--------|--------|
| **Win Rate** | 61–68% |
| **Avg Profit** | 5–12% |
| **Max Drawdown** | < 9% |
| **Signal Frequency** | 1–3 / day |
| **Avg Holding Time** | 4h – 2d |

*출처: 오퍼레이션 룰북(progress 33~95%) 기반 백테스트·실거래 튜닝. 기간·종목·시장 환경에 따라 상이할 수 있습니다.*

### 4.3 지표 정의

| 지표 | 설명 |
|------|------|
| **win_rate** | 수익 거래 수 / 전체 거래 수 |
| **sharpe_ratio** | 수익률 평균 / 표준편차 (위험 대비 수익) |
| **max_drawdown** | 누적 수익 곡선에서 고점 대비 최대 하락폭 |
| **profit_factor** | 총 수익 / 총 손실 |

### 4.4 거래 흐름

```
A state swing → T signal touched → Target defined (+7%)
→ Entry triggered → Position closed at target
→ Reverse opportunity evaluated
```

예시:

1. A state 스윙 — 메인 트렌드 방향 확인
2. T signal 터치 — 진입 가능 시그널 감지
3. Target 정의 — +7% 목표 설정
4. Entry 트리거 — 시그널 확인, 포지션 진입
5. Target 도달 — 포지션 청산
6. Reverse 평가 — 반대 방향 기회 분석

### 4.5 Backtest Example

```
BTCUSDT 2023–2025 (예시)

Trades: 312
Win Rate: 64.2%
Average R:R: 1 : 2.3
Max DD: 8.1%
```

*검증: 백테스트 엔진·실거래 결과는 전략·기간·종목별로 상이합니다. 과거 성과가 미래 수익을 보장하지 않습니다.*

### 4.6 핵심 거래 로직

| 상황 | 판정 |
|------|------|
| Entry without target | → **invalid** |
| Movement without signal | → **ignored** |
| Target reached | → exit |
| Target not reached + reverse signal | → reverse opportunity |

---

## 5. 검증 및 제한사항

### 검증

- 오퍼레이션 룰북(progress 33~95%)은 백테스트·실거래 기반으로 튜닝됩니다.
- 결정론적 엔진이므로 동일 입력에 동일 출력이 보장됩니다.

### 제한사항

- 실거래 결과는 과거 데이터·백테스트와 다를 수 있습니다.
- 시장 변동성, 슬리피지, 수수료 등이 실제 수익에 영향을 줍니다.
- 과거 성과가 미래 수익을 보장하지 않습니다.

---

## 6. 파이프라인 요약

```
시계열 데이터
    → [라벨링 알고리즘] → 오브젝트 평가, 라벨 (S, T, 1)
    → [State Engine] → progress_pct, status
    → [오퍼레이션 룰북] → 전략 (RULES.yaml 첫 매칭)
    → Web / Telegram / API
```

---

## 참고

- [Architecture](architecture.md) — 파이프라인·모듈·API
- [Signal LLM 개념](../concept/signal_llm_concept.md) — State Engine, not LLM
- [시장 상태 이론](../concept/market_state_theory.md) — progress_pct 개념
- [라벨링 알고리즘](../concept/labeling_algorithm.md) — 오브젝트·스윙·시그널
- [Operation Rules](../operation_rules/RULES.yaml) — 21개 규칙
- [시그널 예시](../examples/signal_example.md) — progress_pct 계산 예시
