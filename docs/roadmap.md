# Decker Roadmap

---

## Vision

> **The market is a game** — AI understands the game state, consults with you, and helps find the optimal next move.

| Stage | Goal | Status |
|-------|------|--------|
| **Conversational** | Natural language signals, orders, positions via Telegram/OpenClaw | ✅ Complete |
| **Consultation** | AI explains the structural state + ranked choices | ✅ Complete (Context Engine) |
| **Game-like** | Full context awareness, multi-TF structural reasoning, optimal move suggestion | 🔜 Building |

*Note on naming: "Phase 4" in the product roadmap refers to the proactive signals feature. The "Phase 4 Context Engine" referenced in the [article series](medium/README.md) refers to the sequence labeling + state machine + operation gate architecture — a separate milestone.*

**구현·배포 정본**: 공개 개념·다이어그램은 **의도·스토리**를 설명한다. 실제 플래그·엔진·API JSON 키는 모노레포 `docs/DECKER_ENGINE_STAGING.md` §6, `ENGINE_PRODUCT_INTEGRATION_ROADMAP.md` §3.5.1, `docs/PUBLIC_DOC_AND_IP_RISK_MEMO.md` 를 따른다.

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
| HL 시세·시그널 (백엔드) | HL `allMids` → DB 시세(`hyperliquid`), 시장상태 시계열, funding 시그널(`hyperliquid_market`), watchlist 최초 노출 DB·알림, 배포 전 HL 단위테스트 CI 게이트 |
| OpenClaw 스킬 | SKILL.md 공개, web_fetch → Decker API |
| R3 시그널 LLM v3.0 | rationale·choices·tf_alignment·entry_timing (룰북 경로 $0) |
| R4 엔진+LLM 통합 | ChatJudgmentService, consultation, /llm/opportunities |

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
| CoinGecko OHLC·GeckoTerminal | 시세 보조 연동 (선택, Demo 한도 내) — 분석: docs/CoinGecko_vs_Decker_분석_20250317.md |
| 시그널 LLM v3.0 토큰 레이어 | (선택) 시그널 → LLM 호출 → 자연어 맥락. 현재 룰북 rationale로 대체 |
| 시그널 엔진 + LLM 앱 통합 | ✅ State Engine + Signal LLM = 통합 서비스 (Telegram + API + 스킬) |
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
| **llms.txt 패턴** | ✅ GET /llms.txt (AI 발견성) |

---

## Hyperliquid (백엔드) — 공개 로드맵 정렬 (2026)

> 메인 시세는 **Binance**를 유지하고, **Hyperliquid**는 DEX 영구선물·병행 소스로 연동한다. 구현·스키마·운영 체크리스트는 트레이딩 백엔드 레포에서 관리하며, 본 문서는 공개용 요약만 둔다.

| 영역 | 요약 |
|------|------|
| **시세** | HL `allMids` 주기 수집 → `market_data` (`data_source=hyperliquid`), 사용자 `exchange_preference`에 맞는 시세 우선 조회 |
| **시장상태·시그널** | `hyperliquid_market_state` 시계열, `judgment_signals` 소스 `hyperliquid_market` (funding/bias 기반) |
| **Watchlist** | TradFi/지수 심볼은 HL universe에 실제 노출될 때만 런타임 포함; **첫 노출**은 DB 이벤트 테이블에 기록·선택적 Slack(`ADMIN_SLACK_WEBHOOK`) |
| **품질 게이트** | 백엔드 배포 워크플로에서 HL 관련 단위테스트(스키마 폴백·시그널/API 정책 등) + Postgres 서비스로 선행 실행 |
| **로컬 Docker** | Postgres 초기화 시 HL 테이블 부트스트랩 스크립트 포함(신규 볼륨 기준) |

동기화: 비공개 작업 트리 `decker_ai_strategy_builder_sync/` → 스크립트 `scripts/sync_decker_ai_strategy_builder.sh`로 공개 레포 `decker-ai-strategy-builder` 반영.

---

## 베타 정책 (현재)

**API·에이전트는 베타 테스트 중입니다.**

| 구분 | 베타 | 정식 출시 후 |
|------|------|--------------|
| **공개 (키 없이)** | 시그널·전략·시세·llm/opportunities 모두 호출 가능 | 헬스체크, llms.txt만 |
| **API 키** | 선택 (있으면 usage 추적) | **필수** (회원가입 → 키 발급) |
| **한도** | 미적용 | Free 500/월, Pro 10k 등 |
| **과금** | 미적용 | Stripe 구독 |

**플로우**: ① decker-ai.com 회원가입 ② 설정 → API 키 발급 ③ X-Api-Key 헤더로 호출

상세: 메인 레포 `docs/API_인증_구조_20250318.md`, `docs/과금_서비스_실제_준비_갭_분석_20250317.md` (공개 레포에는 미포함)
