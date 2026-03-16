# 시장 상태 이론

---

## 핵심 개념

기존 트레이딩 봇은 "횡보 vs 상승 vs 하락" 같은 **현재 상태**만 알려줍니다.

DECKER는 해당 상태가 **몇 % 진행되었는지**까지 계산합니다. 이 정보가 진입/청산 타이밍 결정에 직접 사용됩니다.

---

## 시장 구조: Object와 Swing

시장 상태는 **오브젝트(Object)**와 **스윙(Swing)**으로 구성됩니다.

### 오브젝트

시계열 데이터에서 식별되는 평가 대상입니다. 고점, 저점, 유동성 구간 등이 오브젝트로 정의됩니다.

### 스윙

| 스윙 | 의미 | 역할 |
|------|------|------|
| **A** | 메인스윙 | 트렌드 키 방향, 2개 이상의 평가 대상이 위/아래에 위치할 때 방향 결정 |
| **B** | 서브스윙 | 메인스윙의 반대 방향 조정 |
| **C** | 연결스윙 | 청산·진입·리버스가 일어나는 구간 |

스윙의 조합(ab, ac, bb, bc 등)으로 시장 구조를 계산하며, **평가봉(2프라임)** 브레이크 시 시그널이 발생합니다.

---

## 진행도(progress_pct)

시그널(진입가·목표가·손절가) + 현재가 → progress_pct

### 공식

- **Long**: `(current - entry) / (target - entry) × 100`
- **Short**: `(entry - current) / (entry - target) × 100`

State Engine이 `build_signal_state`로 계산합니다.

### 전략 타이밍

| 구분 | 설명 |
|------|------|
| **진입** | progress_pct가 특정 구간(예: 30~70%)일 때 진입 검토 |
| **부분 익절** | progress_pct 66%, 80%, 90% 등에서 룰북에 따라 제안 |
| **전량 청산** | target_reached 또는 stop_hit 시 |

---

## status 의미

| status | 의미 |
|--------|------|
| in_progress | 진행 중 |
| target_reached | 목표 도달 |
| stop_hit | 손절 구간 |
| expired | 만료 |
| unknown | 미판정 |

---

## 오퍼레이션 룰북과의 관계

오퍼레이션 룰북은 "진행 단계"가 아니라 **상태·시간프레임·현재가격에 따라 행동이 달라진다**는 개념이 우선입니다.

status, timeframe, current_price(→progress_pct) 등 조건이 조합되면 그에 맞는 전략(행동)이 매칭됩니다.

---

## 참고

- [Signal LLM 개념](signal_llm_concept.md)
- [라벨링 알고리즘](labeling_algorithm.md)
- [Architecture](../docs/architecture.md)
