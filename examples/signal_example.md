# 시그널 → State → Strategy 예시

---

## 1. 시그널 입력

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

## 2. Trade Flow

```
A state swing → T signal touched → Target defined (+4.2%)
→ Entry triggered (96000) → Target execution → Exit / Reverse
```

### 라벨링 과정

1. 시계열 분석 → 이전 저점이 오브젝트로 식별
2. 프라임 평가 → 96000 레벨에서 1/2 평가 확인
3. 스윙 분류 → A 메인스윙 (상승 방향)
4. 평가봉(2프라임) 브레이크 → **시그널(S) 발생**
5. Target 정의: 100000 (이전 고점 기반)

---

## 3. State Engine 계산

현재가: **98,400**

**progress_pct** (Long):

```
(current - entry) / (target - entry) × 100
= (98400 - 96000) / (100000 - 96000) × 100
= 2400 / 4000 × 100
= 60%
```

**status**: in_progress (목표 100,000 미도달, 손절 92,000 미도달)

---

## 4. 오퍼레이션 룰북 매칭

RULES.yaml 위→아래 검사:

- progress_min: 66 → 60% 미만, 불일치
- progress_min: 50, risk_appetite: [high] → 조건에 따라 매칭 가능

**매칭 결과**: "60% 진행. 리스크 허용 시 홀드 권장. 66% 도달 시 30% 부분 익절 제안."

---

## 5. 시나리오별 결과

| 현재가 | progress_pct | status | 전략 |
|--------|--------------|--------|------|
| 96,000 | 0% | in_progress | 진입 직후. 목표 도달까지 홀드 |
| 98,000 | 50% | in_progress | 50% 진행. risk_appetite에 따라 판단 |
| 98,640 | 66% | in_progress | **66% 진행. 30% 부분 익절 제안** |
| 99,200 | 80% | in_progress | 80% 진행. 50% 부분 익절 후 나머지 홀드 |
| 100,000 | 100% | target_reached | **목표 도달. 전량 청산. Reverse 평가** |
| 92,000 | — | stop_hit | **손절 구간. 청산 또는 관망** |

---

## 6. Target → Signal → Entry 적용

이 예시에서 거래 순서는:

1. **Target**: 100,000 (이전 고점 기반 목표 구조 확인)
2. **Signal**: A 스윙 + 2프라임 브레이크 → S 시그널 발생
3. **Entry**: 96,000 (기대값 +4.2%, 손절 -4.2% 정의 완료 후 진입)

목표가 없었다면 이 진입은 **invalid** 처리됩니다.

---

## 7. API 호출 예시

```bash
# State 조회
curl "https://api.decker-ai.com/api/v1/signals/BTCUSDT/state"

# Strategy 조회
curl "https://api.decker-ai.com/api/v1/signals/BTCUSDT/strategy?timeframe=4h&risk_appetite=medium"

# 시그널 목록
curl "https://api.decker-ai.com/api/v1/judgment/signals/public"
```

---

## 참고

- [Architecture](../docs/architecture.md) — 파이프라인·State Engine
- [모델·알고리즘·성과](../docs/model.md) — 성과 지표
- [Operation Rules](../operation_rules/RULES.yaml) — 35개+ 규칙
- [API Guide](../docs/api-guide.md)
