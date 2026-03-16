#!/usr/bin/env python3
"""
Decker API Python Client — REST API 호출 예제

사용: python api-client-python.py [symbol]
예: python api-client-python.py BTCUSDT

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


def get_state(symbol: str) -> dict:
    """시그널 상태 조회 (progress_pct, status)"""
    r = requests.get(f"{BASE_URL}{API_PREFIX}/signals/{symbol}/state", timeout=10)
    r.raise_for_status()
    return r.json()


def get_strategy(symbol: str, timeframe: str = "1h", risk_appetite: str = "medium") -> dict:
    """진행도 기반 전략 조회 (오퍼레이션 룰북)"""
    r = requests.get(
        f"{BASE_URL}{API_PREFIX}/signals/{symbol}/strategy",
        params={"timeframe": timeframe, "risk_appetite": risk_appetite},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def push_signal(
    symbol: str,
    entry_price: float,
    target_price: float,
    stop_loss: float,
    timeframe: str = "1h",
    direction: str = "long",
) -> dict:
    """시그널 등록 (API 연동용)"""
    payload = {
        "symbol": symbol,
        "timeframe": timeframe,
        "direction": direction,
        "entry_price": entry_price,
        "target_price": target_price,
        "stop_loss": stop_loss,
    }
    r = requests.post(
        f"{BASE_URL}{API_PREFIX}/signals/push",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def get_public_signals(symbol: str, timeframe: str = "1h") -> dict:
    """공개 시그널 목록"""
    r = requests.get(
        f"{BASE_URL}{API_PREFIX}/judgment/signals/public",
        params={"symbol": symbol, "timeframe": timeframe},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def get_market_prices(symbols: list[str]) -> dict:
    """실시간 시세"""
    r = requests.get(
        f"{BASE_URL}{API_PREFIX}/market/prices",
        params={"symbols": ",".join(symbols)},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def main():
    symbol = sys.argv[1] if len(sys.argv) > 1 else "BTCUSDT"
    print(f"=== Decker API Client — {symbol} ===\n")

    try:
        print("1. State (progress_pct, status):")
        state = get_state(symbol)
        print(json.dumps(state, indent=2, ensure_ascii=False))

        print("\n2. Strategy (룰북 기반):")
        strategy = get_strategy(symbol)
        print(json.dumps(strategy, indent=2, ensure_ascii=False))

        print("\n3. Public signals:")
        signals = get_public_signals(symbol)
        print(json.dumps(signals, indent=2, ensure_ascii=False)[:500] + "...")
    except requests.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
