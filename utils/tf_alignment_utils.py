"""
TF Alignment Utilities — Multi-timeframe alignment calculation

Compares signal TF direction with higher TF directions to compute tf_alignment.
Feeds user_context for the operation rulebook.

Ref: docs/medium/09_multi_tf_alignment.md
"""

from typing import Any, Dict, List, Optional

# TF order (small → large)
TF_ORDER: List[str] = ["15m", "1h", "4h", "8h", "1d", "1w"]

# tf_alignment values
TF_ALIGNMENT_FULLY_ALIGNED = "fully_aligned"   # All higher TFs same direction
TF_ALIGNMENT_LOWER_ALIGNED = "lower_aligned"   # 1–2 higher TFs aligned, larger TF against
TF_ALIGNMENT_COUNTER_TREND = "counter_trend"   # Most higher TFs opposite
TF_ALIGNMENT_TRANSITION = "transition"         # Higher TF in C-swing (direction change test)
TF_ALIGNMENT_MIXED = "mixed"                  # No clear pattern


def compute_tf_alignment(
    signal_tf: str,
    signal_direction: str,
    all_tf_directions: Dict[str, str],
    transition_tfs: Optional[List[str]] = None,
) -> str:
    """
    Compute tf_alignment: signal TF vs higher TF directions.

    Args:
        signal_tf: Signal TF (e.g. "1h")
        signal_direction: Signal direction ("long" / "short")
        all_tf_directions: { "1h": "long", "4h": "short", ... }
        transition_tfs: TFs in C-swing state (returns "transition" if any higher TF)

    Returns:
        tf_alignment string
    """
    if signal_tf not in TF_ORDER:
        return TF_ALIGNMENT_MIXED

    signal_idx = TF_ORDER.index(signal_tf)

    higher_tfs = {
        tf: direction
        for tf, direction in all_tf_directions.items()
        if tf in TF_ORDER and TF_ORDER.index(tf) > signal_idx
    }

    if not higher_tfs:
        return TF_ALIGNMENT_FULLY_ALIGNED

    if transition_tfs:
        for tf in transition_tfs:
            if tf in higher_tfs:
                return TF_ALIGNMENT_TRANSITION

    aligned = sum(1 for d in higher_tfs.values() if d == signal_direction)
    total = len(higher_tfs)

    if aligned == total:
        return TF_ALIGNMENT_FULLY_ALIGNED
    elif aligned >= round(total * 0.6):
        return TF_ALIGNMENT_LOWER_ALIGNED
    elif aligned == 0:
        return TF_ALIGNMENT_COUNTER_TREND
    else:
        return TF_ALIGNMENT_MIXED


def compute_swing_context(signal: Dict[str, Any]) -> Dict[str, Any]:
    """Extract swing context from signal."""
    direction = (signal.get("direction") or "").lower()
    swing_direction = "bullish" if direction in ("long", "buy", "positive", "bullish") else "bearish"
    swing_state = (signal.get("swing_state") or "unknown").upper()
    swing_combination = (signal.get("swing_combination") or "").upper()

    return {
        "swing_state": swing_state,
        "swing_direction": swing_direction,
        "swing_combination": swing_combination,
    }


def build_tf_alignment_context(
    signal: Dict[str, Any],
    all_signals: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Single signal + all TF signals → tf_alignment context dict.

    Returns:
        { tf_alignment, swing_state, swing_direction, higher_tf_directions }
    """
    signal_tf = (signal.get("timeframe") or "").strip().lower()
    signal_direction = (signal.get("direction") or "").strip().lower()

    all_tf_directions: Dict[str, str] = {}
    transition_tfs: List[str] = []

    for s in all_signals:
        tf = (s.get("timeframe") or "").strip().lower()
        direction = (s.get("direction") or "").strip().lower()
        swing_state = (s.get("swing_state") or "").upper()
        if tf and direction:
            all_tf_directions[tf] = direction
        if swing_state == "C" and tf and tf != signal_tf:
            transition_tfs.append(tf)

    alignment = compute_tf_alignment(
        signal_tf=signal_tf,
        signal_direction=signal_direction,
        all_tf_directions=all_tf_directions,
        transition_tfs=transition_tfs if transition_tfs else None,
    )

    swing_ctx = compute_swing_context(signal)

    higher_tf_directions = {
        tf: d for tf, d in all_tf_directions.items()
        if tf in TF_ORDER and signal_tf in TF_ORDER
        and TF_ORDER.index(tf) > TF_ORDER.index(signal_tf)
    }

    return {
        "tf_alignment": alignment,
        "swing_state": swing_ctx["swing_state"],
        "swing_direction": swing_ctx["swing_direction"],
        "swing_combination": swing_ctx["swing_combination"],
        "higher_tf_directions": higher_tf_directions,
    }
