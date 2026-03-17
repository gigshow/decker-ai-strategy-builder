# Decker Roadmap

---

## 비전 (Vision)

> **시장 = 게임** — "오르면 매도, 내리면 매수" 게임 심리를 AI가 이해하고, 사용자와 상의해서 최적의 수를 실행한다.

| 단계 | 목표 | roadmap 매핑 |
|------|------|--------------|
| **1단계 (대화형)** | OpenClaw 주문 연결, 대화형 시그널·포지션·주문 | Phase 2~5, Our Story, 턴키 ✅ |
| **중기 (상의)** | 투자전문가처럼 상의 — rationale, confidence, 선택지 | R3 시그널 LLM v3.0, R4 엔진+LLM 통합 |
| **장기 (게임처럼)** | 시장 상태 이해, 최적의 수 제안 | roadmap "장기" 섹션 |

---

## 완료

| 항목 | 내용 |
|------|------|
| Phase 2 | Slack 연동, /decker-link (OpenClaw 경유) |
| Phase 3 | 주문 승인 플로우 |
| Phase 4 | 좋은 시그널 알림, 시그널 제안 → order |
| Phase 5 | 사용자 여정, member_joined 환영 |
| Our Story | 서비스 페이지 스토리 섹션 |
| 턴키 | turnkey/ 경량 Telegram 봇 (Railway 원클릭) |
| 오퍼레이션 룰북 v1.4.0 | progress 33~95, timeframe, risk_appetite, market_state |
| Telegram | @deckerclawbot, decker-link-telegram (자체 에이전트) |
| Hyperliquid·Polymarket | HL·PM 주문 |
| OpenClaw 스킬 | SKILL.md 공개, web_fetch → Decker API |

---

## 진행 중

| 항목 | 내용 |
|------|------|
| 공개 레포 | decker-ai-strategy-builder 문서·샘플 |
| 투웨이 모델 공식화 | Way 1(자체 에이전트) + Way 2(OpenClaw 스킬) 문서·온보딩 정비 |

---

## 예정

| 항목 | 내용 |
|------|------|
| 시그널 LLM v3.0 | 시그널 상태 → LLM 인사이트·설명 API (`/llm/opportunities`) |
| 시그널 엔진 + LLM 앱 통합 | State Engine + Signal LLM = 통합 서비스 (Telegram + API + 스킬) |
| Slack | 사용법 확정 전까지 보류. Telegram 위주 |
| Discord 연동 | 다음 세션 검토 (팀·커뮤니티 채널) |
| What People Say | 초기 사용자 쿼트 수집 |
| clawhub | decker 스킬 publish (후순위, 홍보·생태계 노출용) |
| API 과금·한도 적용 | API 키 발급, check_usage_limit 연동, Stripe 결제 (베타 이후) |

---

## 장기 (게임처럼)

> **시장 = 게임** — AI가 시장 상태를 이해하고, 사용자와 상의한 뒤 최적의 수를 제안·실행한다.

| 항목 | 내용 |
|------|------|
| **시장 상태 이해** | 오더북·청산·펀딩 등 → 시장 국면 파악 (trend, range, breakout 등) |
| **최적의 수 제안** | "이 국면에서 이 수가 유리하다" — 매수·매도·홀드 포인트 |
| **게임처럼 플레이** | 바둑의 수처럼 — 시장 심리 예측, 리스크·리워드 논의 후 실행 |
| **선행 조건** | R3/R4 완료, 상의 플로우 안정화 |

---

## 베타 정책 (현재)

**API·에이전트는 베타 테스트 중입니다.**

| 구분 | 베타 | 정식 출시 후 |
|------|------|--------------|
| **제공** | 시그널·전략·룰북 모델 무제한 | 동일 |
| **한도** | 미적용 | Free 500/월, Pro 10k 등 |
| **과금** | 미적용 | Stripe 구독 |
| **API 키** | 선택 (없어도 호출 가능) | 권장 (한도·과금 추적) |

상세: 메인 레포 `docs/과금_서비스_실제_준비_갭_분석_20250317.md` (공개 레포에는 미포함)
