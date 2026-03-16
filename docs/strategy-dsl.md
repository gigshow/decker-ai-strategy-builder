# Strategy DSL 사양

**YAML 기반 전략 정의. 진입 객체와 진행도를 자유롭게 지정합니다.**

---

## 개요

Strategy DSL은 시장 상태(A/B/C), 진행도(progress_pct), 오브젝트, 프라임 단계를 조합하여 진입/청산 규칙을 정의하는 YAML 기반 사양입니다.

기존 오퍼레이션 룰북(RULES.yaml)이 범용 규칙을 제공한다면, Strategy DSL은 **사용자 정의 전략**을 위한 확장 사양입니다.

---

## DSL 구조

```yaml
name: "BullBreak"
interval: "1h"

entry:
  state: "A"
  progress_min: 30
  object: "prev_high"

exit:
  progress_gte: 85
  or_state: "C"

risk:
  position_pct: 5
  stop_loss_pct: 2.0
```

---

## 필드 설명

### 기본

| 필드 | 타입 | 설명 |
|------|------|------|
| `name` | string | 전략 이름 |
| `interval` | string | 봉 타임프레임 (15m, 1h, 4h, 8h, 1d, 1w) |

### Entry (진입 조건)

| 필드 | 타입 | 설명 |
|------|------|------|
| `state` | string | 진입 시장 상태 (A, B, C) |
| `progress_min` | number | 최소 진행도 (%) |
| `progress_max` | number | 최대 진행도 (%) |
| `object` | string | 시장 오브젝트 (prev_high, prev_low 등) |
| `prime_stage` | string | 프라임 단계 (1/2, 1/2') |

### Exit (청산 조건)

| 필드 | 타입 | 설명 |
|------|------|------|
| `progress_gte` | number | 이 진행도 이상이면 청산 (%) |
| `or_state` | string | 또는 이 상태에서 청산 |

### Risk (리스크)

| 필드 | 타입 | 설명 |
|------|------|------|
| `position_pct` | number | 포트폴리오 대비 포지션 비율 (%) |
| `stop_loss_pct` | number | 손절 퍼센트 (%) |

---

## 예시: 전략 시나리오

### BullBreak — 상승 돌파

```yaml
name: "BullBreak"
interval: "1h"
entry:
  state: "A"
  progress_min: 30
  object: "prev_high"
exit:
  progress_gte: 85
  or_state: "C"
risk:
  position_pct: 5
  stop_loss_pct: 2.0
```

**동작**: state=A이면서 progress≥30%이고 prev_high 오브젝트 접근 시 BUY. progress≥85% 또는 C 연결스윙 진입 시 EXIT.

### ReversePlay — 리버스 진입

```yaml
name: "ReversePlay"
interval: "4h"
entry:
  state: "C"
  progress_min: 0
  object: "liquidity_zone"
exit:
  progress_gte: 60
  or_state: "A"
risk:
  position_pct: 3
  stop_loss_pct: 3.0
```

**동작**: C 연결스윙에서 유동성 청산 구간 진입. 진행도 60% 또는 A 메인스윙 전환 시 EXIT.

### TrendFollow — 트렌드 추종

```yaml
name: "TrendFollow"
interval: "1d"
entry:
  state: "A"
  progress_min: 50
  prime_stage: "1/2'"
exit:
  progress_gte: 90
risk:
  position_pct: 8
  stop_loss_pct: 1.5
```

**동작**: A 메인스윙 진행도 50% 이상 + 2프라임 브레이크 확인 시 진입. 90% 도달 시 청산.

---

## 오퍼레이션 룰북과의 관계

| 구분 | RULES.yaml | Strategy DSL |
|------|------------|--------------|
| 용도 | 범용 규칙 (17개) | 사용자 정의 전략 |
| 조건 | progress_min, status, timeframe, risk_appetite | state, object, prime_stage, progress 범위 |
| 매칭 | 첫 매칭 규칙 반환 | 전략별 독립 평가 |
| LLM | 미사용 | 미사용 |

두 시스템은 **상호 보완적**입니다. 룰북은 기본 전략을, DSL은 고급 사용자의 커스텀 전략을 담당합니다.

---

## 참고

- [Architecture](architecture.md) — 파이프라인·State Engine
- [Operation Rules](../operation_rules/RULES.yaml) — 기본 룰북
- [시그널 예시](../examples/signal_example.md) — 실제 적용 예시
