# GitHub 커뮤니티 (P3)

## Discussions

1. 저장소 **Settings → General → Features → Discussions** 를 켠다.
2. 첫 게시 시 GitHub이 기본 카테고리를 제안한다. 아래를 **추가·이름 맞추기** 하면 이슈 템플릿과 정합하기 좋다.

| 제안 카테고리 | 용도 |
|---------------|------|
| **General** | 공지·잡담 |
| **Q&A** | 사용법·설정 질문 |
| **Ideas** | 기능 제안 |
| **Show and tell** | 연동·스크린샷 공유 |
| **IDE·스킬** (선택) | `.cursor/skills`·ClawHub |
| **자체 호스팅** (선택) | Docker·온프레미스 |

`config.yml`의 **Discussions** 링크는 위 설정 후 동작한다.

## 이슈 템플릿

경로: [`.github/ISSUE_TEMPLATE/`](../.github/ISSUE_TEMPLATE/)

| 템플릿 | 라벨 (권장) |
|--------|-------------|
| 제품 사용 | `product` |
| API·연동 | `api` |
| IDE·스킬 | `cursor-skills` |
| 자체 호스팅 | `self-hosting` |

라벨이 없으면 이슈는 열리지만 **해당 라벨은 자동 부착되지 않을 수 있다**. 저장소 **Issues → Labels** 에서 위 이름으로 만들어 두면 된다.

## 빠른 링크

- [공개 온보딩](./ONBOARDING_PUBLIC.md)
- [릴리즈 시 공개 문서](./RELEASE_CHECKLIST_PUBLIC_DOCS.md)
