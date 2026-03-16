#!/usr/bin/env python3
"""
Strategy Demo — 시그널 등록 → State → Strategy 전체 플로우

Signal → State Engine → Operation Rules 매칭을 한 번에 실행합니다.

사용: python strategy-demo.py [symbol] [entry] [target] [stop]
예: python strategy-demo.py BTCUSDT 96000 100000 92000

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

BASE_URL = os.getenv("DECKER_API_URL", "https://api.decker-ai.com").rstrip("/")
API_PREFIX = "/api/v1"


def main():
    symbol = sys.argv[1] if len(sys.argv) > 1 else "BTCUSDT"
    entry = float(sys.argv[2]) if len(sys.argv) > 2 else 96000.0
    target = float(sys.argv[3]) if len(sys.argv) > 3 else 100000.0
    stop = float(sys.argv[4]) if len(sys.argv) > 4 else 92000.0

    print("=== Strategy Demo: Signal → State → Strategy ===\n")
    print(f"Symbol: {symbol} | Entry: {entry} | Target: {target} | Stop: {stop}\n")

    try:
        # 1. 시그널 등록
        print("1. Push signal...")
        payload = {
            "symbol": symbol,
            "timeframe": "1h",
            "direction": "long",
            "entry_price": entry,
            "target_price": target,
            "stop_loss": stop,
        }
        r = requests.post(
            f"{BASE_URL}{API_PREFIX}/signals/push",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        r.raise_for_status()
        push_result = r.json()
        print(f"   → {json.dumps(push_result, ensure_ascii=False)}\n")

        # 2. State 조회 (progress_pct, status)
        print("2. Get state (progress_pct, status)...")
        r = requests.get(f"{BASE_URL}{API_PREFIX}/signals/{symbol}/state", timeout=10)
        r.raise_for_status()
        state = r.json()
        print(f"   → {json.dumps(state, indent=2, ensure_ascii=False)}\n")

        # 3. Strategy 조회 (룰북 매칭)
        print("3. Get strategy (Operation Rules)...")
        r = requests.get(
            f"{BASE_URL}{API_PREFIX}/signals/{symbol}/strategy",
            params={"timeframe": "1h", "risk_appetite": "medium"},
            timeout=10,
        )
        r.raise_for_status()
        strategy = r.json()
        print(f"   → {json.dumps(strategy, indent=2, ensure_ascii=False)}\n")

        print("=== Done ===")
    except requests.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
