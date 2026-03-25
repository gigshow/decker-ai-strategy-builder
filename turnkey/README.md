# DeckerClaw Turnkey — 경량 Telegram 봇

**선택 D: 턴키** — OpenClaw 없이 Decker 시그널·전략을 Telegram에서 바로 사용. Way 1(호스팅 봇)과 구분하려면 [투웨이 모델 한 페이지](../docs/TWO_WAY_MODEL.md)를 본다.

시그널·전략 조회만 지원. DB 없음. Decker API 호출만.

---

## 5분 배포 (Railway)

1. **이 레포 포크** 또는 `turnkey/` 폴더만 복사
2. **Railway** → New Project → Deploy from GitHub
3. **Root Directory**: `turnkey` (또는 turnkey만 있는 레포면 `.`)
4. **Variables** 설정:
   - `TELEGRAM_BOT_TOKEN` — [@BotFather](https://t.me/BotFather)에서 발급
   - `DECKER_API_URL` — (선택) 기본 `https://api.decker-ai.com`
5. **Deploy** → 완료 후 봇에게 "비트코인 시그널" 전송

---

## 로컬 실행

**API 연동 검증** (토큰 없이):

```bash
cd turnkey
pip install -r requirements.txt
python verify_api.py
```

**Telegram 봇**:

```bash
export TELEGRAM_BOT_TOKEN=your_token
export DECKER_API_URL=https://api.decker-ai.com  # 선택
python bot.py
```

---

## 지원 명령

| 사용자 입력 | 동작 |
|-------------|------|
| `/start` | 환영 메시지 |
| "비트코인 시그널", "BTC 시그널" | BTCUSDT 시그널·전략 조회 |
| "ETH 전략 알려줘" | ETHUSDT 전략 조회 |
| "솔라나 시세" | SOLUSDT 시그널 조회 |

**주문·포지션·자동주문**은 [decker-ai.com](https://decker-ai.com) 또는 [@deckerclawbot](https://t.me/deckerclawbot)에서 이용해 주세요.

---

## 아키텍처

```
[사용자 Telegram]
       │
       ▼
[DeckerClaw Turnkey]  ← 이 봇 (Railway 또는 로컬)
       │
       │ HTTPS
       ▼
[Decker API]  api.decker-ai.com
  - 시그널, progress_pct, 전략
  - RULES.yaml 룰북
```

---

## 참고

- [Decker API Guide](../docs/api-guide.md)
- [선택 기반 아키텍처](../docs/architecture.md) — 턴키 = 선택 D
