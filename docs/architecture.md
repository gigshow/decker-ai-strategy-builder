# Decker Architecture

---

## 서비스 뒷단 구조

"비트코인 시그널 알려줘", "이 시그널 지금 어떻게 할까?" — 말만 하면 응답이 오는 이유는 **뒷단에 아래 구조**가 있기 때문입니다.

시세와 시그널이 모여 → 진행도(상태)로 계산되고 → 오퍼레이션 룰북이 매칭되어 → 전략이 나옵니다. **AI 서비스가 이렇게 동작**합니다.

---

## 핵심 파이프라인

```
┌─────────────┐     ┌─────────────────┐
│ Market Data │     │  Signal Source  │
│  (시세)     │     │  (시그널 소스)   │
└──────┬──────┘     └────────┬────────┘
       │                     │
       └──────────┬──────────┘
                  │
           ┌──────▼──────┐
           │ Label Engine│
           └──────┬──────┘
                  │
           ┌──────▼──────┐
           │ State Engine│   progress_pct, status
           └──────┬──────┘
                  │
           ┌──────▼──────┐
           │Signal Engine│
           └──────┬──────┘
                  │
     ┌────────────┼────────────┐
     │            │            │
     ▼            ▼            │
┌─────────┐ ┌─────────────┐    │
│  User   │ │  Operation  │    │
│ Context │ │   Rules     │    │  RULES.yaml
└────┬────┘ └──────┬──────┘    │
     │             │            │
     └──────┬──────┘            │
            │                   │
     ┌──────▼────────┐          │
     │ LLM Reasoner  │◄─────────┘
     └──────┬────────┘
            │
 ┌──────────▼─────────────┐
 │  Web / Telegram / API  │
 └────────────────────────┘
```

### 단계별 설명

| 단계 | 역할 |
|------|------|
| **Market Data** | 실시간 시세 (현재가) |
| **Signal Source** | 시그널 (진입가·목표가·손절가, 20종목×6시간대) |
| **Label Engine** | REST 단 — 라벨된 시그널 데이터 |
| **State Engine** | 입력: 시그널 + 현재가. 출력: progress_pct, status. API: /api/v1/signals/{symbol}/state |
| **Signal Engine** | REST 단 — 시그널·상태 통합 |
| **User Context + Operation Rules** | 사용자 설정(리스크·시간대) + RULES.yaml 17개 규칙 |
| **LLM Reasoner** | 규칙 매칭 → 전략 생성 (룰북 경로는 LLM 미사용) |
| **Web / Telegram / API** | 사용자에게 전달 |

---

## 개요

```
[진입점]
  • 웹: decker-ai.com (Vercel)
  • Telegram: @deckerclawbot
  • Slack: @deckerclaw
        │
        ▼
[Backend] api.decker-ai.com (Railway, FastAPI)
        │
        ├── /assistant/message     → chat_system_orchestrator
        ├── /signals/{symbol}/state → build_signal_state
        ├── /signals/{symbol}/strategy → reason_signal_state (오퍼레이션 룰북)
        ├── /judgment/signals/public
        └── ...
        │
        ▼
[PostgreSQL] judgment_signals, market_data, ...
```

---

## 시그널 → 전략 흐름

```
1. judgment_signals + current_price
        ↓
2. build_signal_state → progress_pct, status
        ↓
3. (state, user_context) → operation_rules_loader
        ↓
4. RULES.yaml 첫 매칭 규칙 → strategy 반환
        ↓
5. LLM 미사용 → 룰북 경로 AI 토큰 $0
```

---

## 오퍼레이션 룰북 조건

| 조건 | 타입 | 유효값 | 예시 |
|------|------|--------|------|
| progress_min | number | 0~100 | 66 |
| status | string | in_progress, target_reached, stop_hit, expired, unknown | target_reached |
| timeframe | string | 15m, 1h, 4h, 8h, 1d, 1w | 4h |
| risk_appetite | list | low, medium, high | [low, medium] |
| weight_diff_min/max | number | 포트폴리오 비중 | — |

**규칙 매칭**: RULES.yaml 위→아래 순서로 검사. **첫 매칭 규칙** 반환. `state.progress_pct ≥ rule.progress_min`이면 progress_min 조건 충족.

**status 의미**: `in_progress`=진행 중, `target_reached`=목표 도달, `stop_hit`=손절 구간, `expired`=만료, `unknown`=미판정.

---

## progress_pct 계산

시그널(진입·목표·손절) + 현재가 → progress_pct. long일 때 `(current - entry) / (target - entry) * 100`. short일 때 `(entry - current) / (entry - target) * 100`. State Engine이 build_signal_state로 계산.

---

## 오퍼레이션 룰북 핵심 개념

오퍼레이션 룰북은 "진행 단계"가 아니라 **상태·시간프레임·현재가격에 따라 행동이 달라진다**는 개념이 우선입니다. status, timeframe, current_price(→progress_pct) 등 조건이 조합되면 그에 맞는 전략(행동)이 매칭됩니다.

---

## 참고

- **Label·State** — REST API가 제공하는 정보 (라벨된 시그널, progress_pct, status)
- `operation_rules/RULES.yaml` — 규칙 정의
- `operation_rules/PATCHNOTES.md` — 버전별 변경
- **학술 트렌드** — 아키텍처는 LLM Agent + 시장 상태 기반 연구(TradingAgents arXiv 2412.20138, LLM Quant Strategy 등)와 방향을 같이 합니다.
