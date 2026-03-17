#!/usr/bin/env python3
"""
턴키 API 연동 검증 — Telegram 토큰 없이 state/strategy 호출 테스트

사용: python verify_api.py
"""
import os
import sys

import requests

BASE = os.getenv("DECKER_API_URL", "https://api.decker-ai.com").rstrip("/")
API = f"{BASE}/api/v1"


def main() -> int:
    print(f"API: {API}")
    print("Testing /signals/BTCUSDT/state ...")
    state = requests.get(f"{API}/signals/BTCUSDT/state", params={"timeframe": "1h"}, timeout=10)
    print("Testing /signals/BTCUSDT/strategy ...")
    strategy = requests.get(
        f"{API}/signals/BTCUSDT/strategy",
        params={"timeframe": "1h", "risk_appetite": "medium"},
        timeout=10,
    )

    if state.status_code != 200 or strategy.status_code != 200:
        print(f"FAIL: state={state.status_code} strategy={strategy.status_code}")
        return 1

    s = state.json()
    sigs = s.get("signals", [])
    if sigs:
        st = sigs[0].get("state", {})
        print(f"  progress_pct: {st.get('progress_pct')} status: {st.get('status')}")
    strat = strategy.json()
    txt = strat.get("strategy") or ""
    print(f"  strategy: {(txt[:80] + '...') if len(txt) > 80 else txt or 'N/A'}")

    print("OK: API 연동 정상. 턴키 봇은 TELEGRAM_BOT_TOKEN 설정 후 python bot.py 실행.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
