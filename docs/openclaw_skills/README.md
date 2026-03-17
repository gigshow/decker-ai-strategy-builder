# OpenClaw Decker 스킬

**선택 B: OpenClaw 협업** — 자신의 OpenClaw에 Decker 스킬을 추가해 시그널·전략·포지션·주문을 연동할 수 있습니다.

> **동기화**: 이 폴더의 SKILL.md는 메인 레포 `docs/openclaw_skills/decker/`에서 `sync_skill_to_public_repo.sh`로 동기화됩니다.

## 스킬 추가 방법

1. [Decker SKILL.md](decker/SKILL.md) 다운로드
2. 자신의 OpenClaw `skills/decker/` 폴더에 추가
3. 트리거 ("시그널 알려줘", "포지션 보여줘" 등) → `web_fetch` → Decker API 호출

## 흐름

```
사용자 "시그널 알려줘" → OpenClaw (Claude) → Decker 스킬 트리거
  → web_fetch GET https://api.decker-ai.com/... → API 응답 → Claude 자연어 전달
```

상세: [Brand Guide — Way 2](BRAND_GUIDE.md)
