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
| **Label Engine** | 시장 라벨화 |
| **State Engine** | 진행도(progress_pct)·상태 계산 — "몇 % 왔는지" |
| **Signal Engine** | 시그널·상태 통합 |
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

| 조건 | 타입 | 예시 |
|------|------|------|
| progress_min | number | 66 |
| status | string | target_reached |
| timeframe | string | 4h |
| risk_appetite | list | [low, medium] |
| weight_diff_min/max | number | 포트폴리오 비중 |

---

## 참고

- `operation_rules/RULES.yaml` — 규칙 정의
- `operation_rules/PATCHNOTES.md` — 버전별 변경
