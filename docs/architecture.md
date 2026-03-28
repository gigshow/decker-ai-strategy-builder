# Decker AI Architecture

**Decker AI Strategy Builder — 시장 구조 기반 시그널 인텔리전스**

---

## State Engine, not LLM

Decker AI는 LLM이 가격을 예측하는 서비스가 아닙니다.

시계열 데이터에서 시장 구조(Object, Swing)를 분석하고, 진행도(progress_pct)와 상태(status)를 **결정론적으로 계산**하는 엔진입니다. LLM은 그 결과를 자연어로 전달하는 인터페이스(DeckerClaw)입니다.

| 구분 | 일반 AI 트레이딩 | Decker AI |
|------|------------------|-----------|
| 시그널 생성 | LLM/ML 가격 예측 | **시장 상태 엔진** |
| 핵심 출력 | "매수/매도" | progress_pct, status, 전략 |
| LLM 역할 | 예측·판단 | **인터페이스·설명** |
| 토큰 비용 | 시그널마다 호출 | **룰북 경로 $0** |

**비용·프라이버시 라우팅**: 결정론적 경로(룰북) 우선, LLM은 정책상 필요 시에만 호출.

---

## 핵심 철학: Target → Signal → Entry

대부분의 전략은 `signal → entry` 순서입니다.

Decker AI는 **`target → signal → entry`** 순서입니다.

- 목표가 없는 진입은 유효하지 않습니다.
- 시그널 없는 움직임은 무시합니다.
- 시장은 항상 유동성을 청산하는 방향으로 움직입니다.

따라서 모든 움직임은 **수익 기회** 또는 **리버스 기회**가 됩니다.

```
Market State → Signal Touch → Target Formation
→ Entry Decision → Target Execution → Exit / Reverse
```

---

## 시그널 에이전트 harness

> **시그널 에이전트 harness** = State Engine + RULES + SKILL 내장. progress_pct·룰북 기반 판단. LLM 없이 동작 가능 (룰북 경로 $0).

---

## 에이전트 레이어 — 선택에 따른 분기

사용자가 **에이전트 모델을 선택**하면, 제공되는 아키텍처가 달라집니다.

```
[Decker 공통 백엔드]
  State Engine | RULES.yaml v1.4.0 | API
        │
        ├── [선택 A: 자체 에이전트 모델]
        │     intent_engine → Telegram @deckerclawbot / Web
        │     (호스팅, LLM $0)
        │
        ├── [선택 B: OpenClaw 협업]
        │     사용자 OpenClaw + Decker 스킬 → web_fetch → API
        │     (Slack 제한 시 Telegram 우선, Discord 등 — OpenClaw 생태계)
        │
        ├── [선택 C: API 직접]
        │     REST API 호출
        │
        └── [선택 D: 턴키]
              Railway 원클릭 → 경량 Telegram 봇 (turnkey/) → API
```

Decker는 OpenClaw 생태계에 스킬로 참여합니다. OpenClaw 사용자는 Decker 스킬을 추가해 시그널·전략을 연동할 수 있습니다.

---

## 파이프라인

```
시계열 데이터
    → [라벨링 알고리즘] → 오브젝트 평가, 라벨 (S, T, 1)
    → [State Engine] → progress_pct, status
    → [오퍼레이션 룰북] → 전략 (RULES.yaml 첫 매칭)
    → Web / Telegram(자체) / OpenClaw 스킬 / API
```

```
┌─────────────┐     ┌─────────────────┐
│ Market Data │     │  Signal Source  │
│  (시세)     │     │  (시그널 소스)   │
└──────┬──────┘     └────────┬────────┘
       │                     │
       └──────────┬──────────┘
                  │
        ┌─────────▼──────────┐
        │  Labeling Algorithm│   오브젝트 평가, 스윙 분석
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────┐
        │    State Engine    │   progress_pct, status
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────┐
        │   Signal Engine    │   시그널·상태 통합
        └─────────┬──────────┘
                  │
     ┌────────────┼────────────┐
     │            │            │
     ▼            ▼            ▼
┌─────────┐ ┌─────────────┐ ┌──────────┐
│  User   │ │  Operation  │ │   LLM    │
│ Context │ │   Rules     │ │ Reasoner │
└────┬────┘ └──────┬──────┘ └────┬─────┘
     │             │              │
     └──────┬──────┘              │
            │                     │
     ┌──────▼────────┐            │
     │   전략 반환    │◄───────────┘
     └──────┬────────┘
            │
 ┌──────────▼─────────────────────────────┐
 │  Web·Telegram(자체) / OpenClaw 스킬 / API │
 └─────────────────────────────────────────┘
```

---

## 시그널 소스와 라벨링

**시그널 소스**: `judgment_signals` 테이블. REST 푸시(`POST /signals/push`), GitHub, CQS 등에서 수집된 시그널이 저장됩니다.

**라벨링 알고리즘**: 시그널 품질·생성의 **이론적 기반**입니다. 외부 시그널 제공자가 DPDP/라벨링 기반으로 생성한 시그널을 푸시할 수 있으며, Decker AI는 수신된 시그널에 대해 State Engine(progress_pct, status)을 적용합니다.

---

## 라벨링 알고리즘

시계열 데이터를 **오브젝트(대상)**로 평가하여 라벨을 부착합니다.

### 라벨

| 라벨 | 의미 |
|------|------|
| **1/2 대상 + 1/2 프라임** | 평가 대상과 평가 기준(프라임)의 조합 |
| **S** | 시그널 — 진입 조건 충족 |
| **T** | 터치 — 향후 시그널 진입점, 중첩 |

### 오브젝트와 스윙

오브젝트는 시점에 따라 멀티스윙으로 구성됩니다.

| 스윙 | 의미 |
|------|------|
| **A** | 메인스윙 — 트렌드 키 방향. 평가 대상이 현재가 위/아래에 위치할 때 방향 평가 |
| **B** | 서브스윙 — 메인스윙의 반대 방향 조정 |
| **C** | 연결스윙 — 청산·진입·리버스가 일어나는 구간 |

### 시그널 발생

- ab, ac, bb, bc 등 스윙 조합으로 계산
- 각 스윙의 **평가봉(2프라임)**을 현재가가 브레이크할 때 **시그널 발생**

상세: [라벨링 알고리즘](../concept/labeling_algorithm.md)

---

## State Engine

시그널(진입가·목표가·손절가) + 현재가 → **progress_pct**, **status**

### progress_pct 공식

- **Long**: `(current - entry) / (target - entry) × 100`
- **Short**: `(entry - current) / (entry - target) × 100`

### status 판정

| 조건 | 결과 |
|------|------|
| Long: current ≥ target | target_reached |
| Long: current ≤ stop_loss | stop_hit |
| Short: current ≤ target | target_reached |
| Short: current ≥ stop_loss | stop_hit |
| 그 외 | in_progress |

### status 의미

| status | 의미 |
|--------|------|
| in_progress | 진행 중 |
| target_reached | 목표 도달 |
| stop_hit | 손절 구간 |
| expired | 만료 |
| unknown | 미판정 |

### 차별점

기존 봇은 "상승/하락/횡보" 같은 **현재 상태**만 알려줍니다.

Decker AI는 해당 상태가 **몇 % 진행되었는지**까지 계산합니다. 이 정보가 진입/청산 타이밍 결정에 직접 사용됩니다.

---

## 오퍼레이션 룰북

progress_pct, status, timeframe, risk_appetite 조합으로 전략을 매칭합니다.

### 조건

| 조건 | 타입 | 유효값 | 예시 |
|------|------|--------|------|
| progress_min | number | 0~100 | 66 |
| status | string | in_progress, target_reached, stop_hit, expired, unknown | target_reached |
| timeframe | string | 15m, 1h, 4h, 8h, 1d, 1w | 4h |
| risk_appetite | list | low, medium, high | [low, medium] |
| weight_diff_min/max | number | 포트폴리오 비중 | — |

### 매칭 로직

- RULES.yaml 위→아래 순서로 검사
- **첫 매칭 규칙** 반환
- `state.progress_pct ≥ rule.progress_min`이면 progress_min 충족
- **룰북 경로 LLM 미사용** → AI 토큰 비용 $0

### 예시

```
BTCUSDT long, entry=96000, target=100000, current=98640
→ progress_pct = 66%
→ RULES.yaml progress_min: 66 매칭
→ "66% 진행. 30% 부분 익절 제안. 나머지는 목표까지 홀드."
```

상세: [RULES.yaml](../operation_rules/RULES.yaml)

---

## Performance

### 전략 특성

시그널 모델은 예측이 아닌 **오브젝트 스윙 평가** 기반입니다. 목표 구조가 확인된 경우에만 포지션을 열어, 랜덤 진입을 회피합니다.

- 시그널 확인 후 진입
- 사전 정의된 목표 구조
- 리버스 유동성 인식
- 멀티타임프레임 스윙 평가

### 지표 정의

| 지표 | 설명 |
|------|------|
| **win_rate** | 수익 거래 수 / 전체 거래 수 |
| **sharpe_ratio** | 수익률 평균 / 표준편차 (위험 대비 수익) |
| **max_drawdown** | 누적 수익 곡선에서 고점 대비 최대 하락폭 |
| **profit_factor** | 총 수익 / 총 손실 |

### 거래 흐름 예시

```
A state swing → T signal touched → Target defined (+7%)
→ Entry triggered → Position closed at target → Reverse opportunity evaluated
```

### 검증

- 오퍼레이션 룰북(progress 33~95%)은 백테스트·실거래 기반으로 튜닝됩니다.
- 실거래 결과는 과거 데이터·백테스트와 다를 수 있습니다.
- 시장 변동성, 슬리피지, 수수료 등이 실제 수익에 영향을 줍니다.

---

## API

| Method | Path | 용도 |
|--------|------|------|
| GET | `/signals/{symbol}/state` | progress_pct, status |
| GET | `/signals/{symbol}/strategy` | 오퍼레이션 룰북 전략 |
| GET | `/judgment/signals/public` | 시그널 (entry, target, stop) |
| GET | `/judgment/coverage` | 20종목×6시간대 현황 |
| GET | `/market/prices` | 실시간 시세 |
| POST | `/signals/push` | 시그널 등록 |

상세: [API Guide](api-guide.md)

---

## 서비스 개요

```
[진입점 — 선택에 따라]
  • 선택 A (자체): 웹 decker-ai.com, Telegram @deckerclawbot
  • 선택 B (OpenClaw): Slack (제한 시 Telegram)·Discord — 사용자 OpenClaw + Decker 스킬
  • 선택 C (API): REST 직접 호출
        │
        ▼
[Backend] api.decker-ai.com (Railway, FastAPI)
        │
        ├── /signals/{symbol}/state    → build_signal_state
        ├── /signals/{symbol}/strategy → reason_signal_state
        ├── /judgment/signals/public
        └── /assistant/message         → chat_system_orchestrator
        │
        ▼
[PostgreSQL] judgment_signals, market_data, ...
```

---

## Phase 4: The Sequence Engine (Context Engine)

The Sequence Engine extends the base architecture with contextual state awareness:

```
Raw OHLCV
    ↓  Sequence Labeler (MODE_SEQ_V2)
       Each candle: role (anchor/test/signal/connector) + direction + quality score
    ↓  5-State Machine
       INIT → C_SET → B_FORMING → B_SET → W_PENDING
       Tracks: main swing + sub-swing (counter-narrative) + connector phase
    ↓  Operation Gate
       GO · WATCH · HOLD  (three operational modes, not binary)
    ↓  RULES Engine (9 layers, YAML, version-controlled)
       First matching rule → strategy text + ranked action choices
    ↓  AI Consultation (translator, not decision-maker)
       Natural language explanation of the structural state
```

**Key properties:**
- **Deterministic**: Same candle input → same state output. Always.
- **Auditable**: Every signal carries a trace ID linking it to the exact engine version and state that produced it.
- **Three-lane tracking**: Main swing + sub-swing (counter-narrative) + connector phase tracked simultaneously.
- **Ternary gate**: `GO` / `WATCH` / `HOLD` — because "no signal" and "structurally blocked" are different situations.

Full concept: [The Sequence Engine](../concept/sequence_engine.md)  
Deep-dive articles: [Article Series Part 2](medium/part2/README.md)

---

## 참고 / References

- [Sequence Engine concept](../concept/sequence_engine.md) — Sequence labeling, state machine, GO/WATCH/HOLD gate *(new)*
- [Signal LLM 개념](../concept/signal_llm_concept.md) — State Engine vs LLM
- [시장 상태 이론](../concept/market_state_theory.md) — progress_pct 개념
- [라벨링 알고리즘](../concept/labeling_algorithm.md) — 오브젝트·스윙·시그널
- [모델·알고리즘·성과](model.md) — 알고리즘 스토리, 구조, 성과
- [오퍼레이션 룰북](../operation_rules/RULES.yaml) — 35개+ 규칙
- [시그널 예시](../examples/signal_example.md) — progress_pct 계산 예시
