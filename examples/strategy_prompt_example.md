# 전략 프롬프트 예시

---

## "이 시그널 지금 어떻게 할까?"

Telegram·Slack·웹에서 사용자가 이렇게 물으면, DECKER는 다음 흐름으로 응답합니다.

1. 사용자 컨텍스트(종목, 포지션, 리스크 선호) 수집
2. `/signals/{symbol}/state` → progress_pct, status
3. `/signals/{symbol}/strategy` → 오퍼레이션 룰북 매칭 결과
4. LLM(선택): 결과를 자연어로 다듬어 전달

---

## 예시 프롬프트

### 사용자

- "비트코인 시그널 알려줘"
- "이 시그널 지금 어떻게 할까?"
- "ETH 4시간봉 66% 됐는데 익절할까?"

### 시스템 입력 (LLM에 전달되는 컨텍스트)

```
[State]
symbol: BTCUSDT
timeframe: 4h
direction: long
progress_pct: 66
status: in_progress
entry_price: 96000
target_price: 100000
current_price: 99200

[Strategy] (RULES.yaml 매칭 결과)
"4시간봉 66% 진행. 40% 부분 익절 제안. 큰 TF는 보수적 익절."
```

### 예시 응답

"BTC 4시간봉이 목표까지 66% 진행 중입니다. 보수적 운영을 위해 40% 부분 익절을 제안드립니다. 나머지는 목표가(100,000)까지 홀드하시는 것을 권장합니다."

---

## 룰북 경로 vs LLM 경로

| 경로 | 토큰 비용 | 용도 |
|------|-----------|------|
| **룰북** | $0 | progress_pct, status 기반 전략 매칭 |
| **LLM** | 유료 | 결과 자연어 설명, 사용자 질문 답변 |

---

## 참고

- [Quick Start](../docs/quickstart.md)
- [Signal LLM 개념](../concept/signal_llm_concept.md)
- [시그널 예시](signal_example.md)
