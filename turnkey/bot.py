#!/usr/bin/env python3
"""
DeckerClaw Turnkey — 경량 Telegram 봇

시그널·전략 조회만 지원. DB 없음. Decker API 호출만.
환경변수: DECKER_API_URL, TELEGRAM_BOT_TOKEN

사용 예: "비트코인 시그널", "ETH 시세", "BTC 전략 알려줘"
"""
import logging
import os
import re

import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BASE = os.getenv("DECKER_API_URL", "https://api.decker-ai.com").rstrip("/")
API = f"{BASE}/api/v1"

# 키워드 → 심볼 매핑
SYMBOL_MAP = {
    "비트코인": "BTCUSDT",
    "btc": "BTCUSDT",
    "비티씨": "BTCUSDT",
    "이더리움": "ETHUSDT",
    "eth": "ETHUSDT",
    "이더": "ETHUSDT",
    "솔라나": "SOLUSDT",
    "sol": "SOLUSDT",
    "솔": "SOLUSDT",
    "도지": "DOGEUSDT",
    "doge": "DOGEUSDT",
    "리플": "XRPUSDT",
    "xrp": "XRPUSDT",
}


def extract_symbol(text: str) -> str | None:
    """메시지에서 종목 추출. 없으면 None."""
    text_lower = text.lower().strip()
    for kw, sym in SYMBOL_MAP.items():
        if kw.lower() in text_lower:
            return sym
    # USDT 패턴 (BTCUSDT, ETHUSDT 등)
    m = re.search(r"\b([A-Za-z]{2,10})USDT\b", text, re.I)
    if m:
        return m.group(0).upper()
    return None


def get_state(symbol: str, timeframe: str = "1h") -> dict | None:
    try:
        r = requests.get(
            f"{API}/signals/{symbol}/state",
            params={"timeframe": timeframe},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.warning("get_state %s: %s", symbol, e)
        return None


def get_strategy(symbol: str, timeframe: str = "1h", risk: str = "medium") -> dict | None:
    try:
        r = requests.get(
            f"{API}/signals/{symbol}/strategy",
            params={"timeframe": timeframe, "risk_appetite": risk},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.warning("get_strategy %s: %s", symbol, e)
        return None


def format_response(state: dict | None, strategy: dict | None, symbol: str) -> str:
    """API 응답을 사용자용 텍스트로 변환."""
    if not state and not strategy:
        return f"❌ {symbol} 시그널·전략을 불러오지 못했어요. API URL을 확인해 주세요."

    parts = []
    if state:
        signals = state.get("signals", [])
        if signals:
            s0 = signals[0]
            st = s0.get("state", {})
            progress = st.get("progress_pct", 0)
            status = st.get("status", "unknown")
            parts.append(f"📊 {symbol} 진행도: {progress}% | 상태: {status}")
        else:
            parts.append(f"📊 {symbol} — 공개 시그널 없음 (시그널 등록 후 조회 가능)")

    if strategy:
        strat_text = strategy.get("strategy", "")
        if strat_text:
            parts.append(f"📌 전략: {strat_text}")

    if not parts:
        return f"📊 {symbol} — 데이터 없음"
    return "\n".join(parts)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "DeckerClaw 턴키에 오신 것을 환영해요! 🦞\n\n"
        "예: \"비트코인 시그널\", \"ETH 전략 알려줘\"\n"
        "→ Decker API로 시그널·전략을 조회해 드려요.\n\n"
        "주문·포지션은 decker-ai.com 또는 @deckerclawbot에서 이용해 주세요."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text or ""
    symbol = extract_symbol(text)

    if not symbol:
        # 시그널/전략/시세 키워드 없으면 도움말
        if any(k in text for k in ["시그널", "전략", "시세", "얼마", "signal", "strategy"]):
            await update.message.reply_text(
                "종목을 알려주세요. 예: \"비트코인 시그널\", \"ETH 전략\""
            )
        return

    state = get_state(symbol)
    strategy = get_strategy(symbol)
    msg = format_response(state, strategy, symbol)
    await update.message.reply_text(msg[:4000])  # Telegram 4096 제한


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN 환경변수가 필요해요.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("DeckerClaw Turnkey 시작. API: %s", BASE)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
