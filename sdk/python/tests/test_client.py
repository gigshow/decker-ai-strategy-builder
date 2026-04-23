"""
decker-client unit tests — respx mocks, no real network.
"""

from __future__ import annotations

import pytest
import respx
import httpx

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from decker_client import Client
from decker_client.exceptions import AuthError, RateLimitError, APIError, NotFoundError


BASE = "https://api.decker-ai.com"

# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

def test_health_check_ok():
    with respx.mock(base_url=BASE) as mock:
        mock.get("/api/v1/public/health").mock(
            return_value=httpx.Response(200, json={"status": "ok"})
        )
        client = Client(api_key="dk_live_test")
        result = client.health.check()
    assert result.ok
    assert result.status == "ok"


def test_health_check_degraded():
    with respx.mock(base_url=BASE) as mock:
        mock.get("/api/v1/public/health").mock(
            return_value=httpx.Response(200, json={"status": "degraded"})
        )
        result = Client(api_key="dk_live_test").health.check()
    assert not result.ok
    assert result.status == "degraded"


# ---------------------------------------------------------------------------
# Signals — get_latest
# ---------------------------------------------------------------------------

_LATEST_PAYLOAD = {
    "symbol": "BTCUSDT",
    "timeframe": "1h",
    "direction": "long",
    "entry_price": 65000.0,
    "target_price": 67000.0,
    "stop_loss": 64000.0,
    "generated_at": "2026-04-23T08:00:00+00:00",
}


def test_signals_get_latest():
    with respx.mock(base_url=BASE) as mock:
        mock.get("/api/v1/public/signals/BTCUSDT/latest").mock(
            return_value=httpx.Response(200, json=_LATEST_PAYLOAD)
        )
        result = Client(api_key="dk_live_test").signals.get_latest("BTCUSDT")
    assert result.symbol == "BTCUSDT"
    assert result.direction == "long"
    assert result.entry_price == 65000.0
    assert result.generated_at.year == 2026


# ---------------------------------------------------------------------------
# Signals — get_narrative
# ---------------------------------------------------------------------------

_NARRATIVE_PAYLOAD = {
    "symbol": "BTCUSDT",
    "timeframe": "1h",
    "narrative": "현재 BTCUSDT 1h 는 상승 우세...",
    "generated_at": "2026-04-23T08:00:00+00:00",
}


def test_signals_get_narrative():
    with respx.mock(base_url=BASE) as mock:
        mock.get("/api/v1/public/signals/BTCUSDT/narrative").mock(
            return_value=httpx.Response(200, json=_NARRATIVE_PAYLOAD)
        )
        result = Client(api_key="dk_live_test").signals.get_narrative("BTCUSDT", "1h")
    assert result.symbol == "BTCUSDT"
    assert result.timeframe == "1h"
    assert "상승" in result.text


def test_signals_get_narrative_passes_timeframe_param():
    with respx.mock(base_url=BASE) as mock:
        route = mock.get("/api/v1/public/signals/ETHUSDT/narrative").mock(
            return_value=httpx.Response(200, json={**_NARRATIVE_PAYLOAD, "symbol": "ETHUSDT", "timeframe": "4h"})
        )
        Client(api_key="dk_live_test").signals.get_narrative("ETHUSDT", "4h")
    assert route.called
    assert route.calls[0].request.url.params["timeframe"] == "4h"


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

def test_auth_error_on_401():
    with respx.mock(base_url=BASE) as mock:
        mock.get("/api/v1/public/health").mock(
            return_value=httpx.Response(401, json={"detail": "Invalid API key"})
        )
        with pytest.raises(AuthError) as exc_info:
            Client(api_key="dk_live_bad").health.check()
    assert exc_info.value.status_code == 401


def test_rate_limit_error_on_429():
    with respx.mock(base_url=BASE) as mock:
        mock.get("/api/v1/public/health").mock(
            return_value=httpx.Response(
                429,
                json={"detail": "rate limit exceeded"},
                headers={
                    "X-RateLimit-Limit": "100",
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": "1745452800",
                    "Retry-After": "3600",
                },
            )
        )
        with pytest.raises(RateLimitError) as exc_info:
            Client(api_key="dk_live_test").health.check()
    err = exc_info.value
    assert err.status_code == 429
    assert err.retry_after == 3600
    assert err.reset == 1745452800
    assert err.limit == 100


def test_not_found_error_on_404():
    with respx.mock(base_url=BASE) as mock:
        mock.get("/api/v1/public/signals/UNKNOWN/latest").mock(
            return_value=httpx.Response(404, json={"detail": "not found"})
        )
        with pytest.raises(NotFoundError):
            Client(api_key="dk_live_test").signals.get_latest("UNKNOWN")


def test_api_error_on_500():
    with respx.mock(base_url=BASE) as mock:
        mock.get("/api/v1/public/health").mock(
            return_value=httpx.Response(500, text="internal server error")
        )
        with pytest.raises(APIError) as exc_info:
            Client(api_key="dk_live_test").health.check()
    assert exc_info.value.status_code == 500


# ---------------------------------------------------------------------------
# Rate limit info from headers
# ---------------------------------------------------------------------------

def test_last_rate_limit_populated():
    with respx.mock(base_url=BASE) as mock:
        mock.get("/api/v1/public/health").mock(
            return_value=httpx.Response(
                200,
                json={"status": "ok"},
                headers={
                    "X-RateLimit-Limit": "10000",
                    "X-RateLimit-Remaining": "9999",
                    "X-RateLimit-Reset": "1745452800",
                },
            )
        )
        client = Client(api_key="dk_live_test")
        client.health.check()
    rl = client.last_rate_limit
    assert rl is not None
    assert rl.limit == 10_000
    assert rl.remaining == 9_999
    assert rl.reset == 1_745_452_800


# ---------------------------------------------------------------------------
# Context manager
# ---------------------------------------------------------------------------

def test_client_context_manager():
    with respx.mock(base_url=BASE) as mock:
        mock.get("/api/v1/public/health").mock(
            return_value=httpx.Response(200, json={"status": "ok"})
        )
        with Client(api_key="dk_live_test") as client:
            result = client.health.check()
    assert result.ok
