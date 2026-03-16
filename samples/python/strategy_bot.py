#!/usr/bin/env python3
"""
Strategy Bot — 시그널 → 전략 추천 → 주문 연결 예제

시그널 상태 조회 → 룰북 기반 전략 수신 → 주문 실행은 decker-ai.com 또는 Telegram에서.

사용: python strategy_bot.py [symbol]
예: python strategy_bot.py BTCUSDT

환경변수: DECKER_API_URL (기본 https://api.decker-ai.com)
"""
import json
import os
import sys

try:
    import requests
except ImportError:
    print("pip install requests")
    sys.exit(1)

BASE = os.getenv("DECKER_API_URL", "https://api.decker-ai.com").rstrip("/")
API = f"{BASE}/api/v1"


def get_state(symbol: str, timeframe: str = "1h") -> dict:
    r = requests.get(f"{API}/signals/{symbol}/state", params={"timeframe": timeframe}, timeout=10)
    r.raise_for_status()
    return r.json()


def get_strategy(symbol: str, timeframe: str = "1h", risk: str = "medium") -> dict:
    r = requests.get(
        f"{API}/signals/{symbol}/strategy",
        params={"timeframe": timeframe, "risk_appetite": risk},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def main():
    symbol = sys.argv[1] if len(sys.argv) > 1 else "BTCUSDT"
    print(f"=== Strategy Bot: {symbol} ===\n")

    state = get_state(symbol)
    strategy = get_strategy(symbol)

    # progress_pct, status 추출
    signals = state.get("signals", [])
    if signals:
        s0 = signals[0]
        st = s0.get("state", {})
        progress = st.get("progress_pct", 0)
        status = st.get("status", "unknown")
        print(f"Progress: {progress}% | Status: {status}")
    strat_text = strategy.get("strategy", "")
    print(f"Strategy: {strat_text}")
    print("\n→ 주문 실행: decker-ai.com 또는 Telegram @deckerclawbot")


if __name__ == "__main__":
    main()
