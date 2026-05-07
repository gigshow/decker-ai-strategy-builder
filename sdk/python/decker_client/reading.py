"""
Reading resource.

GET /api/v1/public/reading/{symbol}/{timeframe}  — AI market reading
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from ._http import Transport


@dataclass
class ReadingResult:
    """AI-generated market reading for a symbol + timeframe."""
    symbol: str
    timeframe: str
    narrative: str              # 자연어 판독 텍스트
    stance: Optional[str]       # LONG_BIAS / SHORT_BIAS / NEUTRAL / WAIT_FOR_MTF_RESOLUTION
    preferred_direction: Optional[str]  # "+" | "-" | None
    mtf_verdict: Optional[str]  # ALIGNED / NEUTRAL / MIXED / CONFLICT
    raw: dict = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, d: dict) -> "ReadingResult":
        data = d.get("data") or d
        hint = data.get("execution_hint") or {}
        mtf = data.get("mtf_view") or {}
        return cls(
            symbol=data.get("symbol", ""),
            timeframe=data.get("primary_tf") or data.get("timeframe", ""),
            narrative=data.get("narrative") or data.get("text") or "",
            stance=hint.get("stance"),
            preferred_direction=hint.get("preferred_direction"),
            mtf_verdict=mtf.get("verdict"),
            raw=d,
        )


class ReadingResource:
    def __init__(self, transport: "Transport") -> None:
        self._t = transport

    def explain(
        self,
        symbol: str,
        timeframe: str = "4h",
        include_tfs: Optional[str] = None,
    ) -> ReadingResult:
        """
        Fetch AI-generated market reading for a symbol + timeframe.

        The engine state is synthesized into a natural-language analysis
        covering: current phase, key levels, MTF alignment, and action guidance.

        Args:
            symbol:      Trading pair, e.g. ``"BTCUSDT"``
            timeframe:   Primary timeframe, e.g. ``"4h"``
            include_tfs: Comma-separated additional TFs, e.g. ``"1h,4h,1d"``

        Example::

            reading = client.reading.explain("BTCUSDT", "4h")
            print(reading.narrative)
            print(reading.stance)        # "LONG_BIAS"
            print(reading.mtf_verdict)   # "ALIGNED"
        """
        params: dict[str, Any] = {}
        if include_tfs:
            params["include_tfs"] = include_tfs
        body = self._t.request(
            "GET",
            f"/api/v1/public/reading/{symbol}/{timeframe}",
            params=params or None,
        )
        return ReadingResult.from_dict(body)
