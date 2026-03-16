#!/bin/bash
# Decker API — curl 예제
# 로컬: BASE=http://localhost:8000 ./examples.sh

BASE="${DECKER_API_URL:-https://api.decker-ai.com}"
BASE="${BASE%/}"
API="$BASE/api/v1"
SYMBOL="${1:-BTCUSDT}"

echo "=== Decker API curl examples (symbol=$SYMBOL) ==="

echo -e "\n1. GET /signals/{symbol}/state"
curl -s "$API/signals/$SYMBOL/state?timeframe=1h" | head -c 500
echo "..."

echo -e "\n\n2. GET /signals/{symbol}/strategy"
curl -s "$API/signals/$SYMBOL/strategy?timeframe=1h&risk_appetite=medium" | head -c 500
echo "..."

echo -e "\n\n3. POST /signals/push (시그널 등록)"
curl -s -X POST "$API/signals/push" \
  -H "Content-Type: application/json" \
  -d "{\"symbol\":\"$SYMBOL\",\"timeframe\":\"1h\",\"direction\":\"long\",\"entry_price\":96000,\"target_price\":100000,\"stop_loss\":92000}"

echo -e "\n\n4. GET /judgment/signals/public"
curl -s "$API/judgment/signals/public?symbol=$SYMBOL&timeframe=1h" | head -c 300
echo "..."
