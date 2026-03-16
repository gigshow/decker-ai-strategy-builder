# Decker AI Strategy Builder

> **DECKER: 디지털 자산 시장을 지능적으로 해석하는 AI 마켓 스테이트 엔진.**  
> 시그널·진행도(progress_pct) 기반 전략. Telegram에서 말만 하면 시그널·포지션·주문.

[Website](https://decker-ai.com) · [Telegram](https://t.me/deckerclawbot) · [API Docs](https://api.decker-ai.com/docs) · [Quick Start](docs/quickstart.md) · [Roadmap](docs/roadmap.md)

---

## Signal LLM 정의

DECKER does not use traditional ML prediction for signals.

Instead it uses:

- **Price** (진입가·목표가·손절가·현재가)
- **Time** (시간프레임)
- **Market structure** (시그널 → 진행도 → 상태)

to build a deterministic market state engine.

The LLM layer is used to interpret market state signals into actionable strategies.

> AI 트레이딩 = LLM 예측 ❌ / 시장 상태 엔진 + LLM 인터페이스 ✅

---

## Story

**"시장은 게임이다. 오르면 매도, 내리면 매수 — 그 수를 AI가 둔다."**

바둑에서 사람이 AI를 이길 수 없듯, **트레이딩도 사람이 기계를 이길 수 없습니다.** 좋은 AI 모델을 선택하는 것이 중요합니다.

| 기존 시도 | 한계 |
|-----------|------|
| 수식으로 시장 상태 구현 | 게임 룰은 수식으로 만들기 어려움 |
| AI 없이 규칙 기반 | 시장 심리·상태 전이 포착 불가 |

| Decker 접근 | 가능성 |
|-------------|--------|
| 시장 상태를 AI에게 알려주고 | 상태 데이터 기반 예측 |
| 외부 시그널로 시장 라벨화 | 어떤 종목이 찬스인지 |
| 사용자와 상의 (리스크·리워드) | 투자전문가처럼 상담 |
| **알파고처럼** 마켓 플레이 | 최적의 매수·매도 포인트 |

---

## Why Now

- **에이전트 시대**: Telegram·Slack에서 "말만 하면" 시그널·포지션·주문
- **시그널 상태 차별화**: 진행도(progress_pct)·status — 경쟁사 없음
- **AI 시그널 모델**: 시계열 데이터 기반 시장상태 학습 → 정제된 데이터 제공 → 시그널 LLM 로드맵

---

## Quick Start (3단계)

1. **가입** — [decker-ai.com](https://decker-ai.com) 회원가입 (무료)
2. **연동** — [decker-link-telegram](https://decker-ai.com/decker-link-telegram)에서 코드 발급 → [@deckerclawbot](https://t.me/deckerclawbot)에 `/start {코드}`
3. **사용** — "비트코인 시그널 알려줘", "포지션 보여줘", "ETH 0.01 매수해줘" 등 **말만 하면** 됩니다.

---

## Achievements

| Phase | 내용 |
|-------|------|
| **Phase 2** | Slack 연동, /decker-link — "Slack에서 말만 하면" |
| **Phase 3** | 주문 승인 플로우 — "BTC 0.01 매수해줘 → 승인 → 실행" |
| **Phase 4** | 좋은 시그널 알림, 시그널 제안 → "응" → order — "프로액티브 투자 비서" |
| **Phase 5** | 사용자 여정, member_joined 환영 |
| **오퍼레이션** | RULES.yaml v1.3.0, progress 33~95 규칙 — 진행도 기반 전략 |
| **에이전트** | Telegram·Slack, HL·Polymarket — "말만 하면 HL·PM 주문" |

---

## Features

- **시그널·진행도 기반 전략**: 덱커가 시그널과 전략을 하나로 제공. 오퍼레이션 룰북 (progress 33~95%, timeframe, risk) — [RULES.yaml](operation_rules/RULES.yaml) 17개 규칙 공개
- **에이전트**: Telegram @deckerclawbot — 시그널, 포지션, 주문, 자동주문, 뉴스
- **API**: 시그널, 전략, 시세, 시장 상태 (공개 엔드포인트)
- **로드맵**: AI 시그널 모델 → 시그널 LLM 토큰 베이스 서비스

---

## Architecture

"말만 하면" 응답이 오는 이유 — **서비스 뒷단 구조**

```
Market Data + Signal Source → Label Engine → State Engine → Signal Engine
       → (User Context + Operation Rules) → LLM Reasoner → Web/Telegram/API
```

시세·시그널 → 진행도 계산 → 오퍼레이션 룰북 매칭 → 전략. [상세](docs/architecture.md)

```
[웹] decker-ai.com
[Telegram] @deckerclawbot
[Slack] @deckerclaw
        │
        ▼
┌─────────────────────────────────────┐
│  Decker (api.decker-ai.com)         │
│  시그널·시세·전략 — 하나로 제공        │
│  • /signals/{symbol}/state           │
│  • /signals/{symbol}/strategy        │
│  • /judgment/signals/public          │
│  • /assistant/message                │
└─────────────────────────────────────┘
        │
        ▼
[오퍼레이션 룰북] RULES.yaml → progress_min, timeframe, risk_appetite (17개 규칙)
```

---

## Docs

| 문서 | 용도 |
|------|------|
| [Quick Start](docs/quickstart.md) | 3단계 가이드, 체험 시나리오 |
| [모델·알고리즘·성과](docs/model.md) | 심층: 알고리즘 스토리, 구조, 성과 |
| [Architecture](docs/architecture.md) | 파이프라인·모듈 |
| [API Guide](docs/api-guide.md) | 공개 API (개발자·연동용) |
| [Roadmap](docs/roadmap.md) | 로드맵 |
| [Operation Rules](operation_rules/RULES.yaml) | 오퍼레이션 룰북 (17개 규칙, 진행도 기반) |
| [Concept](concept/signal_llm_concept.md) | Signal LLM, 시장 상태, 라벨링 알고리즘 |
| [Examples](examples/signal_example.md) | 시그널→state→strategy 예시 |
| [Samples](samples/README.md) | API 연동 예제 (개발자용) |

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
> **서비스 사용자**: 덱커가 시그널·시세·전략을 하나로 제공합니다. 가입·연동 후 Telegram·웹에서 바로 사용 가능.
>
> **사용 가능한 것**: API 호출 (api.decker-ai.com), samples/signal-push-strategy.sh 실행, RULES.yaml 참조, docs/architecture.md 아키텍처 이해.
