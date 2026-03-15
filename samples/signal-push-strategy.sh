#!/bin/bash
# 시그널 등록 → 전략 조회 (2단계) — 시그널 제공자·개발자 API 연동용
# 사용: ./signal-push-strategy.sh [symbol] [entry] [target] [stop]
# 예: ./signal-push-strategy.sh BTCUSDT 96000 100000 92000

API_URL="${DECKER_API_URL:-https://api.decker-ai.com}"
SYMBOL="${1:-BTCUSDT}"
ENTRY="${2:-96000}"
TARGET="${3:-100000}"
STOP="${4:-92000}"

echo "=== 1. 시그널 등록 (API 연동용) ==="
curl -s -X POST "$API_URL/api/v1/signals/push" \
  -H "Content-Type: application/json" \
  -d "{\"symbol\":\"$SYMBOL\",\"timeframe\":\"1h\",\"direction\":\"long\",\"entry_price\":$ENTRY,\"target_price\":$TARGET,\"stop_loss\":$STOP}" | jq .

echo ""
echo "=== 2. 전략 조회 ==="
curl -s "$API_URL/api/v1/signals/$SYMBOL/strategy?timeframe=1h" | jq .
