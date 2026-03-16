# Decker 모델: 알고리즘과 성과

**대상**: 심층 고객 — 알고리즘 스토리, 구조·개념, 모델 성과를 알고 싶은 분

---

## 1. 알고리즘 스토리

### 탄생 배경

시그널·진행도 기반 전략은 **"상태가 얼마나 진행되었는지"**가 진입/청산 타이밍에 직접 활용된다는 관찰에서 출발했습니다.

기존 트레이딩 봇은 "매수/매도" 신호만 제공합니다. DECKER는 **진행도(progress_pct)**와 **상태(status)**를 추가하여, 사용자가 "지금 66% 진행 — 30% 부분 익절 제안" 같은 구체적 전략을 받을 수 있도록 했습니다.

### 왜 progress_pct, status, RULES 구조인가

- **progress_pct**: 진입가→목표가 구간에서 현재가의 위치를 %로 표현. 직관적이고 전략 조건으로 사용하기 쉬움.
- **status**: target_reached, stop_hit, in_progress 등 — 시그널의 "결과"를 명확히 구분.
- **RULES.yaml**: progress_min, timeframe, risk_appetite 조합으로 규칙 매칭. LLM 없이 결정론적으로 전략 반환 → 토큰 비용 $0.

---

## 2. 구조와 개념

### 2.1 라벨링 알고리즘

시계열 데이터를 **오브젝트(대상)**로 평가하여 라벨(S, T, 1 등) 부착. 스윙(A/B/C) 계산, 평가봉 브레이크 시 시그널 발생.

상세: [concept/labeling_algorithm.md](../concept/labeling_algorithm.md)

### 2.2 State Engine

시그널(진입·목표·손절) + 현재가 → progress_pct, status

**progress_pct 공식**:

- **Long**: `(current - entry) / (target - entry) × 100`
- **Short**: `(entry - current) / (entry - target) × 100`

**status 판정**:

- Long: current ≥ target → target_reached / current ≤ stop_loss → stop_hit
- Short: current ≤ target → target_reached / current ≥ stop_loss → stop_hit
- 그 외 → in_progress

### 2.3 오퍼레이션 룰북

- RULES.yaml 위→아래 순서로 검사. **첫 매칭 규칙** 반환.
- 조건: progress_min, status, timeframe, risk_appetite, weight_diff_min/max
- `state.progress_pct ≥ rule.progress_min`이면 progress_min 조건 충족.

---

## 3. 모델 성과

### 3.1 지표 정의

| 지표 | 설명 |
|------|------|
| **win_rate** | 수익 거래 수 / 전체 거래 수 |
| **sharpe_ratio** | 수익률의 평균 / 표준편차 (위험 대비 수익) |
| **max_drawdown** | 누적 수익 곡선에서 고점 대비 최대 하락폭 |
| **profit_factor** | 총 수익 / 총 손실 |

### 3.2 검증

- 백테스트·모의거래 결과는 전략·기간·종목에 따라 상이합니다.
- 오퍼레이션 룰북(progress 33~95% 구간)은 백테스트·실거래 기반으로 튜닝됩니다.

### 3.3 제한사항

- 실거래 결과는 과거 데이터·백테스트와 다를 수 있습니다.
- 시장 변동성, 슬리피지, 수수료 등이 실제 수익에 영향을 줍니다.

---

## 4. 파이프라인 요약

```
시계열 데이터
    → [라벨링 알고리즘] → 라벨된 시그널
    → [State Engine] → progress_pct, status
    → [오퍼레이션 룰북] → 전략 (RULES.yaml 첫 매칭)
    → Web / Telegram / API
```

---

## 참고

- [Architecture](architecture.md)
- [Signal LLM 개념](../concept/signal_llm_concept.md)
- [시장 상태 이론](../concept/market_state_theory.md)
- [Operation Rules](../operation_rules/RULES.yaml)
