# Changelog

All notable changes to the Decker AI are documented in this file.

---

## [v1.5.0] - 2026-04-23

### Added (Sprint 2 — Public API · Rate Limit · SDK)

- **WP1 — 공개 API 인증**: `POST /api/v1/public/auth/verify` 엔드포인트 · `X-API-Key` 헤더 전용 인증 · `api_keys.tier` 스키마 (FREE / BASIC / PREMIUM, migration 070)
- **WP2 — Rate Limit v2**: tier 기반 일일 한도 (FREE 100 · BASIC 10,000 · PREMIUM 100,000 req/day) · Redis INCR+EXPIREAT · in-memory fallback · `X-RateLimit-Limit / Remaining / Reset` 응답 헤더 · 초과 시 HTTP 429 + `Retry-After`
- **WP3 — OpenAPI 공개**: `api.decker-ai.com/docs` 항상 접근 가능 (DEBUG 조건 제거) · 내부 라우터 `include_in_schema=False` (공개 경로 2개만 스펙 노출) · `scripts/export_openapi.py` CI 아티팩트
- **WP4 — Python SDK `decker-client` v0.1.0**: `pip install decker-client` · `Client` / `signals.get_narrative()` / `signals.get_latest()` / `health.check()` · `RateLimitError.retry_after` · respx 테스트 11건
- **WP5 — 개발자 문서**: `docs/DEVELOPER_API_GUIDE.md` 신규 · 인증·Rate Limit·Endpoints·SDK·FAQ 섹션

---

## [Unreleased]

### Changed

- **README.md**: 전면 재설계 — 페르소나 분기표(트레이더/개발자/에이전트빌더), quickstart 3단계(키발급→curl→SDK), `progress_pct` ASCII 시각화, GO/WATCH/HOLD 시나리오, 지원 심볼·TF 명시. PyPI 미배포 뱃지 제거, SDK 뱃지 `sdk/python/` 로컬 링크로 교체. **"Try it right now"** 데모 curl 블록 상단 추가.
- **docs/quickstart.md**: Step 0(키발급 Telegram) 선행, Path A(Telegram)/B(REST)/C(SDK) 명확 분리, 응답 필드 설명, 지원 심볼·TF 명시.
- **docs/api-guide.md**: 키 발급 경로 수정 ("Settings → API Keys" → Telegram `/apikey`).
- **sdk/python/README.md**: 키 발급 Telegram 경로 명시, `pip install` → `git clone + pip install -e` 안내.
- **docs/signal-performance.md**: 날짜 2026-04-23 갱신, 엔진 소스(`engine:live_l1`) 명시, 실시간 API 참조 안내.
- **docs/DEVELOPER_API_GUIDE.md**: §0 "Try it first (no sign-up)" 데모 섹션 추가; demo·stats 엔드포인트 스펙 문서화.

### Added

- **sdk/python/**: Python SDK `decker-client` 공개 레포에 포함 (`decker_client/` 패키지, `pyproject.toml`, `tests/`). PyPI 배포 예정.
- **백엔드 `GET /api/v1/public/demo`**: 인증 없이 BTCUSDT 1h 실시간 신호 + 내러티브 반환. IP당 10 req/day rate limit (Redis INCR+EXPIREAT, in-memory fallback). `public_demo.py` + `rate_limiting_v2.py` `check_demo_rate_limit()` 신규.
- **백엔드 `GET /api/v1/public/stats`**: 인증 없이 30일 엔진 신호 활동 통계 반환. 심볼별 평가 건수·gate 분포·타임프레임 커버리지. 60초 in-memory TTL 캐시. `public_stats.py` 신규.
- **백엔드 `GET /signal/{symbol}`**: 서버사이드 HTML 공유 카드 (OG 메타태그). Twitter/X·Discord 링크 프리뷰 지원. `public_signal_card.py` 신규. 마운트: `api.decker-ai.com/signal/{symbol}`.
- **Telegram 공유 링크**: 서비스 메시지(Stage A/B/C + MTF) 끝에 `📡 https://api.decker-ai.com/signal/{symbol}` 자동 추가.
- **GitHub Actions**: `.github/workflows/publish-sdk.yml` — `sdk-v*` 태그 push → 테스트(Py 3.9/3.11) → 빌드 → PyPI Trusted Publisher 배포. `.github/workflows/ci.yml` — `sdk/python/` 변경 시 자동 테스트(Py 3.9/3.11/3.12).
- **`sdk/python/pyproject.toml`**: URLs에 Bug Tracker·Changelog 추가. Source → 공개 레포 링크로 수정.
- **`sdk/python/README.md`**: 설치법 `pip install decker-client` (PyPI) 기본 안내로 변경.
- **`README.md`**: PyPI 배지 (`pypi/v/decker-client`), SDK quickstart `pip install decker-client`.

## [v1.4.9] - 2026-04-23

### Fixed (문서 정합)

- **`docs/roadmap.md`**: 내부 `WORK_STATUS` §1과 맞춤 — 비전 **Consultation**을 “완료=제품 없음”으로 읽히지 않게 하고, R3/R4는 **완료**가 아닌 **`## 가동·강화`**로 분리. 공개 repo에 없는 내부 문서 **절대 경로** 인용 제거. 장기 **선행 조건**을 “R3/R4 완료”가 아닌 **밀도·품질** 축으로 수정.
- **`docs/architecture.md`**: 2026-04 절 — “2026 Q2 단일 완료” 뉘앙스 완화, SSOT는 **비공개 모노레포** 수준으로 서술(공개 방문자에게 `WORK_STATUS` 파일명 강요 없음).
- **비공개** `docs/로드맵_통합.md`: §1·§2b·§3·§4를 위 스토리와 동기; **예정**에서 R3/R4 “미구현” 오해 제거(토큰 레이어 등만 예정).

## [v1.4.8] - 2026-04-23

### Changed

- **`operation_rules/RULES.yaml`**: 플랫폼 정본과 동기 — **v2.4.7** (WP-5.3 / ADR-010 Tier·`engine_action_gate`·trigger lane·merge plane §2.5 연계). 공개용 상단 4줄·`updated` 갱신 (`docs/PUBLIC_RULES_REDACTION_POLICY` §3).
- **`docs/roadmap.md`**: 룰북 버전·R3/R4·진행/예정 표를 **현재 제품**(중기 상의·엔진 통합 경로 가동)에 맞게 정리; “공개 레포” 행 → **동기 루틴**으로 명시; 2026 Q2 **엔진-퍼스트** 요약·비내부-경로-only 안내.
- **`docs/architecture.md`**: 2026-04 **정렬 절** 추가 — 공개 RULES·Game-like 로드맵·비공개 `WORK_STATUS` SSOT.
- **`README.md`**: Operations 표 **v2.4.7+** / 엔진 merge 조건 요약.
- **비공개** `docs/로드맵_통합.md`: RULES·roadmap·비전 표 동기.

## [v1.4.7] - 2026-03-30

### Changed

- **`operation_rules/RULES.yaml`**: 플랫폼 정본과 동기 — **v2.3.7** (QKV 연결·merge 평면 키·서브스윙 등). 공개면 헤더는 플랫폼 `PUBLIC_RULES_REDACTION_POLICY` 기준으로 내부 경로·비공개 문서명 제거.
- **`docs/architecture.md`**: merge·`connection.qkv`·룰 버전 정렬 한 줄 추가 (내부 구현 세부·IP 없음).

## [v1.4.6] - 2026-03-28

### Changed

- **README**: 상단 배지·히어로 링크에 **Kakao Channel** 복원; SEO keywords 보강
- **`llms.txt`**: Kakao 채널 URL 추가
- **`docs/architecture.md`**: 한 줄 소개·State Engine 절을 시퀀스·FSM·게이트·`operation_gate` 중심으로 정리
- **`.github/REPO_DISCOVERABILITY.md`**: GitHub About 권장 문구·Topics를 Phase 4 내러티브에 맞게 갱신

## [v1.4.5] - 2026-03-28

### Added

- **Concept**: `concept/sequence_engine.md` — Context Engine / Phase 4 narrative (labeling, FSM, gate, RULES, consultation)
- **Articles (Part 2)**: `docs/medium/part2/` — articles 11–15 (IP-sanitized); index updates in `docs/medium/README.md`

### Changed

- **공개 내러티브 정렬**: README, `diagrams/system_flow.md`, `docs/architecture.md`, `concept/labeling_algorithm.md`, `concept/signal_llm_concept.md`, `docs/model.md`, `examples/signal_example.md`, `examples/strategy_prompt_example.md` — Phase 4 시퀀스·FSM·GO/WATCH/HOLD·엔진/LLM 경계
- **`llms.txt`**: 루트를 단일 진입점으로 통합; `docs/llms.txt`는 루트로 안내
- **온보딩**: 삭제된 내부 기획 문서(`PUBLIC_REPO_REBUILD_PROPOSAL`) 제거·링크 대체
- **README**: `llms.txt`·Sequence Engine 표 링크; `operation_gate` 용어 통일

### Removed

- `docs/PUBLIC_REPO_REBUILD_PROPOSAL.md` — 내부용 기획 문서, 공개 레포에서 제외

## [v1.4.4] - 2026-03-24

### Added

- **에이전트·공개 문서** (ClawHub·방문자 온보딩): `docs/ONBOARDING_PUBLIC.md`, `AGENT_SKILLS_PUBLIC_SUMMARY.md`, `TELEGRAM_AGENT_COMMANDS.md`, `DECKER_AGENT_SKILLS.md`, `GITHUB_COMMUNITY.md`, `RELEASE_CHECKLIST_PUBLIC_DOCS.md` (당시 초안 `PUBLIC_REPO_REBUILD_PROPOSAL.md`는 이후 공개 레포에서 제거됨)
- **루트 `CLAUDE.md`** — 세션 진입용 에이전트 요약 (이 레포 기준)
- **`.github/ISSUE_TEMPLATE`** — `config.yml` + 페르소나별 `01`–`04` (제품 / API / IDE 스킬 / 자체 호스팅)
- **README** — 상단 Visitor paths(3갈래) + Docs 표에 위 문서 링크

---

## [v1.4.3] - 2026-03-19

### Changed

- **usage-guide**: Telegram 대화 키워드에 영문 예시 추가 (show signal, position, price, buy, sell, portfolio 등) — OpenClaw·영문 사용자 지원

---

## [v1.4.2] - 2026-03-18

### Added

- **Article Series (9~10)**: #9 Multi-TF Alignment, #10 Self-Improving Rulebook
- **rationale·choices**: llm_api, consultation에 tf_alignment·entry_timing 레이블 포함 (v3.0 시그널 LLM)
- **Telegram 대화 가이드**: usage-guide에 대화 키워드 (시그널, 전략·상의, 시세, 포지션 등) 추가

### Changed

- README: Article Series 1~10, Harness 목표 한 줄 추가
- api-guide: /llm/opportunities, /consultation에 tf_alignment, entry_timing 스펙

---

## [v1.4.1] - 2025-03-17

### Added

- **Article Series (1~8)**: Medium 연재 아티클 (State Engine, Signal Lifecycle, YAML, API, Backtest, State Machines, $0 LLM Cost)
- **DeckerClaw 클라이언트 아이콘**: `decker_client_claw_progress`, `_ring`, `_bar` (progress_pct 표현)
- **BRAND_GUIDE.md**: 네이밍·표현 규칙, DeckerClaw 포지셔닝
- **assets/**: DeckerClaw 마스코트, 클라이언트 아이콘, 로고

### Changed

- README: Article Series 링크, Try It Now 테이블 컬럼 정리 (Time|Path|What)
- MiroFish 레포 콘텐츠 흡수 (랜딩·퀵스타트·배지·아티클)

---

## [v1.4.0] - 2025-03-17

### Added

- **market_state** 조건: RULES에 `market_state: [range]`, `[trend]` 지원
- `progress_66_range`, `progress_80_trend` 룰 (시장 국면별 전략 분기)
- **risk_reward_ratio**: `/state` 응답에 (target-entry)/(entry-stop) 비율
- **market_state** API: `/signals/{symbol}/state`에 시장 상태 필드 (trend, range, trend_down)
- signal-performance 집계: progress 구간별(33~60, 61~80, 81~95) Win Rate 계산 유틸

### Changed

- RULES.yaml v1.4.0: progress_max, market_state 매칭
- api-guide: risk_reward_ratio, market_state 필드 문서화

---

## [v1.3.1] - 2025-03-15

### Changed

- **RULES.yaml**: `portfolio_default` 룰에 `portfolio_context_required: true` 추가
- 포트폴리오 맥락(weight_diff) 없을 때 default로 fallthrough

---

## [v1.3.0] - 2025-03-10

### Added

- progress 90/95 구간 룰 (`progress_90`, `progress_95`)
- 1h/1d timeframe 전용 룰 (`progress_66_1h`, `progress_66_4h`, `progress_80_1d`)
- progress 33/40 초기 진입 룰 (risk=low)
- progress 50 + risk=high 룰 (`progress_50_high`)

### Changed

- progress 상한 규칙 33~80 → 33~95 확장

---

## [v1.2.0] - 2025-02-15

### Added

- **v4 포트폴리오 스킬**: `weight_diff_min`, `weight_diff_max` 조건
- `portfolio_overweight`, `portfolio_underweight`, `portfolio_signal_80` 룰
- `portfolio_default` (비중 유지)

---

## [v1.1.0] - 2025-01-20

### Added

- 오퍼레이션 룰북 기본 구조 (RULES.yaml)
- `target_reached`, `stop_hit` status 기반 룰
- `progress_66`, `progress_80`, `progress_50` progress_min 룰
- `default` fallback 룰
- `operation_rules_loader.py` 연동
