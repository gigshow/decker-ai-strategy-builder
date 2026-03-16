#!/usr/bin/env python3
"""
시그널 상태 조회 기본 예제

사용: python get_signal.py [symbol] [timeframe]
예: python get_signal.py BTCUSDT 1h

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


def get_signal_state(symbol: str, timeframe: str = "1h") -> dict:
    """시그널 상태 (progress_pct, status) 조회"""
    r = requests.get(f"{API}/signals/{symbol}/state", params={"timeframe": timeframe}, timeout=10)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    symbol = sys.argv[1] if len(sys.argv) > 1 else "BTCUSDT"
    tf = sys.argv[2] if len(sys.argv) > 2 else "1h"
    data = get_signal_state(symbol, tf)
    print(json.dumps(data, indent=2, ensure_ascii=False))
