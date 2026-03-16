# Risk Management Design

**자동주문·주문 실행 시 리스크 제어 설계.**  
Ref: risk_management.py, auto_order_signal_processor, strategy_builder_user_settings

---

## 1. 포지션 한도

| 세이프가드 | 기본값 | 설명 |
|------------|--------|------|
| **1회 최대 포지션** | 계좌의 5% | `max_position_risk`: 0.05. 단일 주문 시 포트폴리오 대비 상한 |
| **동시 포지션 수** | 5개 | `max_concurrent_positions`. 초과 시 신규 진입 차단 |
| **포트폴리오 리스크** | 10% | `max_portfolio_risk`: 0.1. 총 노출 상한 |

---

## 2. 일일 한도

| 세이프가드 | 기본값 | 설명 |
|------------|--------|------|
| **일일 거래 수** | 10건 | `max_daily_trades`. 초과 시 당일 신규 주문 차단 |
| **최대 드로우다운** | 20% | `max_drawdown`: 0.2. 초기 자본 대비 손실 상한 (모니터링) |

---

## 3. 자동주문 세이프가드

| 항목 | 설정 | 설명 |
|------|------|------|
| **쿨다운** | 1시간 | `AUTO_ORDER_COOLDOWN_HOURS`. 동일 user+symbol 재진입 간격 |
| **최소 신뢰도** | auto_order_rules 설정 | `min_confidence` 미만 시그널 무시 |
| **progress 구간** | (설계) | progress &lt; 33 또는 &gt; 90 구간 자동주문 차단 권장 |

---

## 4. 비상 정지

| 방법 | 설명 |
|------|------|
| **자동주문 비활성화** | 대시보드 또는 Telegram에서 자동주문 규칙 비활성화 |
| **/stop (설계)** | Telegram "/stop" 명령어로 전체 자동주문 즉시 중단 (구현 예정) |

---

## 5. 사용자 리스크 설정

`strategy_builder_user_settings` 또는 `user_settings`에서 조정 가능:

- `risk_appetite`: low / medium / high — RULES.yaml 매칭에 사용
- `max_position_risk`, `max_daily_trades` 등 — 위 기본값 오버라이드
