# Strategy DSL 사양

**YAML 기반 전략 정의. 진입 객체, 진행도, 다중 TF 정렬 조건을 자유롭게 지정합니다.**

> ⚠️ **구현 상태**: 이 문서는 **사양(spec)**입니다. 현재 API는 RULES.yaml 형식만 지원합니다. DSL 파서 및 `state`/`object`/`prime_stage`/`tf_alignment` 조건 평가는 로드맵입니다.

---

## 개요

Strategy DSL은 시장 상태(A/B/C), 진행도(progress_pct), 오브젝트, 프라임 단계, 다중 TF 정렬, 진입 타이밍을 조합하여 **완전한 거래 전략**을 정의하는 YAML 기반 사양입니다.

기존 오퍼레이션 룰북(RULES.yaml)이 범용 규칙을 제공한다면, Strategy DSL은 **사용자 정의 + AI 학습 기반 전략**을 위한 확장 사양입니다.

**진화 경로**: 오퍼레이션 룰북(수동 규칙) → 전략 DSL(실데이터 기반 자동 파인튜닝)

**RULES와 관계**: RULES.yaml의 tf_alignment, swing_state, entry_timing은 Strategy DSL의 **부분 집합**. RULES = DSL v1. DSL 파서 없이도 trade_outcomes → RULES 패치 제안 가능.

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
| `entry_timing` | string | 진입 타이밍 (predictive / signal / confirmation) |
| `notification_on` | list | 알림 트리거 단계 (object_forming / evaluation_start / signal / confirmation) |

### Entry (진입 조건)

| 필드 | 타입 | 설명 |
|------|------|------|
| `state` | string | 진입 시장 상태 (A, B, C) |
| `progress_min` | number | 최소 진행도 (%) |
| `progress_max` | number | 최대 진행도 (%) |
| `object` | string | 시장 오브젝트 (prev_high, prev_low, liquidity_zone 등) |
| `prime_stage` | string | 프라임 단계 (1/2, 1/2') |
| `tf_alignment` | string | 다중 TF 정렬 조건 (fully_aligned, lower_aligned, counter_trend, transition, mixed) |
| `higher_tf_state` | string | 직상위 TF 스윙 상태 (A, B, C) |

### Exit (청산 조건)

| 필드 | 타입 | 설명 |
|------|------|------|
| `progress_gte` | number | 이 진행도 이상이면 청산 (%) |
| `or_state` | string | 또는 이 상태에서 청산 |
| `or_tf_change` | string | 상위 TF 스윙 전환 시 청산 (예: "4h:A-" = 4h가 A-로 전환되면 청산) |

### Risk (리스크)

| 필드 | 타입 | 설명 |
|------|------|------|
| `position_pct` | number | 포트폴리오 대비 포지션 비율 (%) |
| `stop_loss_pct` | number | 손절 퍼센트 (%) |
| `scale_in_on` | string | 특정 조건 충족 시 포지션 추가 (예: "4h:A+" = 4h A+ 전환 확인 시) |

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
  tf_alignment: fully_aligned   # 모든 상위 TF 동일 방향일 때만
exit:
  progress_gte: 90
risk:
  position_pct: 8
  stop_loss_pct: 1.5
```

**동작**: A 메인스윙 50% + 2프라임 브레이크 + 전체 TF 정렬 시 진입. 90% 도달 시 청산.

---

### CounterTrendBounce — 역추세 반등 포착

```yaml
name: "CounterTrendBounce"
interval: "1h"
entry:
  state: "B"                      # 서브스윙(조정 반등)
  tf_alignment: counter_trend     # 상위 TF는 반대 방향
  progress_min: 0
  progress_max: 30
exit:
  progress_gte: 60                # 상위 TF 저항 도달 전 청산
  or_tf_change: "4h:A-"          # 4h A- 지속 확인 시 청산 가속
risk:
  position_pct: 2                 # 역추세: 소규모
  stop_loss_pct: 1.5
```

**동작**: 상위 TF 하락 중 1h B 서브스윙 반등. 60% 또는 4h 저항 확인 시 청산. 소규모 포지션.

---

### TransitionScaleIn — TF 전환 구간 스케일인

```yaml
name: "TransitionScaleIn"
interval: "1h"
entry:
  state: "A"
  tf_alignment: transition        # 상위 TF C스윙 전환 테스트 중
  progress_min: 10
exit:
  progress_gte: 85
  or_tf_change: "4h:A-"          # 4h 전환 실패 시 청산
risk:
  position_pct: 3                 # 초기 소규모
  stop_loss_pct: 2.0
  scale_in_on: "4h:A+"           # 4h A+ 전환 확인 시 포지션 추가
```

**동작**: 4h 전환 테스트 중 1h A+ 신호. 소규모 선진입 후 4h A+ 확인 시 스케일인.

---

## 오퍼레이션 룰북과의 관계

| 구분 | RULES.yaml (오퍼레이션 룰북) | Strategy DSL |
|------|------------------------------|--------------|
| 역할 | 범용 포지션 관리 규칙 | 사용자 정의 완전 전략 |
| 조건 | progress_min, status, timeframe, risk_appetite, tf_alignment, swing_state | state A/B/C, object, prime_stage, tf_alignment, higher_tf_state |
| 진입 결정 | tf_alignment 레이어 (v2.0.0) | ✅ entry 섹션 포함 |
| 청산 결정 | ✅ progress 기반 | ✅ exit + or_tf_change |
| 리스크 관리 | 자연어만 | ✅ position_pct, stop_loss_pct, scale_in_on |
| 현재 구현 | ✅ v2.0.0 (35개+ 규칙) | ❌ 미구현 (로드맵) |
| AI 학습 대상 | ✅ 1차 목표 | ✅ 최종 목표 |

**진화 경로**: 오퍼레이션 룰북(수동 규칙) → 전략 DSL(AI 학습 기반 자동 전략)

---

## 참고

- [Architecture](architecture.md) — 파이프라인·State Engine
- [Operation Rules](../operation_rules/RULES.yaml) — 기본 룰북 (v2.0.0)
- [시장 상태 이론](../concept/market_state_theory.md) — tf_alignment, 3축 모델
- [라벨링 알고리즘](../concept/labeling_algorithm.md) — A/B/C 스윙, 2프라임
- [다중TF 분석](../../docs/multi_tf_시장상태_분석_및_개선_20260318.md)
- [덱커 서비스 모델](../../docs/덱커_서비스모델_상태엔진_운용_20260318.md) — 학습 루프, 알림 트리거

---

## 학습 기반 DSL 진화

Strategy DSL은 정적으로 작성되는 것이 아니라, 실데이터에 의해 지속적으로 파인튜닝됩니다.

```
[거래 실행]
    entry_timing, tf_alignment, swing_state, progress_pct at entry
         │
         ▼
[결과 수집: trade_outcomes]
    outcome: win/loss, actual_rr, rule_matched
         │
         ▼
[signal_performance_aggregator.aggregate_win_rate_multidim()]
    (entry_timing × tf_alignment × swing_state × progress) → win_rate, avg_rr
         │
         ▼
[suggest_rule_patches()]
    win_rate 저조 구간 → DSL 조건/포지션 수정 제안
         │
         ▼
[DSL 버전 업데이트]
    자동 패치 또는 리뷰 후 반영 → 다음 버전
```

**목표**: 거래 데이터가 쌓일수록 DSL이 최적화되어 수익률이 향상됩니다.

---

## 알림 트리거 (Proactive Notification)

DSL에 `notification_on`을 지정하면, 해당 단계에서 AI가 선제 알림을 보냅니다.

| 트리거 | 시점 | 의미 |
|--------|------|------|
| `object_forming` | 오브젝트 형성 감지 | "신호 가능성 탐지" — 예측 진입 준비 |
| `evaluation_start` | 평가 시작 (1/2 도달) | "평가 진행 중" — 기존 포지션 점검 |
| `signal` | S 라벨 발생 | "신호 확인됨" — 표준 진입 |
| `confirmation` | 스윙 테스트 통과 | "확정" — 안전 진입 또는 포지션 증가 |

예시:
```yaml
notification_on:
  - evaluation_start   # 평가 시작 시 기존 롱 포지션 점검 알림
  - signal             # 신호 발생 시 진입 알림
```

이 트리거는 AI 대화 레이어(LLM)가 사용자에게 "지금 어떤 상태인지, 어떤 선택을 할 수 있는지"를 먼저 알려주는 기반입니다.
