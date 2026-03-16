# Decker 시스템 흐름

---

## 데이터 흐름 (Mermaid)

```mermaid
flowchart LR
    subgraph Data
        MarketData[실시간 시세<br/>Market Data]
        SignalSource[시그널 소스<br/>judgment_signals]
    end
    subgraph Engine
        LabelEngine[Label Engine<br/>라벨된 시그널]
        StateEngine[State Engine<br/>progress_pct, status]
        SignalEngine[Signal Engine<br/>오퍼레이션 룰북]
    end
    subgraph Output
        Web[Web]
        Telegram[Telegram]
        API[API]
    end

    MarketData --> LabelEngine
    SignalSource --> LabelEngine
    LabelEngine --> StateEngine
    StateEngine --> SignalEngine
    SignalEngine --> Web
    SignalEngine --> Telegram
    SignalEngine --> API
```

---

## 시그널 → 전략 흐름

```mermaid
sequenceDiagram
    participant User
    participant API
    participant StateEngine
    participant RULES

    User->>API: GET /signals/BTCUSDT/strategy
    API->>StateEngine: build_signal_state(signal, current_price)
    StateEngine-->>API: {progress_pct, status}
    API->>RULES: reason_signal_state(state, user_context)
    RULES-->>API: 전략 텍스트
    API-->>User: "66% 진행. 30% 부분 익절 제안."
```

---

## 파이프라인 요약

```
시계열 데이터
    → [라벨링 알고리즘] → 라벨된 시그널
    → [State Engine] → progress_pct, status
    → [오퍼레이션 룰북] → 전략
    → Web / Telegram / API
```

---

## 참고

- [Architecture](../docs/architecture.md)
- [모델·알고리즘·성과](../docs/model.md)
