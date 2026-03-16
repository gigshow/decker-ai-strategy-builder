# Samples

**API 연동·개발자용.** 덱커는 시그널·전략을 하나로 제공합니다. 아래는 API 연동 시 참고할 예제입니다.

## signal-push-strategy (실행 가능)

API 연동 시: 시그널 등록 → 전략 조회 2단계.

```bash
chmod +x samples/signal-push-strategy.sh
./samples/signal-push-strategy.sh BTCUSDT 96000 100000 92000
```

인자: `[symbol] [entry_price] [target_price] [stop_loss]` (기본값 있음)

**예상 출력**: 1단계 200 + JSON (등록 결과), 2단계 200 + JSON (strategy 필드 포함). jq 없으면 `| jq .` 제거해도 동작. **로컬 테스트**: `DECKER_API_URL=http://localhost:8000 ./samples/signal-push-strategy.sh ...`

---

## strategy-demo.py

시그널 등록 → State → Strategy 전체 플로우 (Python).

```bash
pip install requests
python samples/strategy-demo.py BTCUSDT 96000 100000 92000
```

인자: `[symbol] [entry] [target] [stop]` (기본값: BTCUSDT 96000 100000 92000)

---

## api-client-python.py

REST API 호출 예제 (state, strategy, signals, prices).

```bash
pip install requests
python samples/api-client-python.py BTCUSDT
```

인자: `[symbol]` (기본 BTCUSDT)

---

## python/get_signal.py

시그널 상태 조회 최소 예제 (~30줄).

```bash
pip install requests
python samples/python/get_signal.py BTCUSDT 1h
```

---

## python/strategy_bot.py

시그널 → 전략 → 주문 연결 플로우 (~50줄). 주문 실행은 decker-ai.com 또는 Telegram.

```bash
pip install requests
python samples/python/strategy_bot.py BTCUSDT
```

---

## curl/examples.sh

API 빠른 테스트용 curl 모음.

```bash
chmod +x samples/curl/examples.sh
./samples/curl/examples.sh BTCUSDT
```

로컬: `DECKER_API_URL=http://localhost:8000 ./samples/curl/examples.sh`
