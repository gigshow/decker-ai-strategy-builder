# DECKER — AI Market State Engine

> **가격·시간 시계열에서 시장 구조(Object, Swing)를 분석하고, 진행도(progress_pct)와 상태(status)를 계산하여 고정밀 거래 시그널을 생성하는 AI 마켓 스테이트 엔진.**

[Website](https://decker-ai.com) · [Telegram](https://t.me/deckerclawbot) · [API Docs](https://api.decker-ai.com/docs) · [Quick Start](docs/quickstart.md) · [Roadmap](docs/roadmap.md)

---

## State Engine, not LLM

DECKER는 LLM이 가격을 예측하는 서비스가 아닙니다.

시계열 데이터에서 시장 구조를 분석하고, **진행도(progress_pct)**와 **상태(status)**를 결정론적으로 계산하는 엔진입니다. LLM은 결과를 자연어로 전달하는 인터페이스입니다.

| 구분 | 일반 AI 트레이딩 | DECKER |
|------|------------------|--------|
| 시그널 생성 | LLM/ML 가격 예측 | **시장 상태 엔진** |
| 핵심 출력 | "매수/매도" | progress_pct, status, 전략 |
| LLM 역할 | 예측·판단 | **인터페이스·설명** |
| 토큰 비용 | 시그널마다 호출 | **룰북 경로 $0** |

---

## Core Philosophy: Target → Signal → Entry

대부분의 전략은 `signal → entry` 순서입니다.

DECKER는 **`target → signal → entry`** 순서입니다.

| 원칙 | 설명 |
|------|------|
| **Entry without target → invalid** | 목표가 없는 진입은 유효하지 않음 |
| **Movement without signal → ignored** | 시그널 없는 움직임은 무시 |
| **Market clears liquidity** | 시장은 항상 유동성을 청산하는 방향으로 이동 |

따라서 모든 움직임은 **수익 기회** 또는 **리버스 기회**가 됩니다.

```
Target defined → Signal confirmed → Entry triggered
→ Target executed → Exit / Reverse opportunity
```

---

## Performance

### Signal-Driven Strategy Results

시그널 모델은 예측이 아닌 **오브젝트 스윙 평가** 기반입니다. 목표 구조가 확인된 경우에만 포지션을 열어, 랜덤 진입을 회피합니다.

- Signal confirmation before entry
- Pre-defined target structure
- Reverse-liquidity awareness
- Multi-timeframe swing evaluation

### Strategy Metrics

| Metric | Result |
|--------|--------|
| Win Rate | 61–68% |
| Avg Profit | 5–12% |
| Max Drawdown | < 9% |
| Signal Frequency | 1–3 / day |
| Avg Holding Time | 4h – 2d |

### Trade Flow

```
A state swing → T signal touched → Target defined (+7%)
→ Entry triggered → Position closed at target
→ Reverse opportunity evaluated
```

상세: [모델·알고리즘·성과](docs/model.md)

---

## Architecture

```
시계열 데이터
    → [라벨링 알고리즘] → 오브젝트 평가, 라벨 (S, T, 1)
    → [State Engine] → progress_pct, status
    → [오퍼레이션 룰북] → 전략 (RULES.yaml)
    → Web / Telegram / API
```

| 모듈 | 역할 |
|------|------|
| **Labeling Algorithm** | 시계열 → 오브젝트(대상) 평가, 스윙(A/B/C) 분석 |
| **State Engine** | 시그널 + 현재가 → progress_pct, status |
| **Operation Rules** | RULES.yaml 17개 규칙 매칭 → 전략 반환 |
| **LLM Reasoner** | 결과를 자연어로 설명 (선택) |

```
┌─────────────────────────────────────┐
│  Decker (api.decker-ai.com)         │
│  시그널·시세·전략 — 하나로 제공        │
│  • /signals/{symbol}/state           │
│  • /signals/{symbol}/strategy        │
│  • /judgment/signals/public          │
│  • /assistant/message                │
└─────────────────────────────────────┘
```

상세: [Architecture](docs/architecture.md)

---

## Quick Start (3단계)

1. **가입** — [decker-ai.com](https://decker-ai.com) 회원가입 (무료)
2. **연동** — [decker-link-telegram](https://decker-ai.com/decker-link-telegram)에서 코드 발급 → [@deckerclawbot](https://t.me/deckerclawbot)에 `/start {코드}`
3. **사용** — "비트코인 시그널 알려줘", "포지션 보여줘", "ETH 0.01 매수해줘" 등 **말만 하면** 됩니다.

---

## Key Insight

> 대부분 전략은 entry → target 순서로 실패합니다.
>
> DECKER는 **target → signal → entry** 순서입니다.
>
> 모든 거래에 사전 정의된 기대값과 리스크 구조가 존재합니다.

| 상황 | 결과 |
|------|------|
| 목표가 없이 움직임 | → 반대로 찬스 |
| 물림 또는 수익 | → 반대 청산 기회 |
| 모든 움직임 | → profit opportunity 또는 reverse opportunity |

---

## Docs

| 문서 | 용도 |
|------|------|
| [Quick Start](docs/quickstart.md) | 3단계 가이드, 체험 시나리오 |
| [Architecture](docs/architecture.md) | 파이프라인·모듈·State Engine·성과 |
| [모델·알고리즘·성과](docs/model.md) | 알고리즘 스토리, 구조, 성과 지표 |
| [API Guide](docs/api-guide.md) | 공개 API (개발자·연동용) |
| [Strategy DSL](docs/strategy-dsl.md) | YAML 전략 사양 |
| [Roadmap](docs/roadmap.md) | 로드맵 |
| [Operation Rules](operation_rules/RULES.yaml) | 오퍼레이션 룰북 (17개 규칙) |
| [Signal LLM 개념](concept/signal_llm_concept.md) | State Engine, 시장 상태, 라벨링 |
| [시장 상태 이론](concept/market_state_theory.md) | progress_pct 개념 |
| [라벨링 알고리즘](concept/labeling_algorithm.md) | 오브젝트·스윙·시그널 발생 |
| [시그널 예시](examples/signal_example.md) | 시그널→state→strategy 예시 |
| [Samples](samples/README.md) | API 연동 예제 (개발자용) |

---

## Achievements

| Phase | 내용 |
|-------|------|
| **Phase 2** | Slack 연동 — "Slack에서 말만 하면" |
| **Phase 3** | 주문 승인 플로우 — "BTC 0.01 매수해줘 → 승인 → 실행" |
| **Phase 4** | 좋은 시그널 알림, 프로액티브 투자 비서 |
| **Phase 5** | 사용자 여정, member_joined 환영 |
| **오퍼레이션** | RULES.yaml v1.3.0, progress 33~95 규칙 |
| **에이전트** | Telegram·Slack, HL·Polymarket 주문 |

---

## Links

| 용도 | URL |
|------|-----|
| **서비스** | https://decker-ai.com |
| **Telegram 봇** | https://t.me/deckerclawbot |
| **Telegram 연동** | https://decker-ai.com/decker-link-telegram |
| **API 문서** | https://api.decker-ai.com/docs |

---

> ⚠️ 이 리포는 문서·샘플·커뮤니티 허브입니다. 실제 프로덕션 코드는 비공개 리포지토리에서 운영됩니다.
>
> **사용 가능한 것**: API 호출, samples/ 실행, RULES.yaml 참조, docs/ 아키텍처 이해.
