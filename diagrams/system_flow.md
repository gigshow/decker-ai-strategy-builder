# Decker 시스템 흐름

---

## 전체 파이프라인

```mermaid
flowchart LR
    subgraph Input[입력]
        MarketData[실시간 시세<br/>Market Data]
        SignalSource[시그널 소스<br/>judgment_signals]
    end

    subgraph Core[핵심 엔진]
        LabelAlgo[Labeling Algorithm<br/>오브젝트 평가<br/>S / T / 1 라벨]
        StateEngine[State Engine<br/>progress_pct<br/>status]
    end

    subgraph Strategy[전략]
        OpRules[Operation Rules<br/>RULES.yaml<br/>35개+ 규칙]
    end

    subgraph Output[출력]
        Web[Web]
        Telegram[Telegram]
        API[API]
    end

    MarketData --> LabelAlgo
    SignalSource --> LabelAlgo
    LabelAlgo --> StateEngine
    StateEngine --> OpRules
    OpRules --> Web
    OpRules --> Telegram
    OpRules --> API
```

---

## 라벨링 → 시그널 발생 흐름

```mermaid
flowchart TD
    TS[시계열 데이터] --> OD[Object 식별<br/>고점/저점/유동성]
    OD --> PE[Prime 평가<br/>1/2 → 1/2']
    PE --> SC[Swing 분류<br/>A / B / C]
    SC --> SW[Swing 조합 계산<br/>AB, AC, BB, BC]
    SW --> BK{2프라임<br/>브레이크?}
    BK -->|Yes| SIG[시그널 S 발생]
    BK -->|No| WAIT[대기]
    SIG --> SE[State Engine<br/>progress_pct 계산]
```

---

## 시그널 → 전략 시퀀스

```mermaid
sequenceDiagram
    participant User
    participant API
    participant StateEngine
    participant RULES

    User->>API: GET /signals/BTCUSDT/strategy
    API->>StateEngine: build_signal_state(signal, current_price)
    StateEngine-->>API: {progress_pct: 66, status: "in_progress"}
    API->>RULES: reason_signal_state(state, user_context)
    RULES-->>API: 전략 텍스트
    API-->>User: "66% 진행. 30% 부분 익절 제안."
```

---

## Trade Flow

```mermaid
flowchart LR
    A[A State Swing] --> T[T Signal Touch]
    T --> TGT[Target 정의<br/>+7%]
    TGT --> ENTRY[Entry 트리거]
    ENTRY --> EXEC[Target 실행]
    EXEC --> EXIT{Exit}
    EXIT -->|Target 도달| CLOSE[포지션 청산]
    EXIT -->|Reverse 시그널| REV[Reverse 진입]
```

---

## Target → Signal → Entry 원칙

```mermaid
flowchart TD
    TARGET[Target 구조 확인] --> SIGNAL[Signal 확인<br/>2프라임 브레이크]
    SIGNAL --> ENTRY[Entry<br/>기대값 + 리스크 정의 완료]
    ENTRY --> TRADE[거래 실행]

    NO_TARGET[Target 없음] --> INVALID[❌ Invalid Entry]
    NO_SIGNAL[Signal 없음] --> IGNORED[❌ Movement Ignored]
```

---

## 참고

- [Architecture](../docs/architecture.md) — 파이프라인·모듈
- [모델·알고리즘·성과](../docs/model.md) — 성과 지표
- [라벨링 알고리즘](../concept/labeling_algorithm.md) — 오브젝트·스윙
- [Strategy DSL](../docs/strategy-dsl.md) — 사용자 정의 전략
