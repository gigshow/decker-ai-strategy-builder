<!--
  Keywords: AI trading, crypto signal, Bitcoin, Ethereum, futures, stocks, equity,
  Telegram bot, trading API, market state engine, progress_pct, algorithmic trading,
  cryptocurrency, trading bot, 해외선물, 주식
-->
<div align="center">

<img src="assets/decker_claw_mascot_v1.png" width="80" alt="DeckerClaw" />

# Decker AI Strategy Builder

**A deterministic signal lifecycle engine for crypto, futures, and stocks.**  
*Measure progress. Apply rules. No prediction.*

*AI trading · crypto · futures · stocks · Bitcoin · Ethereum · Telegram bot · API*

[![GitHub Stars](https://img.shields.io/github/stars/gigshow/decker-ai-strategy-builder?style=flat-square&color=DAA520)](https://github.com/gigshow/decker-ai-strategy-builder/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/gigshow/decker-ai-strategy-builder?style=flat-square)](https://github.com/gigshow/decker-ai-strategy-builder/network)
[![월 성과](https://img.shields.io/badge/월성과_횡보장-20~30%25-brightgreen?style=flat-square)](docs/signal-performance.md)
[![Telegram](https://img.shields.io/badge/Telegram-DeckerClaw-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://t.me/deckerclawbot)
[![API Docs](https://img.shields.io/badge/API-Docs-00C853?style=flat-square)](https://api.decker-ai.com/docs)
[![Website](https://img.shields.io/badge/Website-decker--ai.com-6C47FF?style=flat-square)](https://decker-ai.com)

[🌐 Website](https://decker-ai.com) · [🤖 Telegram (DeckerClaw)](https://t.me/deckerclawbot) · [📖 API Docs](https://api.decker-ai.com/docs) · [🚀 Quick Start](docs/quickstart.md) · [📊 Signal Performance](docs/signal-performance.md) · [🛡 Risk Management](docs/risk-management.md) · [🗺 Roadmap](docs/roadmap.md)

</div>

---

## ⚡ Try It Now

| Time | Path | What |
|------|------|------|
| **30 sec** | API | `curl -s "https://api.decker-ai.com/api/v1/signals/BTCUSDT/state"` |
| **3 min** | Samples | `./samples/signal-push-strategy.sh BTCUSDT 96000 100000 92000` |
| **5 min** | Telegram | [@deckerclawbot](https://t.me/deckerclawbot) — "비트코인 시그널 알려줘" |
| **5 min** | 턴키 | [turnkey/](turnkey/) — Railway 원클릭 경량 봇 (자체 배포) |

**Decker AI Strategy Builder**는 시그널의 **진행도(progress_pct)**를 계산하고, YAML 룰북으로 전략을 반환합니다. LLM 없이 동작합니다.

> **DeckerClaw** — Decker 자체 에이전트 + OpenClaw 스킬 생태계. DeckerClaw를 **입양**할 수 있습니다: (A) [@deckerclawbot](https://t.me/deckerclawbot) Telegram 사용 (B) OpenClaw·Slack·ClawHub에 Decker 스킬 추가 → web_fetch → API 연동 (C) REST API 직접 호출

---

## 🎯 Overview

**Decker AI**는 가격·시간 시계열에서 시장 구조(Object, Swing)를 분석하고, **진행도(progress_pct)**와 **상태(status)**를 결정론적으로 계산하여 고정밀 거래 시그널을 생성하는 **AI 마켓 스테이트 엔진**입니다. **Harness 목표**: AI 시장 이해 + 사용자 상의 + 최적 실행 (시장=게임).

> **You say:** "비트코인 시그널 알려줘" / "이 시그널 지금 어떻게 할까?" / "ETH 0.01 매수해줘"
>
> **DeckerClaw returns:** 시그널·진행도(progress_pct)·전략·주문 실행 — 말만 하면

LLM은 가격을 예측하지 않습니다. Decker AI는 시장 구조를 **계산**합니다.

---

## 🎯 State Engine, not LLM

| 구분 | 일반 AI 트레이딩 | Decker AI |
|------|------------------|-----------|
| 시그널 생성 | LLM/ML 가격 예측 | **시장 상태 엔진** |
| 핵심 출력 | "매수/매도" | progress_pct, status, 전략 |
| LLM 역할 | 예측·판단 | **인터페이스·설명** |
| 토큰 비용 | 시그널마다 호출 | **룰북 경로 $0** |

---

## 📌 3 Scenarios

| Scenario | Decker AI Strategy Builder |
|----------|----------------------------|
| **Range-bound** | progress_pct가 각 스윙을 독립 추적. 횡보장에서도 20~30% 월 성과 |
| **Trend** | 목표 도달 속도 ↑, Win Rate 70%+ |
| **Reversal** | Target-first 철학. 실패한 롱 = 다음 숏 시그널 정보 |

---

## 🔄 How It Works

사용자의 한 마디가 처리되는 5단계:

1. **You say** — "비트코인 시그널 알려줘"
2. **Signal fetch** — judgment_signals + 실시간 현재가 조회
3. **State Engine** — progress_pct, status 결정론적 계산
4. **Operation Rules** — RULES.yaml 매칭 → 전략 반환 (LLM 없이)
5. **You get** — "66% 진행. 30% 부분 익절 제안. 나머지는 목표까지 홀드." (DeckerClaw가 자연어로 전달)

---

## 💡 Core Philosophy: Target → Signal → Entry

대부분의 전략은 `signal → entry` 순서로, **목표 없이 진입**합니다.

Decker AI는 **`target → signal → entry`** 순서입니다.

| 원칙 | 설명 |
|------|------|
| **Entry without target → invalid** | 목표 구조가 먼저 확인되어야 진입이 유효 |
| **Movement without signal → ignored** | 시그널 없는 움직임은 노이즈 |
| **Market clears liquidity** | 시장은 항상 유동성을 청산하는 방향으로 이동 |

> 목표가 없이 움직이면 → 반대로 찬스  
> 물렸거나 수익이면 → 반대 청산 기회  
> **모든 움직임은 profit opportunity 또는 reverse opportunity**

---

## 📐 What is progress_pct?

시그널은 생성(0%)부터 목표 도달(100%)까지 **수명 주기**를 가집니다. Decker AI는 이 진행도를 실시간으로 계산합니다.

**공식:**

- Long: `(현재가 - 진입가) / (목표가 - 진입가) × 100`
- Short: `(진입가 - 현재가) / (진입가 - 목표가) × 100`

| progress_pct | 의미 | 전략 |
|--------------|------|------|
| 0–32% | 시그널 초기 | 관망 또는 진입 준비 |
| 33–66% | 시그널 활성 | 진입 적기, 리스크 관리 시작 |
| 67–89% | 시그널 후반 | 부분 익절, 포지션 축소 |
| 90–100% | 목표 직전 | 청산 준비 |

> 경쟁사 시그널: **BUY / SELL** 이진값만 제공  
> Decker AI: **BUY + progress 67%** = "기회는 있지만 타이밍 주의"

상세: [시장 상태 이론](concept/market_state_theory.md) · [Architecture](docs/architecture.md)

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

*출처: 오퍼레이션 룰북(progress 33~95%) 기반 백테스트·실거래 튜닝. 과거 성과가 미래 수익을 보장하지 않습니다.*

상세: [모델·알고리즘·성과](docs/model.md)

---

## 🤝 DeckerClaw — 선택 기반 에이전트

에이전트 모델을 **선택**하면, 제공되는 아키텍처가 달라집니다.

| 선택 | 사용자 | 채널 | 설명 |
|------|--------|------|------|
| **A. 자체 에이전트** | 일반 사용자·비개발자 | Telegram @deckerclawbot, Web | Decker **자체 에이전트** (LLM $0) |
| **B. OpenClaw 협업** | OpenClaw 개발자 | Slack (제한 시 Telegram)·Discord 등 | 자신의 OpenClaw에 **Decker 스킬 추가** → web_fetch → API |
| **C. API 직접** | 개발자 | REST API | API 직접 연동 |
| **D. 턴키** | OpenClaw 미사용자 | Railway 원클릭 | [turnkey/](turnkey/) — 경량 Telegram 봇 (시그널·전략 조회) |

Decker는 OpenClaw 생태계에 스킬로 참여합니다. OpenClaw 사용자는 Decker 스킬을 추가해 시그널·전략을 연동할 수 있습니다.

**선택 B 흐름:**
```
개발자 OpenClaw → Decker SKILL.md 트리거 → web_fetch → Decker API → Claude 자연어 응답
```

---

## 🏗 Architecture

```
시계열 데이터
    → [라벨링 알고리즘] → 오브젝트 평가, 라벨 (S, T, 1)
    → [State Engine]    → progress_pct, status
    → [오퍼레이션 룰북] → 전략 (RULES.yaml v1.4.0)
    → Web / Telegram(Way 1) / OpenClaw 스킬(Way 2) / API(Way 3)
```

| 모듈 | 역할 |
|------|------|
| **Labeling Algorithm** | 시계열 → 오브젝트(대상) 평가, 스윙(A/B/C) 분석 |
| **State Engine** | 시그널 + 현재가 → progress_pct, status |
| **Operation Rules** | RULES.yaml 룰북 매칭 → 전략 반환 |
| **LLM Reasoner** | 결과를 자연어로 설명 (선택) |

상세: [Architecture](docs/architecture.md)

---

## 🚀 Quick Start

| Time | Path | Command / Action |
|------|------|------------------|
| **30 sec** | API | `curl -s "https://api.decker-ai.com/api/v1/signals/BTCUSDT/state"` |
| **3 min** | Samples | `./samples/signal-push-strategy.sh BTCUSDT 96000 100000 92000` |
| **10 min** | Telegram | [decker-ai.com](https://decker-ai.com) 가입 → [DeckerClaw](https://t.me/deckerclawbot) 연동 → "비트코인 시그널 알려줘" |

**Telegram (DeckerClaw):**

1. [decker-ai.com](https://decker-ai.com) 회원가입 (무료)
2. [decker-link-telegram](https://decker-ai.com/decker-link-telegram)에서 코드 발급 → [@deckerclawbot](https://t.me/deckerclawbot)에 `/start {코드}`
3. "비트코인 시그널 알려줘", "포지션 보여줘", "ETH 0.01 매수해줘" — **말만 하면** 됩니다.

**[🤖 DeckerClaw 체험하기](https://t.me/deckerclawbot)**

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
| [Operation Rules](operation_rules/RULES.yaml) | 오퍼레이션 룰북 |
| [Brand Guide](docs/BRAND_GUIDE.md) | 네이밍·표현 규칙 |
| [Signal LLM 개념](concept/signal_llm_concept.md) | State Engine, 시장 상태, 라벨링 |
| [시장 상태 이론](concept/market_state_theory.md) | progress_pct 개념 |
| [라벨링 알고리즘](concept/labeling_algorithm.md) | 오브젝트·스윙·시그널 발생 |
| [시그널 예시](examples/signal_example.md) | 시그널→state→strategy 예시 |
| [Samples](samples/README.md) | API 연동 예제 (개발자용) |
| [Article Series (1~10)](docs/medium/README.md) | Medium 연재 아티클 (State Engine, progress_pct, YAML, API, Multi-TF, Rulebook) |

---

## 🏆 Achievements & Roadmap

| 상태 | Phase | 내용 |
|------|-------|------|
| ✅ | **Phase 2** | Slack 연동 (OpenClaw 스킬, Way 2), /decker-link — *Slack: 워크스페이스 제한 이슈로 일시 비활성 가능. Telegram 권장* |
| ✅ | **Phase 3** | 주문 승인 플로우 — "BTC 0.01 매수해줘 → 승인 → 실행" |
| ✅ | **Phase 4** | 좋은 시그널 알림, 프로액티브 투자 비서 |
| ✅ | **Phase 5** | 사용자 여정, member_joined 환영 |
| ✅ | **오퍼레이션** | RULES.yaml v1.4.0, progress·market_state 룰북 |
| ✅ | **에이전트** | Telegram 자체(선택 A) + OpenClaw 스킬(선택 B) + 턴키(선택 D), HL·PM 주문 |
| ✅ | **턴키** | turnkey/ Railway 원클릭 경량 봇 |
| ✅ | **시그널 LLM v3.0** | rationale·choices·tf_alignment·entry_timing (`/llm/opportunities`, `/consultation`) |
| ✅ | **시그널 엔진 + LLM 통합** | State Engine + Signal LLM = 통합 서비스 (Telegram + API + 스킬) |
| 🔜 | **백테스트** | progress 구간별 수익률 검증·리포트 공개 |

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
