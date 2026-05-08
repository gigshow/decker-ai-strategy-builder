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

## 데이터 소스 계약 (Way D)

turnkey 인스턴스는 자체 엔진 없음. 모든 데이터는 Decker 공개 API에서:

| 엔드포인트 | 용도 |
|-----------|------|
| `GET /public/signals/{sym}/latest` | 최신 시그널 (방향·진입가) |
| `GET /public/signals/{sym}/consumer` | 진입가·목표가·손절가 + overlay |
| `GET /public/state/live?symbol={sym}` | 엔진 상태 (c_state, action_gate) |
| `GET /public/reading/{sym}/{tf}` | AI 판독 |
| `GET /public/signals/{sym}/narrative` | 자연어 요약 |

**API Key** — `https://app.decker-ai.com/settings/apikey` 에서 발급  
환경변수 `DECKER_API_KEY`로 주입 (기존 `DECKER_API_URL`과 함께)

**Python SDK 연동 (선택)**:
```python
pip install decker-client  # 또는 pip install ./sdk/python
```
```python
from decker_client import Client
client = Client(api_key=os.environ["DECKER_API_KEY"])

state   = client.state.get_live("BTCUSDT", tf="4h")
sig     = client.signals.get_consumer("BTCUSDT")
reading = client.reading.explain("BTCUSDT", "4h")
```

---

## 아키텍처

```
[사용자 Telegram]
       │
       ▼
[DeckerClaw Turnkey]  ← 이 봇 (Railway 또는 로컬)
       │ X-API-Key: dk_live_xxx
       │ HTTPS
       ▼
[Decker 공개 API]  api.decker-ai.com
  /public/signals/{sym}/consumer   ← 진입가·목표가·손절가
  /public/state/live               ← 엔진 상태
  /public/reading/{sym}/{tf}       ← AI 판독
```

---

## 참고

- [Decker API Guide](../docs/api-guide.md)
- [Python SDK README](../../sdk/python/README.md)
- [선택 기반 아키텍처](../docs/architecture.md) — 턴키 = 선택 D
