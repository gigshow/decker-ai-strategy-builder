---
name: decker-developer
description: "Use when a developer asks about Decker's Public API — obtaining API keys, authentication, rate limits, signal endpoints, SDK usage. Triggers: API key, dk_live, X-API-Key, public API, /public/signals, REST API, developer, integrate Decker, rate limit."
user-invocable: true
metadata:
  version: 1.0.0
  updated: 2026-04-23
---

# Decker Developer API 스킬

## Goal

개발자가 Decker Public API를 연동하는 데 필요한 **키 발급·인증·엔드포인트·Rate Limit** 안내.

---

## 1. API 키 발급 (무료)

**전체 흐름 (3단계)**:

1. [decker-ai.com](https://decker-ai.com) 회원가입
2. **decker-ai.com/decker-link-telegram** → 연동 코드 발급 → 텔레그램 `/start {코드}`
3. 텔레그램 @deckerclawbot 에서:

```
/apikey
→ dk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 발급
```

- `/apikey reset` — 기존 키 폐기 후 재발급.
- 키는 **한 번만** 전체 표시. 분실 시 `/apikey reset`.

**Tier**: 기본 FREE (100 req/day). 상위 플랜 문의는 텔레그램.

---

## 2. 인증 헤더

모든 Public API 요청에 헤더 추가:

```http
X-API-Key: dk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Base URL: `https://api.decker-ai.com`

---

## 3. Public Endpoints

### GET /api/v1/public/signals/{symbol}/latest

최신 시그널 — 방향·진입가·목표가·손절가·진행률.

```bash
curl -H "X-API-Key: dk_live_..." \
  "https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/latest?timeframe=1h"
```

**응답**:

```json
{
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "direction": "long",
  "entry_price": 94200.0,
  "target_price": 97500.0,
  "stop_loss": 92800.0,
  "current_price": 95100.0,
  "progress_pct": 27.3,
  "generated_at": "2026-04-23T09:00:00+00:00"
}
```

**timeframe 가능값**: `15m`, `30m`, `1h`, `4h`, `8h`, `1d`, `1w`

**operation_gate**: `GO` = 진입 신호 / `WATCH` = 관측 중 / `HOLD` = 대기 (GO만 진입 권고)

---

### GET /api/v1/public/signals/{symbol}/narrative

규칙 기반 구조 서사 — LLM 비용 없음, deterministic.

```bash
curl -H "X-API-Key: dk_live_..." \
  "https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/narrative?timeframe=4h"
```

**응답**:

```json
{
  "symbol": "BTCUSDT",
  "timeframe": "4h",
  "narrative": "BTC 4h: A-사이클 진행 중, 트리거 활성 — 상승 1단계 목표 유효.",
  "axis": "bullish",
  "generated_at": "2026-04-23T08:00:00+00:00"
}
```

---

## 4. Rate Limit

| Tier | 일일 한도 | 비고 |
|------|-----------|------|
| FREE | 100 req/day | 텔레그램 /apikey 자동 발급 |
| BASIC | 10,000 req/day | 문의 |
| PREMIUM | 100,000 req/day | 문의 |

429 응답 시 내일 리셋. 헤더: `X-RateLimit-Remaining`.

---

## 5. 시그널 소스 투명성

Public API는 **`engine:live_l1`** 소스만 반환한다.

- **engine:live_l1**: 캔들 클로즈 경계 deterministic 엔진. 엔진이 평가하지 않은 심볼/타임프레임은 404.
- 엔진 커버리지 확인: `/latest` 또는 `/narrative` 호출 → 404이면 미지원.
- 현재 지원 심볼: BTCUSDT, ETHUSDT 등 주요 페어 (확장 중).

---

## 6. Python 예시

```python
import httpx

API_KEY = "dk_live_..."
BASE = "https://api.decker-ai.com/api/v1/public/signals"

async def get_signal(symbol: str, timeframe: str = "1h") -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BASE}/{symbol}/latest",
            params={"timeframe": timeframe},
            headers={"X-API-Key": API_KEY},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
```

---

## 7. 에러 코드

| 코드 | 의미 | 처리 |
|------|------|------|
| 401 | 키 무효 또는 만료 | `/apikey reset`으로 재발급 |
| 404 | 해당 심볼/TF 엔진 미지원 | 지원 심볼(BTC/ETH/SOL/BNB/XRP/DOGE) 및 TF(30m/1h/4h/1d) 확인 |
| 422 | X-API-Key 헤더 자체 누락 | 헤더 추가 |
| 429 | Rate limit 초과 | 내일 리셋 또는 플랜 업그레이드 |

---

## 8. OpenAPI 문서

`https://api.decker-ai.com/docs` — SwaggerUI (Public API 섹션만 노출).

---

*단일 출처: `docs/openclaw_skills/decker-developer/SKILL.md`. 상세 안내: `docs/DEVELOPER_API_GUIDE.md`.*
