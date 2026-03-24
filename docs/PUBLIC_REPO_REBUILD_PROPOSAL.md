# Decker 공개 레포 리빌딩 제안 (다음 세션 이어가기)

**상태**: P0~P4 반영됨 (이슈 템플릿·커뮤니티 문서·릴리즈 체크리스트).  
**배경**: GStack 스킬 레포는 “스킬 다운로드·커뮤니티” 중심, Decker는 “서비스 + 코드 + 문서”가 한 레포 — **페르소나별 진입점**을 나누지 않으면 첫인상이 산만해짐.  
**참고 분석**: `docs/DECKER_AGENT_SKILLS.md` (스킬 A/B 층), `docs/AGENT_SKILLS_PUBLIC_SUMMARY.md` (대외 짧은 인덱스 정책)

---

## 1. 목표 (이 레포의 공개 목적)

| 축 | 의도 |
|----|------|
| **제품** | 실제 사용 가능한 경로(웹·텔레그램·API)가 README에서 한눈에 |
| **온보딩** | 에이전트 스킬·명령은 **단일 출처** 링크만 노출 |
| **홍보·투명성** | 로드맵/상태는 링크 한 줄로, 장문은 별도 문서 |
| **기여** | 개발자 클론·실행·기여는 별 섹션 또는 `CONTRIBUTING` |

---

## 2. 현재 이슈 (요약)

- 루트 `README.md`에 **날짜별 변경·내부 작업 맥락**이 길게 쌓여 **GStack식 “한 화면 한 길”**과 거리가 있음.
- 방문자 유형이 **최종 사용자 / IDE 스킬 사용자 / 백엔드 기여자**로 나뉘는데, **같은 README에 모두** 섞여 있음.
- 스킬은 **레포 일부 경로만** 있으면 되는데, 전체 클론이 부담 — **“최소 다운로드 단위”**가 문서화되지 않음.

---

## 3. 제안: 페르소나별 진입 (README 상단 구조)

**목표 형태** (상단 ~20–40줄 안에 고정):

1. **한 줄 가치 제안** + 배지 + 라이브 링크  
2. **세 갈래 CTA**
   - **써보기** → `https://www.decker-ai.com`, 텔레그램/연동 링크 (`docs/TELEGRAM_AGENT_COMMANDS.md` 또는 서비스 내 안내)
   - **에이전트·스킬** → `docs/AGENT_SKILLS_PUBLIC_SUMMARY.md` → `DECKER_AGENT_SKILLS.md`, `openclaw_skills/README.md`
   - **개발자** → API Docs, (작성 시) `CONTRIBUTING`, 로컬 실행 최소 절차 링크  
3. **상세 변경 이력** → `CHANGELOG` / `docs/readme_history` / `WORK_STATUS` 로만 위임 (README 본문에서는 짧게)

---

## 4. 우선순위 작업 (P0 → P4)

### P0 — README 슬림 + 진입 3갈래

- [x] README 상단에 위 **3갈래** 반영  
- [x] “최근 변경” 블록은 `CHANGELOG`로 이전 (2025-03 요약)  
- [x] `docs/WORK_STATUS_AND_ROADMAP.md`는 README **개발자** 행·문서 표에서 링크

### P1 — 공개 온보딩 단일 문서 (선택 파일명)

- [x] `docs/ONBOARDING_PUBLIC.md` 신설 (제품 / Cursor / 기여자)  
- [x] `AGENT_SKILLS_PUBLIC_SUMMARY.md`에 한 줄로 교차 링크

### P2 — 스킬 “다운로드 가능 단위” 명시

- [x] `ONBOARDING_PUBLIC.md` §2에 최소 경로 표 + `sparse-checkout` 예시  
- [ ] (선택) 릴리즈 zip은 미작성

### P3 — 커뮤니티·이슈 정렬

- [x] `.github/ISSUE_TEMPLATE/config.yml` + `01`~`04` (제품 / API / IDE 스킬 / 자체 호스팅)
- [x] `docs/GITHUB_COMMUNITY.md` — Discussions 켜기·권장 카테고리·라벨

### P4 — 릴리즈 ↔ 문서 동기화 루틴

- [x] `docs/RELEASE_CHECKLIST_PUBLIC_DOCS.md` — 태그·ClawHub 전 체크리스트  
- [x] `DECKER_AGENT_SKILLS.md` §8 — `/document-release` 관례와 `docs(release): …` 커밋 패턴

---

## 5. 건드리지 말 것 (정책 유지)

- **단일 출처**: 텔레그램 `/` 명령·채널 구분 → `docs/TELEGRAM_AGENT_COMMANDS.md`  
- **짧은 대외 요약** → `docs/AGENT_SKILLS_PUBLIC_SUMMARY.md`  
- **스킬 목록의 소스 오브 트루스** → `docs/DECKER_AGENT_SKILLS.md` (표 변경 시 여기 먼저)

---

## 6. 다음 세션에서 할 일 (체크)

1. ~~README 편집·CHANGELOG 이관~~ (완료)  
2. ~~`ONBOARDING_PUBLIC.md` 초안~~ (완료)  
3. 링크·앵커(`#-빠른-시작` 등) 배포 후 GitHub에서 한 번 확인  
4. ~~P3 / P4~~ (완료) — 저장소에서 **Discussions** 기능만 켜면 됨

---

## 7. 관련 파일 (빠른 점프)

| 파일 | 역할 |
|------|------|
| `README.md` | 상단 3갈래·문서 표 (리빌딩 반영됨) |
| `docs/ONBOARDING_PUBLIC.md` | 레포 방문자 랜딩 |
| `docs/AGENT_SKILLS_PUBLIC_SUMMARY.md` | ClawHub·짧은 인덱스 |
| `docs/DECKER_AGENT_SKILLS.md` | 스킬 구조·표 |
| `docs/TELEGRAM_AGENT_COMMANDS.md` | 봇 명령 단일 출처 |
| `docs/WORK_STATUS_AND_ROADMAP.md` | 상태·로드맵 |
| `CLAUDE.md` | 세션 진입 요약 (링크 정합) |
| `docs/GITHUB_COMMUNITY.md` | Discussions·이슈 템플릿 |
| `docs/RELEASE_CHECKLIST_PUBLIC_DOCS.md` | 릴리즈 시 공개 문서 동기화 |
| `.github/ISSUE_TEMPLATE/` | 페르소나별 이슈 폼 |

---

*이 문서는 세션 간 핸드오프용이다. 실행 여부·일정은 팀/담당자 판단.*
