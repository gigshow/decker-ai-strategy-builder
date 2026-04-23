# Decker Roadmap

---

## Vision

> **The market is a game** — AI understands the game state, consults with you, and helps find the optimal next move.


| Stage              | Goal                                                                           | Status                                                                                                                             |
| ------------------ | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Conversational** | Natural language signals, orders, positions via Telegram/OpenClaw              | ✅ Complete                                                                                                                         |
| **Consultation**   | AI explains the structural state + ranked choices                              | **✅ Shipped** · *strategic “mid-term” depth, engine contracts, and ops quality are still **iterating** (see alignment note below)* |
| **Game-like**      | Full context awareness, multi-TF structural reasoning, optimal move suggestion | 🔜 Building                                                                                                                        |


*Note on naming: "Phase 4" in the product roadmap refers to the proactive signals feature. The "Phase 4 Context Engine" referenced in the [article series](medium/README.md) refers to the sequence labeling + state machine + operation gate architecture — a separate milestone.*

**내부 SSOT와 맞추는 한 줄 (비전 단계)**: 비공개 모노레포 `WORK_STATUS` **§1 한눈에 보기** 기준 — **1단계(대화형)는 완료**, **중기(상의)는 “준비 중”**으로 표기한다. 그와 동시에 R3/R4·상의 API·엔진 merge·채널은 **이미 가동**한다. 즉 “기능이 없다”가 아니라, **비전 단계의 ‘완료’와 ‘제품 가동’을 혼동하면 안 된다**는 뜻이다. 아래 표의 R3·R4는 **완료**가 아니라 **가동·강화** 축에 둔다.

**구현·배포 정본**: 공개 개념·다이어그램은 **의도·스토리**다. 실제 플래그·엔진·API JSON·`merge` 평면(plane 2.5)·`operation_rules` 로더는 **비공개 플랫폼 모노레포**가 정본이며, 공개본은 [operation_rules/RULES.yaml](../operation_rules/RULES.yaml) `version`/`updated`로만 추적한다. (내부 전용 경로·IP·절대 문서명은 **공개 repo에 싣지 않는다**.)

**내부 본선(요약, 단일 맨락 아님)**: 엔진·데이터·트리거·플랫폼·UX는 **서로 다른 우선순위 큐**(예: 상류 L0–L1, 티어1~3, 엔진 스프린트, FP empirical 출구, CBA/SMS, 운영 장애 복구)로 **병행**된다. “2026 Q2 엔진-퍼스트”는 **한 덩어리가 아니라** 내부 문서에 정의된 **다수 맨락**의 방향을 한 줄로 요약한 것이며, **끝난 일의 체크리스트가 아니다** — 세부·열림 이슈는 **비공개** `WORK_STATUS` §0·`HANDOFF`가 SSOT.

---

## 비전 (Vision)

> **시장 = 게임** — "오르면 매도, 내리면 매수" 게임 심리를 AI가 이해하고, 사용자와 상의해서 최적의 수를 실행한다.


| 단계            | 목표                                      | roadmap 매핑                                                                        |
| ------------- | --------------------------------------- | --------------------------------------------------------------------------------- |
| **1단계 (대화형)** | OpenClaw 주문 연결, 대화형 시그널·포지션·주문          | Phase 2~5, Our Story, 턴키 ✅                                                        |
| **중기 (상의)**   | 투자전문가처럼 상의 — rationale, confidence, 선택지 | R3·R4 **기능은 상당 부분 제공 중**; 다중 TF·엔진 필드·정책은 **지속 밀도 강화** (비공개 로드맵 `WORK_STATUS` §0) |
| **장기 (게임처럼)** | 시장 상태 이해, 최적의 수 제안                      | 아래 "장 long" + 엔진-퍼스트 프로그램과 병행                                                     |


---

## 완료 (제품·채널 마일스톤 — 비전 “중기·장기 완료”와 동일하지 않음)


| 항목                     | 내용                                                                                                                                   |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Phase 2                | Slack 연동, /decker-link (OpenClaw 경유)                                                                                                 |
| Phase 3                | 주문 승인 플로우                                                                                                                            |
| Phase 4                | 좋은 시그널 알림, 시그널 제안 → order                                                                                                            |
| Phase 5                | 사용자 여정, member_joined 환영                                                                                                             |
| Our Story              | 서비스 페이지 스토리 섹션                                                                                                                       |
| 턴키                     | turnkey/ 경량 Telegram 봇 (Railway 원클릭)                                                                                                 |
| 오퍼레이션 룰북 **v2.4.7+**   | 9+ 레이어, progress·multi-TF·**엔진 merge 평면**(QKV·게이·줄기·`action_gate`·trigger 레인 등), [RULES.yaml](../operation_rules/RULES.yaml) — 공개 미러 |
| Telegram               | @deckerclawbot, decker-link-telegram (자체 에이전트)                                                                                       |
| Hyperliquid·Polymarket | HL·PM 주문                                                                                                                             |
| HL 시세·시그널 (백엔드)        | HL `allMids` → DB 시세(`hyperliquid`), 시장상태 시계열, funding 시그널(`hyperliquid_market`), watchlist 최초 노출 DB·알림, 배포 전 HL 단위테스트 CI 게이트        |
| OpenClaw 스킬            | SKILL.md 공개, web_fetch → Decker API                                                                                                  |
| **공개 API + Python SDK** | `POST /public/auth/verify` · `X-API-Key` 인증 · tier 기반 Rate Limit (FREE 100/BASIC 10k/PREMIUM 100k req/day) · Redis INCR+EXPIREAT · `pip install decker-client` v0.1.0 · OpenAPI 공개 스펙 · [DEVELOPER_API_GUIDE.md](DEVELOPER_API_GUIDE.md) |


---

## 가동·강화 (중기 상의 축 — **이미 경로는 열려 있고**, 밀도·계약·관측이 계속)


| 항목           | 내용                                                                                                        |
| ------------ | --------------------------------------------------------------------------------------------------------- |
| R3 시그널 LLM   | rationale·choices·tf_alignment·entry_timing (룰북 경로 $0) — **서비스 가동**; v3.0 **토큰/레이어** 등은 아래 “예정”·내부 티어에 따름 |
| R4 엔진+LLM 통합 | ChatJudgmentService, consultation, `/llm/opportunities` — **가동**; 엔진 trace·merge·어드민·품질은 **지속**           |


---

## 진행 중


| 항목         | 내용                                                                                                                        |
| ---------- | ------------------------------------------------------------------------------------------------------------------------- |
| 공개 레포 동기   | `decker_ai_strategy_builder_sync` → GitHub `decker-ai-strategy-builder` (rsync); **RULES·roadmap·아키텍처** 주기 갱신             |
| 투웨이 모델 공식화 | Way 1(자체 에이전트) + Way 2(OpenClaw 스킬) 문서·온보딩 — [ONBOARDING_PUBLIC](ONBOARDING_PUBLIC.md) 기준 **대부분 정리됨**; 잔여는 생태·ClawHub 후순위 |
| 엔진-퍼스트 본선  | 2026 Q2 내부: 트리거 계약·청산 정책 v1.1·크로스-TF 원장·관측/성과 UI·운영 품질 — **공개 요약은 본 문서·architecture만**                                    |


---

## 예정


| 항목                           | 내용                                                                                         |
| ---------------------------- | ------------------------------------------------------------------------------------------ |
| CoinGecko OHLC·GeckoTerminal | 시세 보조 연동 (선택, Demo 한도 내) — 분석: docs/CoinGecko_vs_Decker_분석_20250317.md                     |
| 시그널 LLM v3.0 토큰 레이어          | (선택) 시그널 → LLM 호출 → 자연어 맥락. 현재 룰북 rationale로 대체                                            |
| 공개 백테스트·리포트 산출물              | progress-range·표본·재현 절 ([signal-performance](signal-performance.md)) — README "🔜" 항과 동일 축 |
| Slack                        | 사용법 확정 전까지 보류. Telegram 위주                                                                 |
| Discord 연동                   | 다음 세션 검토 (팀·커뮤니티 채널)                                                                       |
| What People Say              | 초기 사용자 쿼트 수집                                                                               |
| clawhub                      | decker 스킬 publish (후순위, 홍보·생태계 노출용)                                                        |
| Stripe 과금 연동                  | 유료 티어 Stripe 구독 결제 (BASIC/PREMIUM 업그레이드 플로우)                                               |


---

## 장기 (게임처럼)

> **시장 = 게임** — AI가 시장 상태를 이해하고, 사용자와 상의한 뒤 최적의 수를 제안·실행한다.


| 항목              | 내용                                                                       |
| --------------- | ------------------------------------------------------------------------ |
| **시장 상태 이해**    | 오더북·청산·펀딩 등 → 시장 국면 파악 (trend, range, breakout 등)                        |
| **최적의 수 제안**    | "이 국면에서 이 수가 유리하다" — 매수·매도·홀드 포인트                                        |
| **게임처럼 플레이**    | 바둑의 수처럼 — 시장 심리 예측, 리스크·리워드 논의 후 실행                                      |
| **선행 조건**       | 상의·엔진 경로의 **밀도·다중 TF·정책**이 제품 수준으로 안정 (비전 표의 “Complete”가 아닌 **품질·심도** 축) |
| **llms.txt 패턴** | ✅ GET /llms.txt (AI 발견성)                                                 |


---

## Hyperliquid (백엔드) — 공개 로드맵 정렬 (2026)

> 메인 시세는 **Binance**를 유지하고, **Hyperliquid**는 DEX 영구선물·병행 소스로 연동한다. 구현·스키마·운영 체크리스트는 트레이딩 백엔드 레포에서 관리하며, 본 문서는 공개용 요약만 둔다.


| 영역            | 요약                                                                                                     |
| ------------- | ------------------------------------------------------------------------------------------------------ |
| **시세**        | HL `allMids` 주기 수집 → `market_data` (`data_source=hyperliquid`), 사용자 `exchange_preference`에 맞는 시세 우선 조회 |
| **시장상태·시그널**  | `hyperliquid_market_state` 시계열, `judgment_signals` 소스 `hyperliquid_market` (funding/bias 기반)           |
| **Watchlist** | TradFi/지수 심볼은 HL universe에 실제 노출될 때만 런타임 포함; **첫 노출**은 DB 이벤트 테이블에 기록·선택적 Slack(`ADMIN_SLACK_WEBHOOK`) |
| **품질 게이트**    | 백엔드 배포 워크플로에서 HL 관련 단위테스트(스키마 폴백·시그널/API 정책 등) + Postgres 서비스로 선행 실행                                   |
| **로컬 Docker** | Postgres 초기화 시 HL 테이블 부트스트랩 스크립트 포함(신규 볼륨 기준)                                                          |


동기화: 비공개 작업 트리 `decker_ai_strategy_builder_sync/` → 스크립트 `scripts/sync_decker_ai_strategy_builder.sh`로 공개 레포 `decker-ai-strategy-builder` 반영.

---

## API 인증 · 한도 (현재)

| 구분 | 설명 |
|------|------|
| **인증** | `X-API-Key` 헤더 필수 (모든 `/public/*` 경로) |
| **키 발급** | [decker-ai.com](https://decker-ai.com) → 설정 → API 키 |
| **FREE** | 100 req/day |
| **BASIC** | 10,000 req/day |
| **PREMIUM** | 100,000 req/day |
| **초과 시** | HTTP 429 + `Retry-After` |

**플로우**: ① [decker-ai.com](https://decker-ai.com) 회원가입 ② 설정 → API 키 발급 ③ `X-API-Key` 헤더로 호출

상세: [DEVELOPER_API_GUIDE.md](DEVELOPER_API_GUIDE.md)