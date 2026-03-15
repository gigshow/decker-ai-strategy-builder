# Decker Architecture

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
5. LLM 미사용 → 토큰 $0
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
