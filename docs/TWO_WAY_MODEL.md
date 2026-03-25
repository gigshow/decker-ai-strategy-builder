# DeckerClaw 투웨이 모델 — 한 페이지

**목적**: 같은 Decker API·시그널 엔진을 **Way 1(자체 에이전트)** 과 **Way 2(OpenClaw 스킬)** 로 쓸 때, 누가 무엇을 고르는지 한 화면에서 정리한다. API 직접·턴키는 아래 표에 함께 둔다.

**짧은 인덱스**: [AGENT_SKILLS_PUBLIC_SUMMARY.md](./AGENT_SKILLS_PUBLIC_SUMMARY.md) · 상세 브랜딩 표현: [BRAND_GUIDE.md](./BRAND_GUIDE.md)

---

## 핵심 한 줄

> **Telegram [@deckerclawbot](https://t.me/deckerclawbot) = Way 1 — Decker 자체 에이전트(OpenClaw 미경유). 자신의 OpenClaw에 스킬만 붙이는 경로 = Way 2 — `web_fetch` → Decker API.**

---

## 같은 백엔드, 다른 입구

```
        ┌─────────────────────────────────────┐
        │  Decker API · State Engine · RULES  │
        └─────────────────┬───────────────────┘
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
   Way 1 — 자체 에이전트              Way 2 — OpenClaw 스킬
   Telegram / 웹 (호스팅)             사용자 OpenClaw → SKILL.md
```

문서·아키텍처의 **선택 A~D**와의 대응: [architecture.md](./architecture.md) (에이전트 레이어 다이어그램).

| 흔한 이름 | 문서상 코드명 | 요약 |
|-----------|----------------|------|
| Way 1 | 선택 A | 호스팅된 DeckerClaw — 룰북 우선 경로, 즉시 체험 |
| Way 2 | 선택 B | 개발자 OpenClaw + Decker 스킬 |
| REST | 선택 C | API 직접 |
| 경량 봇 | 선택 D | OpenClaw 없이 [turnkey](../turnkey/README.md)로 자가 배포 |

---

## 누구에게 무엇인가

| 대상 | 경로 | 다음 한 걸음 |
|------|------|----------------|
| 바로 써보기 (비개발자) | **Way 1** | [decker-ai.com](https://decker-ai.com) · [@deckerclawbot](https://t.me/deckerclawbot) · [TELEGRAM_AGENT_COMMANDS.md](./TELEGRAM_AGENT_COMMANDS.md) |
| OpenClaw·ClawHub 사용자 | **Way 2** | [openclaw_skills/README.md](./openclaw_skills/README.md) → `decker/SKILL.md` |
| 백엔드만 붙이기 | **선택 C** | [api-guide.md](./api-guide.md) · [api.decker-ai.com/docs](https://api.decker-ai.com/docs) |
| OpenClaw 없이 내 Telegram 봇 | **선택 D** | [turnkey/README.md](../turnkey/README.md) (Railway 등) |

---

## 5분 데모 스크립트

| 시간 | 행동 | 기대 결과 |
|------|------|-----------|
| ~30초 | `curl`로 시그널 state 조회 ([Try It Now](https://github.com/gigshow/decker-ai-strategy-builder#-try-it-now) 예시) | JSON에 `progress_pct` 등 |
| ~3분 | 레포 [samples/](../samples/) 스크립트 (예: `signal-push-strategy.sh`) | 로컬에서 전략·시그널 흐름 확인 |
| ~5분 | Telegram에서 "비트코인 시그널 알려줘" | Way 1 응답 |
| (선택) | Railway에 turnkey 배포 | 선택 D — 자가 호스팅 경량 봇 |
| (선택) | OpenClaw에 Decker 스킬 추가 후 동일 의도 발화 | Way 2 — `web_fetch` → API |

---

## 혼동 방지

| 오해 | 실제 |
|------|------|
| "DeckerClaw = 전부 OpenClaw 기반" | **아님.** Telegram 메인 경로(Way 1)는 **자체 에이전트**다. |
| "Slack이 Way 1과 동일" | Slack·Discord 쪽은 **Way 2**(OpenClaw 스킬)가 전형적이다. 제한·우선 채널은 [BRAND_GUIDE.md](./BRAND_GUIDE.md)를 따른다. |

---

## 더 읽기

| 문서 | 용도 |
|------|------|
| [ONBOARDING_PUBLIC.md](./ONBOARDING_PUBLIC.md) | 페르소나별 온보딩 |
| [architecture.md](./architecture.md) | 선택 A~D 다이어그램 |
| [roadmap.md](./roadmap.md) | 공개 로드맵 |
