# decker-client

Official Python SDK for the [Decker](https://decker-ai.com) crypto signal & narrative engine.

## Install

```bash
pip install decker-client
```

Requires Python 3.9+. For local/editable install from source:

```bash
git clone https://github.com/gigshow/decker-ai-strategy-builder.git
pip install -e decker-ai-strategy-builder/sdk/python/
```

## Get your API key

Keys are issued via Telegram:

1. Open [@deckerclawbot](https://t.me/deckerclawbot) → send `/start`
2. Send `/apikey` → receive `dk_live_xxxxxxxxxxxxxxxxxxxxxxxx`
3. Lost it? `/apikey reset` revokes and reissues

## Quickstart

```python
from decker_client import Client

with Client(api_key="dk_live_xxx") as client:
    # Latest signal
    sig = client.signals.get_latest("BTCUSDT", timeframe="1h")
    print(f"{sig.direction} | entry={sig.entry_price} | progress={sig.progress_pct}%")
    print(f"gate: {sig.operation_gate}")  # GO / WATCH / HOLD

    # Structural narrative
    narr = client.signals.get_narrative("BTCUSDT", "4h")
    print(narr.text)

    # Health check (no API key required for underlying call)
    health = client.health.check()
    print(health.ok)  # True
```

**Supported symbols**: `BTCUSDT` `ETHUSDT` `SOLUSDT` `BNBUSDT` `XRPUSDT` `DOGEUSDT`  
**Supported timeframes**: `30m` `1h` `4h` `1d`

## Authentication

All requests (except `health.check`) require a valid API key passed as `X-API-Key`.

```python
client = Client(api_key="dk_live_xxx")
# or
with Client(api_key="dk_live_xxx") as client:
    ...
```

## Rate limits

| Tier    | Daily limit    |
|---------|---------------|
| FREE    | 100 req/day   |
| BASIC   | 10,000 req/day |
| PREMIUM | 100,000 req/day |

After any request, check `client.last_rate_limit`:

```python
rl = client.last_rate_limit
print(f"{rl.remaining}/{rl.limit} requests remaining today")
print(f"Resets at: {rl.reset}")
```

When the quota is exhausted, a `RateLimitError` is raised.

## Error handling

```python
from decker_client import Client, RateLimitError, AuthError, NotFoundError

with Client(api_key="dk_live_xxx") as client:
    try:
        sig = client.signals.get_latest("BTCUSDT")
    except AuthError:
        print("Invalid or revoked key — run /apikey reset in Telegram")
    except NotFoundError:
        print("No active signal for this symbol/timeframe")
    except RateLimitError as e:
        print(f"Rate limited — retry in {e.retry_after}s")
```

| Exception         | HTTP status | Meaning                       |
|------------------|-------------|-------------------------------|
| `AuthError`      | 401         | Invalid or revoked API key    |
| `NotFoundError`  | 404         | Symbol/TF not supported       |
| `RateLimitError` | 429         | Daily quota exhausted         |
| `APIError`       | 5xx         | Server error                  |

## Local testing

Override the base URL for local development:

```python
client = Client(api_key="dk_live_xxx", base_url="http://localhost:8000")
```

## API reference

Full OpenAPI spec: [api.decker-ai.com/docs](https://api.decker-ai.com/docs)  
Developer guide: [docs/DEVELOPER_API_GUIDE.md](../docs/DEVELOPER_API_GUIDE.md)

## License

MIT
