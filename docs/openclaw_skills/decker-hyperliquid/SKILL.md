---
name: decker-hyperliquid
description: "Use when user asks about Hyperliquid DEX trading via Decker. Triggers: HL, 하이퍼리퀴드, DEX, 영구선물, HL 매수, HL 포지션, Hyperliquid 시세. Includes Safety Guidelines (position sizing, slippage)."
user-invocable: true
metadata:
  version: 1.2.0
  extends: decker
---

# Decker + Hyperliquid (DEX) 스킬

## Goal

Decker를 통해 **Hyperliquid DEX**에서 시세 조회·주문 실행. 메인 decker 스킬을 확장.

## 운영 모델 (에이전트 컨텍스트)

- **메인 시세(서비스 기본)**: Binance 계열. HL은 **병행** — `market_data`에 `data_source=hyperliquid`로 주기 적재, 사용자 `exchange_preference=hyperliquid`이면 HL 소스 우선.
- **Watchlist(TradFi/지수·대표주식)**: HL universe·`allMids`에 **실제로 노출될 때만** 수집·시그널 대상에 자동 포함. 미노출 심볼은 조회 불가·시그널 없을 수 있음 — 사용자에게 "HL에 아직 없을 수 있어요" 수준으로 안내 (내부 API 경로·URL 출력 금지).
- **시그널**: Funding/bias 기반 시그널은 `judgment_signals`에 `source=hyperliquid_market`. 좋은 시그널 알림은 사용자 선호 거래소에 맞춰 시세 표시.
- **첫 상장 감지**: 운영 DB에 watchlist 활성 이벤트 기록·선택적 관리자 Slack (에이전트가 사용자에게 웹훅 노출 금지).

## Quick Reference

| 사용자 말 | 액션 | 비고 |
|-----------|------|------|
| "HL BTC 0.01 매수해줘", "Hyperliquid에서 이더 매수" | order-request **exchange_id=hyperliquid** | 승인 플로우 |
| "HL 시세", "Hyperliquid BTC 가격", "HL 바이어스", "SP500/골드/오일 시세" | 시세·바이어스 API (아래 참조) | 인증 불필요 |
| "HL 포지션", "Hyperliquid 포지션" | Assistant API | JWT 필요 |

## DECKER_API_URL

https://api.decker-ai.com

## 시세·바이어스 조회 (HL-L2 확장)

**HL 시세·펀딩·바이어스** — 인증 불필요. `{DECKER_API_URL}` = DECKER_API_URL 환경변수 또는 https://api.decker-ai.com

| 용도 | API | 응답 |
|------|-----|------|
| 종목별 시세·펀딩·바이어스 | `GET {DECKER_API_URL}/api/v1/hyperliquid/market-state?symbol=BTC` | mark_price, funding_rate, bias |
| HL 통합 시장상태 | `GET {DECKER_API_URL}/api/v1/judgment/market-status?exchange=hyperliquid` | sources.hyperliquid (bias, symbols) |

- symbol: BTC, ETH, SOL, XRP, DOGE, BNB, SP500, XYZ100, GOLD, OIL, AAPL, NVDA, TSLA, MSFT, AMZN
- exchange 파라미터: binance | hyperliquid | all (생략 시 전체)

## 주문 (Hyperliquid)

**order-request에 exchange_id=hyperliquid 추가**:

```
GET {DECKER_API_URL}/api/v1/link/slack/order-request?slack_user_id={sender_id}&symbol=BTC&side=buy&quantity=0.01&exchange_id=hyperliquid&openclaw_secret={OPENCLAW_SECRET}
```

- **exchange_id=hyperliquid** 필수 (Hyperliquid DEX 실행)
- symbol: BTC, ETH 등 (USDT 선물 자동)
- quantity: 계약 수량

## 전제 조건

- Decker 가입 + Slack 연동
- user_settings.exchange_preference = hyperliquid 또는 order 시 exchange_id 지정
- **Hyperliquid 키 연동** (Decker 설정 → 거래소 API 설정)

## Hyperliquid 키 설정 (에이전트 안내용)

1. **API 전용 지갑 생성**: https://app.hyperliquid.xyz/API 접속 → "Create API Wallet"
2. **개인키 백업**: 생성 시 표시되는 개인키(0x로 시작)를 안전하게 저장 (한 번만 표시)
3. **Decker 설정**: 로그인 → 설정 → 거래소 API 설정 → Hyperliquid
   - API Key: 지갑 주소(0x..., 42자) — 선택
   - Secret Key: 개인키(0x..., 64자 이상) — **필수**
4. **거래소 선택**: exchange_preference를 "Hyperliquid"로 설정 후 저장
5. **주문**: "HL BTC 0.01 매수해줘" (Slack/Telegram)

⚠️ API Wallet은 출금 불가, 거래 전용. 메인 지갑과 분리 권장.

## Safety Guidelines (ClawHub hyperliquid-trading 흡수)

**주문 실행 전:**
1. 사용자에게 거래 파라미터 확인 (코인, 수량, 방향, 가격)
2. 현재 시세·기존 포지션을 함께 표시
3. 예상 비용/수익 계산 후 안내

**Position sizing:**
- 계정 자산의 20% 초과 주문 시 경고
- 잔고 기준 적정 수량 제안

**가격·슬리피지:**
- Limit 주문 시 지정가와 현재가 비교
- 지정가가 시장가 대비 5% 이상 이탈 시 오타 가능성 경고
- 시장가 주문 시 슬리피지(5% 등) 안내

## Error Handling

- "Address required" / "Private key required" → Decker 설정에서 Hyperliquid 키 연동 확인
- "Unknown coin" / 시세 없음 → 코어 크립토(BTC, ETH, …) 심볼 확인. **TradFi/지수**는 HL에 **상장·노출된 경우에만** 조회 가능 — 미지원이면 decker 스킬의 HL 병행 안내와 동일하게 개념 설명만
- 네트워크 오류 → API 상태·연결 확인
- **자동 재시도 금지** — 실패 시 사용자 확인 후 재요청

## 참고

- 메인 decker 스킬: `docs/openclaw_skills/decker/SKILL.md` (v2.3.5+ HL 병행 요약)
- Hyperliquid: 탈중앙 영구선물 DEX
- 백엔드 마스터(내부): `docs/HL.md`
