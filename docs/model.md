# Decker Model — Algorithm Story and Performance

**Audience**: Readers who want the algorithm story, structure, differentiation, and performance metrics — in one place.

---

## English overview

Decker is built on three pillars:

1. **Target → Signal → Entry** — Target structure is defined before entry; signals confirm that structure.
2. **Sequence Engine (Context Engine)** — Candles are read as a grammatical sequence; a 5-state machine tracks structural position; a ternary **operation gate** (`GO` / `WATCH` / `HOLD`) expresses operational mode.
3. **RULES + optional LLM** — [RULES.yaml](../operation_rules/RULES.yaml) matches state to strategy (**$0** on the rules path). The LLM only narrates the result.

Concept docs: [Sequence Engine](../concept/sequence_engine.md) · [Labeling](../concept/labeling_algorithm.md) · [Diagrams](../diagrams/system_flow.md)

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
| 시퀀스 라벨 + 상태 머신 | 구조 기반 시그널, 재현 가능한 전이 |
| 진행도(progress_pct) 계산 | 정량적 전략 타이밍 |
| 오퍼레이션 룰북 매칭 | 결정론적 전략, LLM 비용 $0 (룰 경로) |
| GO/WATCH/HOLD 게이트 | 이진 신호가 놓치는 "관망 vs 리스크오프" 구분 |

---

## 3. 구조와 개념

### 3.1 시퀀스 라벨링 (현행 제품 축)

시계열 봉은 **역할(role)**로 라벨됩니다 — 앵커(C), 테스트(B), 시그널/확인, 커넥터, 와이드 브레이크(W) 등. 라벨은 **봉 관계**(이전 봉 대비 고저 돌파·인사이드 등)로 결정되며, **문법 규칙**(예: 시그널은 특정 시퀀스 이후에만)을 따릅니다.

동시에 **3개 레인**을 추적합니다: 메인 스윙, 서브 스윙(역방 압력), 커넥터 구간.

| 구성 요소 | 의미 |
|-----------|------|
| **Sequence labels** | 각 봉의 구조적 역할 |
| **5-state FSM** | INIT → C_SET → B_FORMING → B_SET → W_PENDING |
| **operation_gate** | GO / WATCH / HOLD |
| **label_quality** | confidence, stability, regime_consistency |

상세: [라벨링 알고리즘](../concept/labeling_algorithm.md) · [Sequence Engine](../concept/sequence_engine.md) · [시스템 다이어그램](../diagrams/system_flow.md)

### 3.2 State Engine (progress_pct · status)

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

조건 예: progress_min, status, timeframe, risk_appetite, weight_diff_min/max, tf_alignment, entry_timing, 엔진 합성 키(문서·버전은 [RULES.yaml 헤더](../operation_rules/RULES.yaml) 참고).

상세: [Operation Rules](../operation_rules/RULES.yaml)

---

## 4. 성과 (Performance)

### 4.1 전략 특성

시그널 모델은 단일 지표 예측이 아니라 **구조·진행도·룰북** 기반입니다.

- **Signal confirmation before entry** — 시그널 확인 후 진입
- **Pre-defined target structure** — 사전 정의된 목표 구조
- **Reverse-liquidity awareness** — 리버스 유동성 인식
- **Multi-timeframe alignment** — 멀티 타임프레임 정렬 (RULES 레이어)

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

### 4.4 거래 흐름 (개념)

```
Structural cycle completes → Target defined → Entry with risk bounds
→ progress_pct tracked → RULES suggest partial TP / hold / exit
→ Target or stop → Reverse opportunity evaluated
```

예시 단계:

1. 시퀀스·상태 머신으로 구조적 국면 확정
2. 시그널(방향·진입·목표·손절)과 현재가로 progress_pct 산출
3. RULES 첫 매칭으로 전략·choices 제공
4. (선택) LLM이 동일 입력을 자연어로 설명

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

## 6. 파이프라인 요약 (Phase 4)

```
OHLCV candles
    → [Sequence labeling] → roles + 3-lane context + label_quality
    → [5-state machine] → structural state + operation_gate (GO/WATCH/HOLD)
    → [State Engine] → progress_pct, status (signal lifecycle)
    → [RULES.yaml] → strategy + ranked choices (first match)
    → [LLM consultation, optional] → natural language (does not override engine)
    → Web / Telegram / API
```

---

## 참고

- [Architecture](architecture.md) — 파이프라인·모듈·API
- [Signal LLM 개념](../concept/signal_llm_concept.md) — State Engine, not LLM
- [시장 상태 이론](../concept/market_state_theory.md) — progress_pct
- [라벨링 알고리즘](../concept/labeling_algorithm.md) — 시퀀스 라벨링
- [Operation Rules](../operation_rules/RULES.yaml)
- [시그널 예시](../examples/signal_example.md)
- [Article series](medium/README.md)
