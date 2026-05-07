"""
State resource.

GET /api/v1/public/state/live  — real-time engine state (CBA phase, action gate, key direction)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ._http import Transport


@dataclass
class TfStateSnapshot:
    """Per-timeframe engine state."""
    timeframe: str
    c_state: Optional[str]        # B_FORMING / A_FORMING / BREAK_PLUS / ...
    action_gate: Optional[str]    # GO / WATCH / HOLD
    key_direction: Optional[str]  # "+" | "-"
    raw: dict = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, tf: str, d: dict) -> "TfStateSnapshot":
        return cls(
            timeframe=tf,
            c_state=d.get("c_state"),
            action_gate=d.get("action_gate"),
            key_direction=d.get("key_direction"),
            raw=d,
        )


@dataclass
class StateLive:
    """Engine live state for a symbol + timeframe."""
    symbol: str
    timeframe: str
    c_state: Optional[str]
    action_gate: Optional[str]
    key_direction: Optional[str]
    key_price: Optional[float]
    current_price: Optional[float]
    mtf: Dict[str, TfStateSnapshot] = field(default_factory=dict)
    raw: dict = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, d: dict) -> "StateLive":
        data = d.get("data") or d
        primary = data.get("primary_state") or data
        mtf_raw = data.get("mtf_snapshot") or {}
        mtf = {
            tf: TfStateSnapshot.from_dict(tf, snap)
            for tf, snap in mtf_raw.items()
            if isinstance(snap, dict)
        }
        return cls(
            symbol=data.get("symbol", ""),
            timeframe=data.get("timeframe", ""),
            c_state=primary.get("c_state"),
            action_gate=primary.get("action_gate"),
            key_direction=primary.get("key_direction"),
            key_price=_float(primary.get("key_price")),
            current_price=_float(data.get("current_price")),
            mtf=mtf,
            raw=d,
        )


def _float(v: Any) -> Optional[float]:
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


class StateResource:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def get_live(
        self,
        symbol: str,
        tf: str = "4h",
        mtf: Optional[str] = None,
    ) -> StateLive:
        """
        Fetch real-time engine state for a symbol.

        Args:
            symbol: Trading pair, e.g. ``"BTCUSDT"``
            tf:     Primary timeframe, e.g. ``"4h"``
            mtf:    Comma-separated MTF list, e.g. ``"1h,4h,1d"``
                    Defaults to ``"30m,1h,4h,1d"``

        Example::

            state = client.state.get_live("BTCUSDT", tf="4h")
            print(state.action_gate)   # "GO" | "WATCH" | "HOLD"
            print(state.key_direction) # "+" | "-"
        """
        params: Dict[str, Any] = {"symbol": symbol, "tf": tf}
        if mtf:
            params["mtf"] = mtf
        body = self._t.request("GET", "/api/v1/public/state/live", params=params)
        return StateLive.from_dict(body)
