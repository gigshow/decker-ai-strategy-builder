"""
Internal HTTP transport layer.

Wraps httpx.Client with:
- X-API-Key header injection
- Automatic retry on transient errors (5xx, network timeout)
- X-RateLimit-* header parsing on every response
- Unified error mapping → decker_client.exceptions
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import httpx

from .exceptions import (
    APIError,
    AuthError,
    NotFoundError,
    PermissionError,
    RateLimitError,
)

DEFAULT_BASE_URL = "https://api.decker-ai.com"
DEFAULT_TIMEOUT = 30.0
_MAX_RETRIES = 3
_RETRY_STATUSES = {500, 502, 503, 504}


@dataclass
class RateLimitInfo:
    limit: int
    remaining: int
    reset: int  # unix timestamp

    @classmethod
    def from_headers(cls, headers: httpx.Headers) -> "RateLimitInfo":
        def _int(key: str) -> int:
            try:
                return int(headers.get(key, 0))
            except ValueError:
                return 0

        return cls(
            limit=_int("x-ratelimit-limit"),
            remaining=_int("x-ratelimit-remaining"),
            reset=_int("x-ratelimit-reset"),
        )


class Transport:
    """Synchronous HTTP transport used by all resource modules."""

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            headers={
                "X-API-Key": api_key,
                "Accept": "application/json",
                "User-Agent": f"decker-client/0.1.0 python-httpx/{httpx.__version__}",
            },
            timeout=timeout,
        )
        self.last_rate_limit: RateLimitInfo | None = None

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Execute request with retry; return parsed JSON body."""
        last_exc: Exception | None = None
        for attempt in range(_MAX_RETRIES):
            try:
                resp = self._client.request(method, path, params=params, json=json)
                self.last_rate_limit = RateLimitInfo.from_headers(resp.headers)
                return self._handle(resp)
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_exc = exc
                if attempt < _MAX_RETRIES - 1:
                    time.sleep(2**attempt)

        raise APIError(f"Request failed after {_MAX_RETRIES} attempts: {last_exc}")

    def _handle(self, resp: httpx.Response) -> Any:
        sc = resp.status_code
        if sc == 401:
            raise AuthError("Invalid or revoked API key", status_code=401)
        if sc == 403:
            raise PermissionError("Access denied", status_code=403)
        if sc == 404:
            raise NotFoundError("Resource not found", status_code=404)
        if sc == 429:
            headers = resp.headers
            retry_after = int(headers.get("retry-after", 0))
            reset = int(headers.get("x-ratelimit-reset", 0))
            limit = int(headers.get("x-ratelimit-limit", 0))
            raise RateLimitError(
                "Daily API quota exceeded",
                retry_after=retry_after,
                reset=reset,
                limit=limit,
            )
        if sc >= 500:
            raise APIError(f"Server error {sc}: {resp.text[:200]}", status_code=sc)
        if sc >= 400:
            raise APIError(f"Client error {sc}: {resp.text[:200]}", status_code=sc)
        return resp.json()

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "Transport":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()
