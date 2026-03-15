# Decker API Guide

공개 API 엔드포인트. Base URL: `https://api.decker-ai.com`

전체 문서: [api.decker-ai.com/docs](https://api.decker-ai.com/docs)

---

## 인증 불필요

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
# 시그널 상태
curl "https://api.decker-ai.com/api/v1/signals/BTCUSDT/state"

# 진행도 기반 전략
curl "https://api.decker-ai.com/api/v1/signals/BTCUSDT/strategy?timeframe=4h&risk_appetite=high"

# 공개 시그널
curl "https://api.decker-ai.com/api/v1/judgment/signals/public?symbol=BTCUSDT&timeframe=1h"
```
