# decker-client

Official Python SDK for the [Decker](https://decker-ai.com) crypto signal & narrative engine.

## Install

```bash
pip install decker-client
```

## Quickstart

```python
from decker_client import Client

client = Client(api_key="dk_live_xxx")

# Get the LLM narrative for BTCUSDT 1h
narr = client.signals.get_narrative("BTCUSDT", "1h")
print(narr.text)
# → "현재 BTCUSDT 1h 는 상승 우세..."

# Latest signal
sig = client.signals.get_latest("BTCUSDT")
print(sig.direction, sig.entry_price)

# Service health (no API key required for the underlying HTTP call)
health = client.health.check()
print(health.ok)  # True
```

## Authentication

All requests (except `health.check`) require a valid API key in the `X-API-Key` header.
Obtain your key at [decker-ai.com](https://decker-ai.com).

## Rate limits

| Tier    | Daily limit   |
|---------|--------------|
| FREE    | 100 req/day  |
| BASIC   | 10,000 req/day |
| PREMIUM | 100,000 req/day |

When the quota is exhausted, a `RateLimitError` is raised:

```python
from decker_client import RateLimitError

try:
    narr = client.signals.get_narrative("BTCUSDT", "1h")
except RateLimitError as e:
    print(f"Retry after {e.retry_after}s (resets at {e.reset})")
```

After any successful request, check `client.last_rate_limit` for current quota status:

```python
client.health.check()
rl = client.last_rate_limit
print(f"{rl.remaining}/{rl.limit} requests remaining today")
```

## Errors

| Exception        | HTTP status | Meaning                        |
|-----------------|-------------|-------------------------------|
| `AuthError`     | 401         | Invalid or revoked API key     |
| `PermissionError` | 403       | Key lacks required permissions |
| `NotFoundError` | 404         | Symbol / resource not found    |
| `RateLimitError` | 429        | Daily quota exhausted          |
| `APIError`      | 5xx         | Server error                   |

## API reference

Full OpenAPI spec: [api.decker-ai.com/docs](https://api.decker-ai.com/docs)

## License

MIT
