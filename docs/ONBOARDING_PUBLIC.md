# Decker 공개 레포 — 방문자 온보딩

**목적**: GitHub·블로그·ClawHub에서 레포만 연 사람이 **페르소나별로 다음 한 걸음**만 선택하도록 정리한다.

**짧은 인덱스(표)**: [AGENT_SKILLS_PUBLIC_SUMMARY.md](./AGENT_SKILLS_PUBLIC_SUMMARY.md) — ClawHub·릴리즈 노트용으로 유지.

---

## 1. 제품을 써보고 싶다 (최종 사용자)

| 단계 | 링크 |
|------|------|
| 웹 | [decker-ai.com](https://www.decker-ai.com) |
| API 문서 | [api.decker-ai.com/docs](https://api.decker-ai.com/docs) |
| 텔레그램 봇 `/` 명령·자연어 | [TELEGRAM_AGENT_COMMANDS.md](./TELEGRAM_AGENT_COMMANDS.md) (단일 출처) |
| 연동(예) | [decker-link-telegram](https://decker-ai.com/decker-link-telegram), [decker-link (Slack)](https://decker-ai.com/decker-link) |

---

## 2. 로컬에서 Decker 도메인 스킬만 쓰고 싶다

상세 표·우선순위는 [DECKER_AGENT_SKILLS.md](./DECKER_AGENT_SKILLS.md)가 단일 출처다.

### 최소 경로 (전체 플랫폼 monorepo)

IDE 스킬·`.cursor/rules`는 **비공개 메인 레포**에 있다. 아래로 필요한 디렉터리만 받는다:

```bash
git clone --filter=blob:none --sparse https://github.com/gigshow/decker-trading-platform.git decker-skills
cd decker-skills
git sparse-checkout set .cursor/skills/decker-signal .cursor/skills/decker-execution-mode .cursor/rules
git sparse-checkout add docs
```

함께 두면 좋은 문서: `docs/DECKER_AGENT_SKILLS.md`, `docs/TELEGRAM_AGENT_COMMANDS.md`, 이 레포의 [openclaw_skills/README.md](./openclaw_skills/README.md).

### 이 레포(문서·샘플·스킬 패키지)만 클론

```bash
git clone https://github.com/gigshow/decker-ai-strategy-builder.git
```

---

## 3. 코드를 빌드·기여하고 싶다

| 단계 | 문서 |
|------|------|
| 이 레포 빠른 시작 | [README.md](../README.md) **Quick Start** |
| 로드맵 (이 레포) | [roadmap.md](./roadmap.md) |
| 전체 플랫폼 상태·로드맵 | 비공개 [decker-trading-platform](https://github.com/gigshow/decker-trading-platform) 의 `docs/WORK_STATUS_AND_ROADMAP.md` (접근 가능한 경우) |
| 엔지니어링 워크플로 스킬 표 | [DECKER_AGENT_SKILLS.md](./DECKER_AGENT_SKILLS.md) §3 — 일부 번들(`.agents/skills/gstack`)은 monorepo에만 존재 |
| 이슈·Discussions | [GITHUB_COMMUNITY.md](./GITHUB_COMMUNITY.md), [`.github/ISSUE_TEMPLATE/`](../.github/ISSUE_TEMPLATE/) |
| 릴리즈 시 공개 문서 | [RELEASE_CHECKLIST_PUBLIC_DOCS.md](./RELEASE_CHECKLIST_PUBLIC_DOCS.md) |
| 기여·문서 톤 | [CONTRIBUTING.md](../CONTRIBUTING.md) (루트) |

---

## 4. 한눈에 (표)

| 문서 | 용도 |
|------|------|
| [AGENT_SKILLS_PUBLIC_SUMMARY.md](./AGENT_SKILLS_PUBLIC_SUMMARY.md) | 짧은 인덱스 |
| [DECKER_AGENT_SKILLS.md](./DECKER_AGENT_SKILLS.md) | 스킬 구조·표 |
| [TELEGRAM_AGENT_COMMANDS.md](./TELEGRAM_AGENT_COMMANDS.md) | 텔레그램·웹 PhaseD 구분 |
| [CLAUDE.md](../CLAUDE.md) | 세션 진입 요약 |
| [GITHUB_COMMUNITY.md](./GITHUB_COMMUNITY.md) | Discussions·이슈 템플릿 |
| [RELEASE_CHECKLIST_PUBLIC_DOCS.md](./RELEASE_CHECKLIST_PUBLIC_DOCS.md) | 태그·대외 릴리즈 전 문서 |
| [CONTRIBUTING.md](../CONTRIBUTING.md) (루트) | 기여·공개 문서 톤 |

---

## 5. 메타

공개 레포 개선 제안·체크리스트: [PUBLIC_REPO_REBUILD_PROPOSAL.md](./PUBLIC_REPO_REBUILD_PROPOSAL.md).
