# Decker 에이전트·스킬 가이드

**목적**: 이 저장소에서 사용하는 **에이전트 스킬 구조·선택 규칙**을 한곳에 정리한다. (도메인 스킬 vs 엔지니어링 워크플로)  
외부에서 가져온 워크플로 패키지는 **레이아웃·배포 방식만 참고**하고, 명명·우선순위·도메인 규칙은 **Decker 모델**에 맞춘다.

**최종 갱신**: 2026-04-23

---

## 1. 스킬 두 층 (구조)

| 층 | 역할 | 경로 (예) | 비고 |
|----|------|-------------------|------|
| **A. Decker 도메인 스킬** | 시그널·실행·전략 등 **제품 도메인** 전용 지침 | `.cursor/skills/decker-*` | 레포에만 존재, 최우선 참조 |
| **B. 엔지니어링 워크플로 스킬** | 리뷰·조사·QA·배포 등 **공통 개발 절차** | 동봉 패키지 아래 `SKILL.md` | 슬래시 명령으로 호출 (§3) |

---

## 2. Decker 도메인 스킬 (표)

에이전트는 해당 작업을 할 때 **아래 스킬을 먼저** 읽는다.

| 스킬 ID | 용도 (언제) | 디렉터리 | 핵심 문서·코드 |
|---------|----------------|----------|----------------|
| `decker-signal` | 시그널 수집·저장·배포, Signal LLM, `judgment_signals`, 룰북·tier | `.cursor/skills/decker-signal/` | `docs/SIGNAL_LLM_*.md`, `operation_rules_loader.py` |
| `decker-execution-mode` | `execution_mode`, `ExecutionRouter`, 모의/실 라벨, 채팅 주문 경로 | `.cursor/skills/decker-execution-mode/` | `chat_trading_service`, `execution/` |

**추가 예정** (도메인이 커지면 같은 패턴으로 행 추가): 전략빌더 파이프라인, 운영 알림 등.

각 `SKILL.md`는 공통으로 **YAML frontmatter** (`name`, `description`) + **한 장 요약** + **문서 맵** + **코드 경로 표**를 유지한다.

---

## 3. 엔지니어링 워크플로 스킬 (표)

제품 도메인이 아닌 **개발 절차**에 대응한다. 호출은 관례적으로 **슬래시 명령** (`/review`, `/investigate` 등)을 쓴다.

**소스 위치**: 동봉 패키지 루트는 `.agents/skills/gstack/` (업스트림 디렉터리명 유지). 스킬 본문은 하위 폴더의 `SKILL.md`에 있다.

| 작업 유형 | 권장 호출 | 설명 |
|-----------|-----------|------|
| 아이디어·범위 정리 | `/office-hours` | 코딩 전 문제 정의·설계 방향 |
| CEO 관점 범위·우선순위 | `/plan-ceo-review` | 기능 컷·가치 재정의 |
| 아키텍처·엣지 케이스 | `/plan-eng-review` | 데이터 흐름·테스트 관점 |
| UX/디자인 기획 검토 | `/plan-design-review`, `/design-consultation` | 디자인 차원·시스템 |
| PR·랜딩 전 코드 리뷰 | `/review` | CI 통과 후 프로덕션 리스크 |
| 근본 원인 분석 | `/investigate` | 수정 전 가설 검증 (번들은 `/debug` 명칭 문서도 있음) |
| 디자인 감사·수정 루프 | `/design-review` | UI 일관성 |
| 브라우저 QA | `/qa`, `/qa-only` | 실제 Chromium 기반 검증 |
| 보안 감사 | `/cso` | OWASP·STRIDE |
| 테스트·푸시·PR | `/ship` | 원커맨드 출격 |
| 머지·배포·검증 | `/land-and-deploy`, `/canary` | 배포 파이프라인 |
| 릴리즈 후 문서 동기화 | `/document-release` | |
| 회고 | `/retro` | |
| 웹 브라우저 자동화 | `/browse` | **`mcp__claude-in-chrome__*` 사용 금지** |
| 인증 QA용 쿠키 | `/setup-browser-cookies` | |
| 안전 모드 | `/careful`, `/freeze`, `/guard`, `/unfreeze` | 파괴적 명령·편집 범위 |
| 원샷 다각 검토 | `/autoplan` | 다역할 파이프라인 |
| 성능·CWV | `/benchmark` | |
| 번들 자체 업그레이드 | (번들 제공 명령) | 패키지 내 `setup`·문서 참조 |

상세 목록은 동봉 패키지의 `AGENTS.md`와 각 `SKILL.md`를 따른다.

---

## 4. Decker 운영 원칙 (에이전트)

- **조사 없이 버그 수정 금지** — `/investigate` 등으로 원인 정리 후 수정.
- **머지 전 리뷰** — `/review` 권장.
- **프로덕션·DB·시크릿** — `/careful` 또는 `/guard` 고려.
- **브라우저** — `/browse` 스킬 경로만 사용 (위 표).

---

## 5. 배포·동기화 (기여자)

| 항목 | 내용 |
|------|------|
| Decker 도메인 스킬 | `.cursor/skills/decker-*/SKILL.md`를 레포와 함께 버전 관리. |
| IDE 프로젝트 스킬 | `.cursor/skills/<name>/` 구조 유지. |
| 동봉 워크플로 패키지 | 경로 이상 시 패키지 루트에서 `./setup --host auto` (패키지 README·`setup` 스크립트 참조). |

---

## 6. 텔레그램 에이전트 `/` 명령

제품 봇에서 쓰는 슬래시 명령·자연어 대응은 **`docs/TELEGRAM_AGENT_COMMANDS.md`** (단일 출처).  
웹 PhaseD(`chatCommandHandler.ts`)와의 **역할 분리**는 동 문서 **§6 채널 구분**.

**추가 명령 (2026-04-23)**: `/apikey` — 연동 후 Public API 키(`dk_live_xxx`) 자동 발급. 개발자가 `X-API-Key` 헤더로 공개 API를 사용할 수 있다. 상세: `docs/DEVELOPER_API_GUIDE.md`.

---

## 7. 관련 문서

| 문서 | 용도 |
|------|------|
| `CLAUDE.md` | 세션 진입·요약 링크 |
| `docs/ONBOARDING_PUBLIC.md` | GitHub 방문자·페르소나별 온보딩 |
| `CONTRIBUTING.md` (루트) | 기여·공개 문서·커밋 톤 |
| `docs/WORK_STATUS_AND_ROADMAP.md` | 상태·로드맵 |
| `docs/AGENT.md` | 에이전트 고도화 로드맵 |
| `docs/TELEGRAM_AGENT_COMMANDS.md` | 텔레그램 `/` 명령·자연어 |
| `docs/RELEASE_CHECKLIST_PUBLIC_DOCS.md` | 태그·대외 릴리즈 시 문서 동기화 (§8) |
| `docs/GITHUB_COMMUNITY.md` | Discussions·이슈 템플릿·라벨 안내 |

---

## 8. 릴리즈 시 공개 문서 동기화 (P4)

버전 태그·ClawHub·대외 공지 전에 **`docs/RELEASE_CHECKLIST_PUBLIC_DOCS.md`** 체크리스트를 따른다. 요약:

- **`AGENT_SKILLS_PUBLIC_SUMMARY`**, **`TELEGRAM_AGENT_COMMANDS`**, **OpenClaw `SKILL.md`**, **`CLAUDE.md`**, 필요 시 **`ONBOARDING_PUBLIC`** 이 서로 모순 없게 맞춘다.
- 스킬 표·§3 워크플로 표를 바꿀 때는 **이 문서(§1–§3)를 먼저** 고친 뒤 `CLAUDE.md`는 링크·한 줄만 맞춘다 (기존 규칙과 동일).
- 문서만 갱신하는 커밋은 `docs(release): sync public agent docs` 같은 메시지로 구분해도 된다. 자동화된 **`/document-release`** 가 있으면 그 절차에 **위 체크리스트**를 합친다.

---

*이 문서가 스킬 목록의 단일 출처다. 표를 바꿀 때는 여기를 먼저 갱신하고 `CLAUDE.md`는 링크·한 줄 요약만 맞춘다.*
