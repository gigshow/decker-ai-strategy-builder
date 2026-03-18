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

## 다중 TF 정렬 모델 (Multi-TF Alignment)

시장 상태는 **단일 TF가 아니라 복수 TF의 조합**으로 이해해야 합니다.

### TF 계층

```
1w (주봉) ← 최상위 의지 (메이커의 장기 목표)
1d (일봉)
8h
4h         ← 메이커의 주 활동 구간
1h
15m        ← 단기 신호 발생
```

### tf_alignment: 신호 TF와 상위 TF 방향 비교

| tf_alignment | 의미 | 신뢰도 | 포지션 크기 |
|---|---|---|---|
| `fully_aligned` | 신호 TF + 모든 상위 TF 동일 A스윙 방향 | 최고 | 100% |
| `lower_aligned` | 신호 + 직상위 1~2 TF 정렬, 더 큰 TF 반대 | 중간 | 50~70% |
| `counter_trend` | 대부분 상위 TF가 반대 A스윙 | 최저 | 20~30% |
| `transition` | 상위 TF 중 C 연결스윙 구간 존재 (전환 테스트) | 잠재 높음 | 30~50% 시작 |
| `mixed` | 혼합 / 명확한 패턴 없음 | 낮음 | 30~40% |

### 핵심 시나리오

**역추세 반등 (counter_trend)**:
```
1h: A+ (매수 신호)  ← 신호 발생
4h: A- (하락 메인스윙)
1d: A- (하락 메인스윙)
```
→ 1h가 4h/1d 하락 중 B 또는 C 파동 반등일 가능성.  
→ 목표가 = 4h 매도 저항가 이하. 소규모 포지션.

**전환 구간 (transition)**:
```
1h: A+ (매수 신호)
4h: C 연결스윙 (전환 테스트 중)
1d: A- (하락 메인스윙)
```
→ 4h 방향 전환 가능성 열림 (확인 필요).  
→ 퍼즐처럼: 4h A+ 전환 확인 시 포지션 점진적 증가.

**전체 정렬 (fully_aligned)**:
```
1h: A+ / 4h: A+ / 1d: A+
```
→ 모든 의지 일치. 가장 신뢰도 높은 진입 기회.

---

## 3축 시장 상태 모델

완전한 시장 상태 이해를 위해 3개 축을 조합합니다:

| 축 | 출처 | 의미 |
|---|---|---|
| **progress_pct** | `build_signal_state()` | 이 시그널이 목표까지 얼마나 갔는가 |
| **market_state** | `MarketStateAggregator` (청산/유동성) | 지금 시장 유동성 국면 (trend/range) |
| **tf_alignment** | `tf_alignment_utils.py` (다중TF 방향 비교) | 이 신호가 큰 그림과 일치하는가 |

---

## 오퍼레이션 룰북과의 관계

오퍼레이션 룰북(RULES.yaml v2.0.0)은 이 3축을 조합하여 전략을 결정합니다.

| 규칙 레이어 | 사용 축 |
|---|---|
| STATUS 레이어 | status |
| PORTFOLIO 레이어 | weight_diff + progress_pct |
| TF ALIGNMENT 레이어 (v2.0.0) | tf_alignment + progress_pct |
| SWING STATE 레이어 (v2.0.0) | swing_state |
| MARKET STATE 레이어 (v1.4.0) | market_state + progress_pct |
| PROGRESS 레이어 | progress_pct + timeframe + risk_appetite |

---

## 참고

- [Signal LLM 개념](signal_llm_concept.md)
- [라벨링 알고리즘](labeling_algorithm.md)
- [Architecture](../docs/architecture.md)
- [다중TF 분석](../../docs/multi_tf_시장상태_분석_및_개선_20260318.md)
