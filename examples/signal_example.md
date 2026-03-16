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

## 2. 현재가 가정

- **현재가**: 98,400

---

## 3. State Engine 계산

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
- ...

**예시 매칭 결과**: "60% 진행. 리스크 허용 시 홀드 권장. 66% 도달 시 30% 부분 익절 제안."

---

## 5. API 호출 예시

```bash
# State 조회
curl "https://api.decker-ai.com/api/v1/signals/BTCUSDT/state"

# Strategy 조회 (timeframe, risk_appetite 지정)
curl "https://api.decker-ai.com/api/v1/signals/BTCUSDT/strategy?timeframe=4h&risk_appetite=medium"
```

---

## 6. 시나리오별 결과

| 현재가 | progress_pct | status | 전략 예시 |
|--------|--------------|--------|-----------|
| 96,000 | 0% | in_progress | 진행 중. 목표 도달까지 홀드 권장. |
| 98,000 | 50% | in_progress | 50% 진행. (risk_appetite에 따라) |
| 99,200 | 80% | in_progress | 80% 이상 진행. 50% 부분 익절 후 나머지는 목표까지 홀드 권장. |
| 100,000 | 100% | target_reached | 목표 도달. 전량 청산 권장. |
| 92,000 | — | stop_hit | 손절 구간. 청산 또는 관망 권장. |

---

## 참고

- [API Guide](../docs/api-guide.md)
- [Architecture](../docs/architecture.md)
- [Operation Rules](../operation_rules/RULES.yaml)
