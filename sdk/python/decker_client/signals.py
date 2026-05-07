"""
Signals resource.

GET /api/v1/public/signals/{symbol}/latest    — latest signal
GET /api/v1/public/signals/{symbol}/narrative — LLM narrative
GET /api/v1/public/signals/{symbol}/consumer  — full consumer snapshot (overlay applied)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional

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


@dataclass
class ConsumerSignal:
    """Full consumer snapshot — same data the auto-order engine consumes."""
    symbol: str
    direction: Optional[str]       # "long" | "short" | None
    decision: Optional[str]        # "ENTER" | "WAIT" | "SKIP"
    entry_price: Optional[float]
    target_t1: Optional[float]
    stop_price: Optional[float]
    risk_reward_ratio: Optional[float]
    mtf_verdict: Optional[str]     # ALIGNED / NEUTRAL / MIXED / CONFLICT
    action_gate: Optional[str]     # GO / WATCH / HOLD
    overlay_filter_pass: Optional[bool]   # None if no overlay applied
    overlay_skill_id: Optional[str]
    raw: dict = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, d: dict) -> "ConsumerSignal":
        data = d.get("data") or d
        ovl = data.get("overlay") or {}
        return cls(
            symbol=data.get("symbol", ""),
            direction=data.get("direction") or data.get("final_direction"),
            decision=data.get("decision") or data.get("final_decision"),
            entry_price=_float_or_none(data.get("entry_price")),
            target_t1=_float_or_none(data.get("target_t1")),
            stop_price=_float_or_none(data.get("stop_price")),
            risk_reward_ratio=_float_or_none(data.get("risk_reward_ratio")),
            mtf_verdict=data.get("mtf_verdict"),
            action_gate=data.get("effective_action_gate") or data.get("action_gate"),
            overlay_filter_pass=ovl.get("filter_pass"),
            overlay_skill_id=ovl.get("skill_id"),
            raw=d,
        )


def _float_or_none(v: Any) -> Optional[float]:
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


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

    def get_consumer(self, symbol: str) -> ConsumerSignal:
        """
        Fetch the full consumer snapshot — same payload the auto-order engine uses.

        Includes entry/target/stop prices, MTF verdict, action gate, and
        skill overlay metadata (``overlay_filter_pass``, ``overlay_skill_id``).

        Args:
            symbol: Trading pair, e.g. ``"BTCUSDT"``

        Example::

            sig = client.signals.get_consumer("BTCUSDT")
            if sig.action_gate == "GO" and sig.overlay_filter_pass is not False:
                print(f"Entry: {sig.entry_price}, T1: {sig.target_t1}, SL: {sig.stop_price}")
        """
        body = self._t.request("GET", f"/api/v1/public/signals/{symbol}/consumer")
        return ConsumerSignal.from_dict(body)
