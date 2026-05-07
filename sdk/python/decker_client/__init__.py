"""
decker-client — Official Python SDK for the Decker Public API.

Quickstart::

    from decker_client import Client

    client = Client(api_key="dk_live_xxx")
    narr = client.signals.get_narrative("BTCUSDT", "1h")
    print(narr.text)
"""

from __future__ import annotations

from ._http import DEFAULT_BASE_URL, Transport
from .exceptions import (
    APIError,
    AuthError,
    DeckerError,
    NotFoundError,
    PermissionError,
    RateLimitError,
)
from .health import HealthResource, HealthResult
from .reading import ReadingResource, ReadingResult
from .signals import ConsumerSignal, NarrativeResult, SignalLatest, SignalsResource
from .state import StateResource, StateLive, TfStateSnapshot

__version__ = "0.2.0"
__all__ = [
    "Client",
    "__version__",
    # exceptions
    "DeckerError", "AuthError", "PermissionError",
    "RateLimitError", "APIError", "NotFoundError",
    # result types
    "HealthResult", "SignalLatest", "NarrativeResult",
    "ConsumerSignal", "StateLive", "TfStateSnapshot", "ReadingResult",
]


class Client:
    """
    Decker API client.

    Args:
        api_key:  Your ``dk_live_*`` API key.
        base_url: Override the default production URL (useful for staging).
        timeout:  HTTP timeout in seconds (default 30).

    Resources:
        client.health   — :class:`~decker_client.health.HealthResource`
        client.signals  — :class:`~decker_client.signals.SignalsResource`
        client.state    — :class:`~decker_client.state.StateResource`
        client.reading  — :class:`~decker_client.reading.ReadingResource`

    Example::

        with Client(api_key="dk_live_xxx") as client:
            state = client.state.get_live("BTCUSDT", tf="4h")
            if state.action_gate == "GO":
                sig = client.signals.get_consumer("BTCUSDT")
                reading = client.reading.explain("BTCUSDT", "4h")
                print(reading.narrative)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ) -> None:
        self._transport = Transport(api_key=api_key, base_url=base_url, timeout=timeout)
        self.health = HealthResource(self._transport)
        self.signals = SignalsResource(self._transport)
        self.state = StateResource(self._transport)
        self.reading = ReadingResource(self._transport)

    @property
    def last_rate_limit(self):
        """Most recent :class:`~decker_client._http.RateLimitInfo` after any request."""
        return self._transport.last_rate_limit

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._transport.close()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *_) -> None:
        self.close()
