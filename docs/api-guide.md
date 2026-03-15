# Decker API Guide

**API 연동·개발자용.** 서비스 사용자 관점에서는 덱커가 시그널·시세·전략을 하나로 제공합니다.

Base URL: `https://api.decker-ai.com`  
전체 문서: [api.decker-ai.com/docs](https://api.decker-ai.com/docs)

---

## 비용 구분

| 구간 | 설명 |
|------|------|
| **룰북 기반** | /state, /strategy, /llm/opportunities — LLM 미사용, **AI 토큰 비용 없음** |
| **호출 수·서버** | 정책은 별도. (Free 500/월 등 예정) |

---

## 시그널 등록 (POST) — API 연동용

시그널·시세 제공이 API로 연동되는 경우 사용. 서비스 사용자는 덱커가 이를 하나로 제공한다고 이해하면 됩니다.

```
POST /api/v1/signals/push
```

**Body** (JSON)

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| symbol | string | ✅ | BTCUSDT, ETHUSDT 등 |
| timeframe | string | | 15m, 1h, 4h, 8h, 1d, 1w (기본 1h) |
| direction | string | | long, short (기본 long) |
| entry_price | float | ✅ | 진입가 |
| target_price | float | ✅ | 목표가 |
| stop_loss | float | | 손절가 |
| current_price | float | | 현재가 (없으면 entry_price 사용) |

**등록 후** `/state`, `/strategy`, `/llm/opportunities` 즉시 사용 가능.

```bash
curl -X POST "https://api.decker-ai.com/api/v1/signals/push" \
  -H "Content-Type: application/json" \
  -d '{"symbol":"BTCUSDT","timeframe":"1h","direction":"long","entry_price":96000,"target_price":100000,"stop_loss":92000}'
```

---

## 인증 불필요 (GET)

| Method | Path | 용도 |
|--------|------|------|
| GET | /api/v1/system/health | 헬스체크 |
| GET | /api/v1/judgment/coverage | 20종목×6시간대 신호 현황 |
| GET | /api/v1/judgment/signals/public?symbol=BTCUSDT&timeframe=1h | 시그널 (direction, confidence, entry/target/stop) |
| GET | /api/v1/signals/{symbol}/state | 종목별 시그널 상태 (progress_pct, status) |
| GET | /api/v1/signals/{symbol}/strategy?timeframe=1h&risk_appetite=medium | 진행도 기반 전략 (오퍼레이션 룰북) |
| GET | /api/v1/market/prices?symbols=BTCUSDT,ETHUSDT | 실시간 시세 |
| GET | /api/v1/judgment/compare?symbols=BTCUSDT,ETHUSDT&timeframe=1h | 다중 자산 비교 |
| GET | /api/v1/judgment/market-status?interval=24h | 시장 상태 (바이낸스 청산, HL 펀딩) |

---

## 시그널 전략 API (핵심)

```
GET /api/v1/signals/{symbol}/strategy?timeframe=1h&risk_appetite=medium
```

**파라미터**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| symbol | path | BTCUSDT, ETHUSDT 등 |
| timeframe | query | 15m, 1h, 4h, 8h, 1d, 1w (기본 1h) |
| risk_appetite | query | low, medium, high (선택) |

**응답 예시**

```json
{
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "strategy": "66% 진행. 30% 부분 익절 제안. 나머지는 목표까지 홀드."
}
```

---

## 사용 예시

```bash
# 1. 시그널 등록 (시그널 제공자·개발자 API 연동용)
curl -X POST "https://api.decker-ai.com/api/v1/signals/push" \
  -H "Content-Type: application/json" \
  -d '{"symbol":"BTCUSDT","timeframe":"1h","direction":"long","entry_price":96000,"target_price":100000,"stop_loss":92000}'

# 2. 등록 후 전략 조회
curl "https://api.decker-ai.com/api/v1/signals/BTCUSDT/strategy?timeframe=1h"

# 시그널 상태
curl "https://api.decker-ai.com/api/v1/signals/BTCUSDT/state"

# 공개 시그널
curl "https://api.decker-ai.com/api/v1/judgment/signals/public?symbol=BTCUSDT&timeframe=1h"
```
