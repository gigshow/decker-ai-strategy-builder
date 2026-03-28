# Decker Quick Start

**3 steps. Under 5 minutes. Signal → State → Strategy.**

| Path | Time | What you get |
|------|------|-------------|
| **API (no account)** | 30 sec | `curl "https://api.decker-ai.com/api/v1/signals/BTCUSDT/state"` |
| **Telegram** | 5 min | Connect [@deckerclawbot](https://t.me/deckerclawbot) → ask in natural language |
| **OpenClaw skill** | 10 min | Add Decker skill → `web_fetch` → API integration |

*For deeper context on how the engine works: [Sequence Engine concept](../concept/sequence_engine.md) · [Article Series](medium/README.md)*

---

*한국어 가이드 / Korean guide below*

---

3단계로 시작. 5분 안에 시그널·포지션·주문 체험.

---

## 1. 가입

1. [decker-ai.com](https://decker-ai.com) 접속
2. 회원가입 (무료)

---

## 2. 연동

### Telegram (권장)

1. [decker-ai.com/decker-link-telegram](https://decker-ai.com/decker-link-telegram) 접속
2. 로그인 후 **연동 코드** 발급
3. Telegram에서 [@deckerclawbot](https://t.me/deckerclawbot) 검색 → 대화 시작
4. `/start {발급받은코드}` 전송
5. 연동 완료

### OpenClaw 스킬 연동 (선택 B)

**에이전트 모델 선택 B** — 자신의 OpenClaw에 Decker 스킬을 추가해 시그널·전략을 연동합니다. Slack (제한 시 Telegram 우선)·Discord 등 OpenClaw 지원 채널에서 사용 가능.

1. [Decker SKILL.md](openclaw_skills/decker/SKILL.md) 다운로드
2. 자신의 OpenClaw `skills/decker/` 폴더에 추가
3. "시그널 알려줘" 등 트리거 → web_fetch → Decker API 호출

상세: [OpenClaw 스킬 가이드](openclaw_skills/README.md) · [Brand Guide — 선택 B](BRAND_GUIDE.md)

---

## 3. 사용 (말만 하면)

| 입력 | 기능 |
|------|------|
| `비트코인 시그널 알려줘` | BTCUSDT 시그널 (롱/숏, 진입가·목표가·손절가) |
| `포지션 보여줘` | 포트폴리오 요약 |
| `수익현황` | 총 평가액·손익 |
| `ETH 0.01 매수해줘` | 주문 (승인 플로우) |
| `이더리움 자동주문 해줘` | 시그널 발동 시 자동 매수 |
| `뉴스 보여줘` | 뉴스 즉시 |
| `이 시그널 지금 어떻게 할까?` | 진행도 기반 전략 (오퍼레이션 룰북) |

---

## 체험 시나리오 (순서대로)

1. **인사** — "하이" / "뭐 할 수 있어?"
2. **시그널** — "비트코인 시그널 알려줘"
3. **자동주문** — "이더리움 자동주문 해줘" → "자동주문 설정 보여줘"
4. **주문** — "ETH 0.01 매수해줘" → 승인 버튼 클릭

---

## API 연동 (개발자용)

API로 시그널·전략을 연동하는 경우 [API Guide](api-guide.md) 참고. 덱커는 시그널과 전략을 하나의 서비스로 제공합니다.

### 엔진 레시피 → 실봉 한 줄 (모노레포)

공개 문서는 **설명(레시피)** 이고, **실제 거래소 OHLCV → 엔진 JSON** 은 플랫폼 레포 스크립트로 돌립니다. 절차·명령은 [Engine recipe & run](engine-recipe-and-run.md) 를 본다.

---

## 에이전트 vs 대시보드

| 채팅에서 가능 | 대시보드에서만 |
|---------------|----------------|
| 시그널·시세·포지션·주문·청산·자동주문·뉴스 | 가입·연동·설정·API 키·알림 켜기·포트폴리오 리셋·전략 빌더 |

---

## AI 서비스 구조가 궁금하면?

[Architecture](architecture.md) — 서비스 뒷단 구조, 핵심 파이프라인 (Market Data → Label → State → Signal → LLM Reasoner → Web/Telegram/API)
