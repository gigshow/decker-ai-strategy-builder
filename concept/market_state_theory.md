# 시장 상태 이론

---

## 진행도(progress_pct) 개념

DECKER의 핵심 차별점은 **"상태가 얼마나 진행되었는지"**를 계산한다는 것입니다.

기존 트레이딩 봇은 "횡보 vs 상승 vs 하락" 같은 **현재 상태**만 알려줍니다.  
DECKER는 해당 상태가 **몇 % 진행되었는지**까지 계산합니다.

이 정보는 진입/청산 타이밍 결정에 직접 활용됩니다.

---

## 시장 구조와 전략 타이밍

| 구분 | 설명 |
|------|------|
| **진입** | progress_pct가 특정 구간(예: 30~70%)일 때 진입 검토 |
| **부분 익절** | progress_pct 66%, 80%, 90% 등에서 룰북에 따라 제안 |
| **전량 청산** | target_reached 또는 stop_hit 시 |

오퍼레이션 룰북은 "진행 단계"가 아니라 **상태·시간프레임·현재가격에 따라 행동이 달라진다**는 개념이 우선입니다.

---

## progress_pct 계산

시그널(진입가·목표가·손절가) + 현재가 → progress_pct

- **Long**: `(current - entry) / (target - entry) × 100`
- **Short**: `(entry - current) / (entry - target) × 100`

State Engine이 `build_signal_state`로 계산합니다.

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

## 참고

- [Signal LLM 개념](signal_llm_concept.md)
- [라벨링 알고리즘](labeling_algorithm.md)
- [Architecture](../docs/architecture.md)
