# 릴리즈 시 공개 문서 동기화 (P4)

**언제**: 버전 태그·ClawHub·대외 공지 직전에 한 번 돈다.  
**관례 커밋 메시지**: `docs(release): sync public agent docs` (문서만 바꿀 때)

## 체크리스트

| # | 문서 / 산출물 | 확인 |
|---|----------------|------|
| 0 | (정책) `CONTRIBUTING.md` | 공개 문서·릴리즈 노트에 **작성 도구명으로 작성 주체를 표기하지 않음** |
| 1 | `docs/AGENT_SKILLS_PUBLIC_SUMMARY.md` | 표·한 줄이 현재 스킬·채널과 일치 |
| 2 | `docs/TELEGRAM_AGENT_COMMANDS.md` | `/` 명령·웹 PhaseD 구분 (단일 출처) |
| 3 | `docs/openclaw_skills/**/SKILL.md` (배포하는 패키지) | OpenClaw 스킬 버전·frontmatter·`README` 링크 |
| 4 | `CLAUDE.md` | 필독 목록·한 줄 요약이 위와 링크 정합 |
| 5 | `docs/DECKER_AGENT_SKILLS.md` | 도메인 스킬 표·§3 워크플로 표 변경 시 여기 먼저 |
| 6 | `docs/ONBOARDING_PUBLIC.md` | sparse-checkout·URL·페르소나 경로 |
| 7 | `docs/CHANGELOG.md` | 사용자에게 보일 변경 한 줄 (선택) |

## 워크플로 스킬과의 관계

엔지니어링 번들에서는 **`/document-release`** 를 쓰는 관례가 있다. Decker에서는 **공개 에이전트·명령 문서**는 위 표가 **최소 세트**이며, 위 표만 갱신하는 PR은 CI 부담이 적으므로 **문서 전용 커밋**으로 분리해도 된다.

## OpenClaw 스킬 버전

`docs/openclaw_skills/README.md` 및 패키지 내 `SKILL.md` frontmatter의 버전을 **릴리즈 노트·ClawHub 설명**과 동일하게 맞춘다.
