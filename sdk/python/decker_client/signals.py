"""
Signals resource.

GET /api/v1/public/signals/{symbol}/latest
GET /api/v1/public/signals/{symbol}/narrative
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from ._http import Transport


@dataclass
class SignalLatest:
    symbol: str
    timeframe: str
    direction: str            # "long" | "short" | "neutral"
    entry_price: float
    target_price: float
    stop_loss: float
    generated_at: datetime
    raw: dict = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, d: dict) -> "SignalLatest":
        return cls(
            symbol=d["symbol"],
            timeframe=d["timeframe"],
            direction=d.get("direction", ""),
            entry_price=float(d.get("entry_price") or 0),
            target_price=float(d.get("target_price") or 0),
            stop_loss=float(d.get("stop_loss") or 0),
            generated_at=datetime.fromisoformat(d["generated_at"].replace("Z", "+00:00")),
            raw=d,
        )


@dataclass
class NarrativeResult:
    symbol: str
    timeframe: str
    text: str
    generated_at: datetime
    raw: dict = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, d: dict) -> "NarrativeResult":
        return cls(
            symbol=d["symbol"],
            timeframe=d["timeframe"],
            text=d.get("narrative") or d.get("text") or "",
            generated_at=datetime.fromisoformat(d["generated_at"].replace("Z", "+00:00")),
            raw=d,
        )


class SignalsResource:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def get_latest(self, symbol: str) -> SignalLatest:
        """
        Fetch the most recent signal for a symbol.

        Args:
            symbol: Trading pair, e.g. ``"BTCUSDT"``
        """
        body = self._t.request("GET", f"/api/v1/public/signals/{symbol}/latest")
        return SignalLatest.from_dict(body)

    def get_narrative(self, symbol: str, timeframe: str) -> NarrativeResult:
        """
        Fetch the LLM narrative for a symbol + timeframe.

        Args:
            symbol:    Trading pair, e.g. ``"BTCUSDT"``
            timeframe: Candle interval, e.g. ``"1h"``

        Example::

            narr = client.signals.get_narrative("BTCUSDT", "1h")
            print(narr.text)
        """
        body = self._t.request(
            "GET",
            f"/api/v1/public/signals/{symbol}/narrative",
            params={"timeframe": timeframe},
        )
        return NarrativeResult.from_dict(body)
