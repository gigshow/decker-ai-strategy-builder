# Decker AI API Guide

**API 연동·개발자용.** Decker AI Strategy Builder는 시그널·시세·전략을 하나로 제공합니다.

Base URL: `https://api.decker-ai.com`  
경로 prefix: `/api/v1/` (예: `/api/v1/signals/BTCUSDT/state`)  
전체 문서: [api.decker-ai.com/docs](https://api.decker-ai.com/docs)

**인증**: 아래 엔드포인트는 인증 불필요 (공개 API). POST /signals/push 포함.

> **베타**: API·에이전트는 베타 테스트 중. 한도·과금 미적용. 시그널·전략·룰북 모델만 제공.

---

## 비용 구분

| 구간 | 설명 |
|------|------|
| **룰북 기반** | /state, /strategy, /llm/opportunities — LLM 미사용, **AI 토큰 비용 없음** |
| **호출 수·티어** | Free 500/월, Pro 10k, Trader 50k, API 무제한 (베타: 미적용) |

---

## 시그널 등록 (POST) — API 연동용

시그널·시세 제공이 API로 연동되는 경우 사용. 서비스 사용자는 덱커가 이를 하나로 제공한다고 이해하면 됩니다. **용어**: judgment_signals = 시그널 소스(DB). /signals/ = API 경로.

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
| GET | /api/v1/signals/{symbol}/state | 종목별 시그널 상태 (progress_pct, status, risk_reward_ratio, market_state) |
| GET | /api/v1/signals/{symbol}/strategy?timeframe=1h&risk_appetite=medium | 진행도 기반 전략 (오퍼레이션 룰북) |
| GET | /api/v1/market/prices?symbols=BTCUSDT,ETHUSDT | 실시간 시세 |
| GET | /api/v1/judgment/compare?symbols=BTCUSDT,ETHUSDT&timeframe=1h | 다중 자산 비교 |
| GET | /api/v1/judgment/market-status?interval=24h | 시장 상태 (바이낸스 청산, HL 펀딩) |
| GET | /api/v1/llm/opportunities?symbol=BTC&minConfidence=0.6&limit=5 | LLM용 인사이트 피드 (conviction, progress_pct, strategy) |

---

## LLM 인사이트 API (v3.0 시그널 LLM)

```
GET /api/v1/llm/opportunities?symbol=BTC&minConfidence=0.6&limit=5
```

**용도**: 에이전트·대화형 서비스용. conviction, progress_pct, strategy 등 LLM에 넣기 좋은 JSON.

**파라미터**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| symbol | query | 종목 필터 (BTC, BTCUSDT 등, 생략 시 BTC·ETH·SOL) |
| minConfidence | query | 최소 신뢰도 0~1 (선택) |
| limit | query | 결과 수 1~50 (기본 10) |

**응답 예시**

```json
{
  "opportunities": [
    {
      "symbol": "BTCUSDT",
      "timeframe": "4h",
      "direction": "long",
      "conviction": 0.72,
      "risk_reward": 1.8,
      "progress_pct": 66,
      "status": "in_progress",
      "strategy": "66% 진행. 30% 부분 익절 제안. 나머지는 목표까지 홀드.",
      "entry_price": 96000,
      "target_price": 100000,
      "stop_loss": 92000,
      "current_price": 98640,
      "generated_at": "2025-03-17T10:00:00"
    }
  ],
  "count": 1
}
```

**비용**: 룰북 기반 (LLM 미사용) → AI 토큰 $0.

---

## 시그널 전략 API (핵심)

```
GET /api/v1/signals/{symbol}/strategy?timeframe=1h&risk_appetite=medium&tier=premium
```

**파라미터**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| symbol | path | BTCUSDT, ETHUSDT 등 |
| timeframe | query | 15m, 1h, 4h, 8h, 1d, 1w (기본 1h) |
| risk_appetite | query | low, medium, high (선택) |
| tier | query | basic, standard, premium (선택, Phase 5) |

**응답 예시**

```json
{
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "strategy": "66% 진행. 30% 부분 익절 제안. 나머지는 목표까지 홀드."
}
```

---

## status 값 정의

`GET /signals/{symbol}/state` 응답의 `signals[].state.status`:

| status | 의미 |
|--------|------|
| **in_progress** | 진행 중 (목표·손절 미도달) |
| **target_reached** | 목표 도달 |
| **stop_hit** | 손절 구간 |
| **expired** | 만료 |
| **unknown** | 미판정 (시세·진입가 없음) |

---

## progress_pct 해석

| progress 구간 | 의미 | 룰북 전략 |
|---------------|------|----------|
| 0~33% | 초기 | default (목표까지 홀드) |
| 33~50% | 진입·초기 익절 | risk=low 시 5% 초기 익절 |
| 50~66% | 중반 | 20% 부분 익절 또는 홀드 |
| 66~80% | 후반 | 30~50% 부분 익절 |
| 80~95% | 목표 근접 | 50~80% 부분 익절 |
| 95%+ | 직전 | 80% 부분 또는 전량 청산 |

---

## state 응답 확장 (v1.4)

`GET /signals/{symbol}/state` 응답:

| 필드 | 타입 | 설명 |
|------|------|------|
| progress_pct | number | 0~100 진행도 |
| status | string | in_progress, target_reached, stop_hit 등 |
| risk_reward_ratio | number? | (target-entry)/(entry-stop). stop_loss 있을 때만 |
| market_state | string? | 시장 국면: trend, trend_down, range (liquidation/funding 기반) |

`market_state`는 오퍼레이션 룰북의 `market_state` 조건과 연동. (breakout_early, pullback, range, trend 등 향후 확장)

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

# LLM 인사이트 (에이전트·대화형)
curl "https://api.decker-ai.com/api/v1/llm/opportunities?symbol=BTC&limit=5"
```
