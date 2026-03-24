# Decker 에이전트·명령 — 공개 요약 (ClawHub·온보딩용)

**목적**: 레포·블로그·ClawHub에 붙일 수 있는 **짧은 인덱스**. 상세는 링크만 유지.

| 문서 | 내용 |
|------|------|
| [ONBOARDING_PUBLIC.md](./ONBOARDING_PUBLIC.md) | 레포 방문자: 써보기·IDE 스킬·기여 경로 한 장 |
| [DECKER_AGENT_SKILLS.md](./DECKER_AGENT_SKILLS.md) | Decker 도메인 스킬(`decker-*`) vs 엔지니어링 워크플로 |
| [TELEGRAM_AGENT_COMMANDS.md](./TELEGRAM_AGENT_COMMANDS.md) | 텔레그램 봇 `/` 명령·자연어·웹 PhaseD와 채널 구분 |
| [openclaw_skills/README.md](./openclaw_skills/README.md) | OpenClaw 패키지·배포 경로 |
| [CLAUDE.md](../CLAUDE.md) (레포 루트) | 세션 진입 요약 |

## 한 줄

- **개발(IDE 스킬)**: 도메인은 `decker-signal`, `decker-execution-mode` 등 프로젝트 스킬.
- **사용자(텔레그램)**: `/help`, `/services`, 자연어 동일 동작 — 표는 `TELEGRAM_AGENT_COMMANDS.md`.
- **웹 PhaseD 데모 채팅**: `service-page` 내장 명령 — 텔레그램과 1:1 아님(§5).

## 릴리즈 노트에 넣을 때

위 표만 복사하거나, 변경 시 **해당 문서 단일 출처**를 갱신한 뒤 커밋 해시를 노트에 적는다.
