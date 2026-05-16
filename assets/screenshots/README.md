# Screenshots

User-provided screenshots used in the main README. Mobile (iPhone) captures throughout.

## Naming convention

`NN_<page>_<variant>.jpg` — zero-padded order matches README embed order.

## Inventory (17 files)

| # | File | Page | Notes |
|---|---|---|---|
| 01 | `01_hero_mobile.jpg` | Main landing (mobile) | "매매는 룰이. 설명은 LLM이." + 무료시작 CTA + LIVE BTCUSDT BEAR card |
| 02 | `02_watch_dashboard.jpg` | Watch dashboard | 6 symbol grid + KRX HOLD banner |
| 03 | `03_signal_list.jpg` | Signal list | KRX banner + 6 crypto signals (BNB/BTC/DOGE/ETH/SOL/XRP) |
| 04 | `04_signal_detail.jpg` | Signal detail | ETH GO ALIGNED + SHORT 진입검토 + TF matrix + R:R 2.0× |
| 05 | `05_signal_chart.jpg` | Signal chart | ETH 1h TradingView candlestick + ENTRY/TARGET/STOP overlays |
| 06 | `06_signal_ai_reading.jpg` | Signal AI reading | MTF 정합 매도 강 · CONFIDENCE 40 · MARKET CONTEXT |
| 07 | `07_login.jpg` | Login | OwlClawMark + "시장 구조를 읽는 엔진" + Google OAuth |
| 08 | `08_signup.jpg` | Sign up | 4 input + 무료 가입 + Telegram CTA |
| 09 | `09_trade_mock_portfolio.jpg` | Trade — Mock | Portfolio $49,900 + 3 positions (BTC long / ETH short +$264) |
| 10 | `10_trade_order.jpg` | Trade — Order form | long/short toggle + BTCUSDT + 0.01 + ▲ 롱 매수 (모의) |
| 11 | `11_strategy_preset.jpg` | Strategy | ON/OFF + preset + 적용 채널 (Telegram/Web/자동주문/REST/MCP) |
| 12 | `12_review_performance.jpg` | Review | 30-day +0.13% chart + symbol breakdown + 22 trades |
| 13 | `13_krx_hot.jpg` | KRX — hot market | SK하이닉스 ADD · 삼성전자 EXIT |
| 14 | `14_krx_signals.jpg` | KRX — signals | KOSPI200 GO 109 / WATCH 4 / HOLD 94 (207 tickers) |
| 15 | `15_krx_favorites.jpg` | KRX — favorites | SK하이닉스 + 삼성전자 (local storage) |
| 16 | `16_telegram_deckerclaw.jpg` | Telegram @deckerclawbot | 6-crypto signal status briefing |
| 17 | `17_telegram_krx.jpg` | Telegram @krxdeckerbot | KRX end-of-day briefing + ADD candidates (5) |

## Spec

| Item | Value |
|---|---|
| Theme | Dark mode (Decker default) |
| Annotation | None (raw UI) |
| PII masking | Username / email / API key / real balance = dummy |
| Format | JPG (mobile captures, < 500 KB each) |
| Viewport | Mobile (iPhone 13/14, 390×844) |

## Recapture workflow (when UI changes)

1. Sign in on iPhone Safari with the **demo / dummy** account (no real balance).
2. Confirm dark mode on the device.
3. Capture each page (vol-down + power button on iPhone).
4. AirDrop to Mac → drop into this folder.
5. Rename to match the inventory above (overwrite existing file).
6. (Optional) ImageOptim / TinyPNG to keep under 500 KB.
7. Commit; README embed paths stay valid since names are stable.

## Add a new screenshot

1. Pick next `NN` (currently 17 used → start at 18).
2. Filename: `NN_<page>_<variant>.jpg` (snake_case, English).
3. Add a row to the inventory table above.
4. If used in the main README, embed via `<img src="assets/screenshots/NN_<...>.jpg" width="220" alt="..." />`.
