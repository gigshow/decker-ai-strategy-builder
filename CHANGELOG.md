# Changelog

All notable changes to the Decker AI Strategy Builder are documented in this file.

---

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
