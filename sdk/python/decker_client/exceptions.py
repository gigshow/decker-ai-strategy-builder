"""
Decker client exceptions.
"""

from __future__ import annotations


class DeckerError(Exception):
    """Base exception for all decker-client errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class AuthError(DeckerError):
    """API key is missing, invalid, or revoked (HTTP 401)."""


class PermissionError(DeckerError):
    """Authenticated but not authorised for this resource (HTTP 403)."""


class RateLimitError(DeckerError):
    """Daily quota exhausted (HTTP 429).

    Attributes:
        retry_after: Seconds until the quota resets (from Retry-After header).
        reset:       Unix timestamp of the next quota window (from X-RateLimit-Reset).
        limit:       Total daily quota for this key.
    """

    def __init__(
        self,
        message: str,
        retry_after: int = 0,
        reset: int = 0,
        limit: int = 0,
    ) -> None:
        super().__init__(message, status_code=429)
        self.retry_after = retry_after
        self.reset = reset
        self.limit = limit


class APIError(DeckerError):
    """Unexpected server error (HTTP 5xx) or malformed response."""


class NotFoundError(DeckerError):
    """Requested resource does not exist (HTTP 404)."""
