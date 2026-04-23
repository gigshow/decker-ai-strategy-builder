"""
Health resource — GET /api/v1/public/health
"""

from __future__ import annotations

from dataclasses import dataclass

from ._http import Transport


@dataclass
class HealthResult:
    status: str  # "ok"

    @property
    def ok(self) -> bool:
        return self.status == "ok"


class HealthResource:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def check(self) -> HealthResult:
        """Return service health. No API key required."""
        body = self._t.request("GET", "/api/v1/public/health")
        return HealthResult(status=body.get("status", "unknown"))
