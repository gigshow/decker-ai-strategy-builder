# Decker Quick Start

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

### Slack

1. [decker-ai.com/decker-link](https://decker-ai.com/decker-link) 접속
2. Slack 사용자 ID 입력 (프로필 → 더보기 → 멤버 ID 복사, U로 시작)
3. Slack에서 @deckerclaw 봇이 있는 채널 또는 DM으로 이동

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

---

## 에이전트 vs 대시보드

| 채팅에서 가능 | 대시보드에서만 |
|---------------|----------------|
| 시그널·시세·포지션·주문·청산·자동주문·뉴스 | 가입·연동·설정·API 키·알림 켜기·포트폴리오 리셋·전략 빌더 |

---

## AI 서비스 구조가 궁금하면?

[Architecture](architecture.md) — 서비스 뒷단 구조, 핵심 파이프라인 (Market Data → Label → State → Signal → LLM Reasoner → Web/Telegram/API)
