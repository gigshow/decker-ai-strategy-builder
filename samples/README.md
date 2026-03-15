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

## strategy-demo (예정)

Mock 전략 데모. `npm install && npm run dev`

## api-client-python (예정)

REST API 호출 예제.
