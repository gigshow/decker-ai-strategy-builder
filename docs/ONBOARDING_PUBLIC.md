# Decker 공개 레포 — 방문자 온보딩

**목적**: GitHub·블로그·ClawHub에서 레포만 연 사람이 **페르소나별로 다음 한 걸음**만 선택하도록 정리한다.

**짧은 인덱스(표)**: [AGENT_SKILLS_PUBLIC_SUMMARY.md](./AGENT_SKILLS_PUBLIC_SUMMARY.md) — ClawHub·릴리즈 노트용으로 유지.

**투웨이 모델 (Way 1 자체 에이전트 · Way 2 OpenClaw 스킬)** — [TWO_WAY_MODEL.md](./TWO_WAY_MODEL.md)에서 한 페이지로 정리한다.

---

## 1. 제품을 써보고 싶다 (최종 사용자)

| 단계 | 링크 |
|------|------|
| 웹 | [decker-ai.com](https://www.decker-ai.com) |
| API 문서 | [api.decker-ai.com/docs](https://api.decker-ai.com/docs) |
| API 연동 가이드 | [DEVELOPER_API_GUIDE.md](./DEVELOPER_API_GUIDE.md) — 인증·SDK·Rate Limit |
| 텔레그램 봇 `/` 명령·자연어 | [TELEGRAM_AGENT_COMMANDS.md](./TELEGRAM_AGENT_COMMANDS.md) (단일 출처) |
| 연동(예) | [decker-link-telegram](https://decker-ai.com/decker-link-telegram), [decker-link (Slack)](https://decker-ai.com/decker-link) |

**시그널 용어 (한눈에)**: Decker는 **`winner_layer`**(차트·디버그에서 “지금 어느 축이 모니터상 우세하게 보이는지”를 가리키는 표시)와 **`winner_stem_*`**(푸시·운영 룰에 쓰는 “승자 줄기”, 메인·서브·연결 중 실제로 귀속된 줄기)를 **구분**합니다. 같은 봉에서 둘이 **다를 수** 있으니, 알림·자동화 해석은 **`winner_stem_*`**(및 엔진이 노출하는 stem·레인 필드)를 기준으로 보는 것이 맞습니다. 기술적 배경·호환 일정은 [ADR-002 — winner_layer vs winner_stem](adr/ADR-002-winner-layer-vs-winner-stem-deprecation.md)을 참고하세요.

---

## 2. 로컬에서 Decker 도메인 스킬만 쓰고 싶다

상세 표·우선순위는 [DECKER_AGENT_SKILLS.md](./DECKER_AGENT_SKILLS.md)가 단일 출처다.

### 최소 경로 (레포 안에서)

| 경로 | 역할 |
|------|------|
| `.cursor/skills/decker-signal/` | 시그널·Signal LLM·룰북·tier |
| `.cursor/skills/decker-execution-mode/` | `execution_mode`, ExecutionRouter, 모의/실 |
| `.cursor/rules/decker-agent-skills.mdc` | 프로젝트 규칙 → 위 스킬 표 참조 |

함께 두면 좋은 문서: `docs/DECKER_AGENT_SKILLS.md`, `docs/TELEGRAM_AGENT_COMMANDS.md`(제품 봇과 혼동 시), [openclaw_skills/README.md](./openclaw_skills/README.md).

### 레포 전체 없이 디렉터리만 받기 (선택)

```bash
git clone --filter=blob:none --sparse https://github.com/gigshow/decker-trading-platform.git decker-skills
cd decker-skills
git sparse-checkout set .cursor/skills/decker-signal .cursor/skills/decker-execution-mode .cursor/rules
git sparse-checkout add docs
```

`docs/`는 위 명령으로 상위 폴더만 포함되며, 필요 시 `docs/DECKER_AGENT_SKILLS.md` 등만 골라 쓰면 된다. 원격·브랜치는 포크에 맞게 바꾼다.

---

## 3. 코드를 빌드·기여하고 싶다

| 단계 | 문서 |
|------|------|
| 클론·Docker·로컬 포트 | [README.md](../README.md)의 **빠른 시작** |
| 상태·로드맵 | [WORK_STATUS_AND_ROADMAP.md](./WORK_STATUS_AND_ROADMAP.md) |
| 엔지니어링 워크플로 스킬(리뷰·QA·배포 등) | [DECKER_AGENT_SKILLS.md](./DECKER_AGENT_SKILLS.md) §3, 동봉 `.agents/skills/gstack/` |
| 이슈·Discussions | [GITHUB_COMMUNITY.md](./GITHUB_COMMUNITY.md), [`.github/ISSUE_TEMPLATE/`](../.github/ISSUE_TEMPLATE/) |
| 릴리즈 시 공개 문서 | [RELEASE_CHECKLIST_PUBLIC_DOCS.md](./RELEASE_CHECKLIST_PUBLIC_DOCS.md) |
| 기여·문서 톤 | [CONTRIBUTING.md](../CONTRIBUTING.md) (루트) |

---

## 4. 한눈에 (표)

| 문서 | 용도 |
|------|------|
| [TWO_WAY_MODEL.md](./TWO_WAY_MODEL.md) | Way 1·2·API·턴키 한 페이지 |
| [AGENT_SKILLS_PUBLIC_SUMMARY.md](./AGENT_SKILLS_PUBLIC_SUMMARY.md) | 짧은 인덱스 |
| [DECKER_AGENT_SKILLS.md](./DECKER_AGENT_SKILLS.md) | 스킬 구조·표 |
| [TELEGRAM_AGENT_COMMANDS.md](./TELEGRAM_AGENT_COMMANDS.md) | 텔레그램·웹 PhaseD 구분 |
| [CLAUDE.md](../CLAUDE.md) | 세션 진입 요약 |
| [GITHUB_COMMUNITY.md](./GITHUB_COMMUNITY.md) | Discussions·이슈 템플릿 |
| [RELEASE_CHECKLIST_PUBLIC_DOCS.md](./RELEASE_CHECKLIST_PUBLIC_DOCS.md) | 태그·대외 릴리즈 전 문서 |
| [CONTRIBUTING.md](../CONTRIBUTING.md) (루트) | 기여·공개 문서 톤 |
| [ADR-002 — winner_layer vs winner_stem](adr/ADR-002-winner-layer-vs-winner-stem-deprecation.md) | 시그널 해석: 모니터 표시 축 vs 승자 줄기(stem) |

---

## 5. 메타

공개 레포 개선 제안·체크리스트: [PUBLIC_REPO_REBUILD_PROPOSAL.md](./PUBLIC_REPO_REBUILD_PROPOSAL.md).
