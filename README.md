<div align="center">

# DECKER — AI Market State Engine

**디지털 자산 시장 구조를 읽고, 시그널·진행도·전략을 하나로.**  
*Signal Intelligence Engine for Digital Assets — not prediction, but state.*

[![GitHub Stars](https://img.shields.io/github/stars/gigshow/decker-ai-strategy-builder?style=flat-square&color=DAA520)](https://github.com/gigshow/decker-ai-strategy-builder/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/gigshow/decker-ai-strategy-builder?style=flat-square)](https://github.com/gigshow/decker-ai-strategy-builder/network)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://t.me/deckerclawbot)
[![API Docs](https://img.shields.io/badge/API-Docs-00C853?style=flat-square)](https://api.decker-ai.com/docs)
[![Website](https://img.shields.io/badge/Website-decker--ai.com-6C47FF?style=flat-square)](https://decker-ai.com)

[🌐 Website](https://decker-ai.com) · [🤖 Telegram Bot](https://t.me/deckerclawbot) · [📖 API Docs](https://api.decker-ai.com/docs) · [🚀 Quick Start](docs/quickstart.md) · [🗺 Roadmap](docs/roadmap.md)

</div>

---

## ⚡ Overview

**DECKER**는 가격·시간 시계열에서 시장 구조(Object, Swing)를 분석하고, **진행도(progress_pct)**와 **상태(status)**를 결정론적으로 계산하여 고정밀 거래 시그널을 생성하는 **AI 마켓 스테이트 엔진**입니다.

> **You say:** "비트코인 시그널 알려줘" / "이 시그널 지금 어떻게 할까?" / "ETH 0.01 매수해줘"
>
> **DECKER returns:** 시그널·진행도(progress_pct)·전략·주문 실행 — 말만 하면

LLM은 가격을 예측하지 않습니다. DECKER는 시장 구조를 **계산**합니다.

---

## 🎯 State Engine, not LLM

| 구분 | 일반 AI 트레이딩 | DECKER |
|------|------------------|--------|
| 시그널 생성 | LLM/ML 가격 예측 | **시장 상태 엔진** |
| 핵심 출력 | "매수/매도" | progress_pct, status, 전략 |
| LLM 역할 | 예측·판단 | **인터페이스·설명** |
| 토큰 비용 | 시그널마다 호출 | **룰북 경로 $0** |

---

## 🔄 How It Works

사용자의 한 마디가 처리되는 5단계:

1. **You say** — "비트코인 시그널 알려줘"
2. **Signal fetch** — judgment_signals + 실시간 현재가 조회
3. **State Engine** — progress_pct, status 결정론적 계산
4. **Operation Rules** — RULES.yaml 매칭 → 전략 반환 (LLM 없이)
5. **You get** — "66% 진행. 30% 부분 익절 제안. 나머지는 목표까지 홀드."

---

## 💡 Core Philosophy: Target → Signal → Entry

대부분의 전략은 `signal → entry` 순서로, **목표 없이 진입**합니다.

DECKER는 **`target → signal → entry`** 순서입니다.

| 원칙 | 설명 |
|------|------|
| **Entry without target → invalid** | 목표 구조가 먼저 확인되어야 진입이 유효 |
| **Movement without signal → ignored** | 시그널 없는 움직임은 노이즈 |
| **Market clears liquidity** | 시장은 항상 유동성을 청산하는 방향으로 이동 |

> 목표가 없이 움직이면 → 반대로 찬스  
> 물렸거나 수익이면 → 반대 청산 기회  
> **모든 움직임은 profit opportunity 또는 reverse opportunity**

---

## 📊 Performance

시그널 모델은 예측이 아닌 **오브젝트 스윙 평가** 기반입니다.

| Metric | Result |
|--------|--------|
| **Win Rate** | 61–68% |
| **Avg Profit** | 5–12% |
| **Max Drawdown** | < 9% |
| **Signal Frequency** | 1–3 / day |
| **Avg Holding Time** | 4h – 2d |

```
A state swing → T signal touched → Target defined (+7%)
→ Entry triggered → Position closed at target
→ Reverse opportunity evaluated
```

상세: [모델·알고리즘·성과](docs/model.md)

---

## 🏗 Architecture

```
시계열 데이터
    → [라벨링 알고리즘] → 오브젝트 평가, 라벨 (S, T, 1)
    → [State Engine]    → progress_pct, status
    → [오퍼레이션 룰북] → 전략 (RULES.yaml)
    → Web / Telegram / API
```

| 모듈 | 역할 |
|------|------|
| **Labeling Algorithm** | 시계열 → 오브젝트(대상) 평가, 스윙(A/B/C) 분석 |
| **State Engine** | 시그널 + 현재가 → progress_pct, status |
| **Operation Rules** | RULES.yaml 17개 규칙 매칭 → 전략 반환 |
| **LLM Reasoner** | 결과를 자연어로 설명 (선택) |

상세: [Architecture](docs/architecture.md)

---

## 🚀 Quick Start

| 필요한 것 | 설명 |
|-----------|------|
| 계정 | [decker-ai.com](https://decker-ai.com) 무료 가입 |
| Telegram | [@deckerclawbot](https://t.me/deckerclawbot) |

**3단계로 시작:**

1. **가입** — [decker-ai.com](https://decker-ai.com) 회원가입 (무료)
2. **연동** — [decker-link-telegram](https://decker-ai.com/decker-link-telegram)에서 코드 발급 → [@deckerclawbot](https://t.me/deckerclawbot)에 `/start {코드}`
3. **사용** — "비트코인 시그널 알려줘", "포지션 보여줘", "ETH 0.01 매수해줘" 등 **말만 하면** 됩니다.

**[🤖 지금 Telegram에서 체험하기](https://t.me/deckerclawbot)**

---

## 📚 Docs

| 문서 | 용도 |
|------|------|
| [Quick Start](docs/quickstart.md) | 3단계 가이드, 체험 시나리오 |
| [Architecture](docs/architecture.md) | 파이프라인·모듈·State Engine |
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

## 🏆 Achievements

| Phase | 내용 |
|-------|------|
| **Phase 2** | Slack 연동 — "Slack에서 말만 하면" |
| **Phase 3** | 주문 승인 플로우 — "BTC 0.01 매수해줘 → 승인 → 실행" |
| **Phase 4** | 좋은 시그널 알림, 프로액티브 투자 비서 |
| **Phase 5** | 사용자 여정, member_joined 환영 |
| **오퍼레이션** | RULES.yaml v1.3.0, progress 33~95 규칙 |
| **에이전트** | Telegram·Slack, HL·Polymarket 주문 |

---

## 🔗 Links

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
