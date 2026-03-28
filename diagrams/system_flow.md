# Decker — System Flow Diagrams

Visual overviews of the Decker engine pipeline.

---

## Full Pipeline (Phase 4: Sequence Engine)

```mermaid
flowchart LR
    subgraph Input[Input]
        OHLCV[OHLCV Candles\nRaw market data]
        SigStore[Signal Store\njudgment_signals]
    end

    subgraph Label[1. Sequence Labeler]
        Role[Candle Role\nanchor / test / signal\nconnector / wide-break]
        Quality[Label Quality\nconfidence · stability\nregime consistency]
    end

    subgraph State[2. State Machine]
        FSM[5-State FSM\nINIT → C_SET\nB_FORMING → B_SET\nW_PENDING]
        Lanes[3-Lane Tracking\nmain · sub-swing · connector]
    end

    subgraph Gate[3. Operation Gate]
        GO[GO\nCycle complete]
        WATCH[WATCH\nTest in progress]
        HOLD[HOLD\nStructural risk]
    end

    subgraph Rules[4. RULES Engine]
        YAML[RULES.yaml\n9 layers · 30+ rules\nversion-controlled]
        Choices[Strategy + Choices\nranked action options]
    end

    subgraph Consult[5. AI Consultation]
        LLM[LLM as Translator\nnot decision-maker]
        NL[Natural language\nexplanation]
    end

    subgraph Output[Output]
        Web[Web]
        TG[Telegram\n@deckerclawbot]
        API[REST API]
    end

    OHLCV --> Role
    OHLCV --> Quality
    Role --> FSM
    Quality --> FSM
    FSM --> Lanes
    Lanes --> GO
    Lanes --> WATCH
    Lanes --> HOLD
    GO --> YAML
    WATCH --> YAML
    HOLD --> YAML
    YAML --> Choices
    SigStore --> YAML
    Choices --> LLM
    LLM --> NL
    NL --> Web
    NL --> TG
    Choices --> API
```

---

## The 5-State Machine

```mermaid
stateDiagram-v2
    [*] --> INIT
    INIT --> C_SET : anchor candle
    C_SET --> B_FORMING : test begins
    C_SET --> W_PENDING : bilateral break
    B_FORMING --> B_SET : test confirmed
    B_FORMING --> C_SET : test invalidated
    B_SET --> INIT : signal confirmed (new cycle)
    B_SET --> C_SET : test invalidated
    W_PENDING --> B_FORMING : direction resolved
    W_PENDING --> C_SET : break invalidated
```

*Each transition is deterministic: same input → same output. Always.*

---

## Three Lanes (Simultaneous Tracking)

```mermaid
flowchart TD
    subgraph Main[Main Swing]
        MA[Who is winning\nthe current cycle?]
    end

    subgraph Sub[Sub-Swing Counter]
        SA[What is the opposition\nbuilding toward?]
        SC[sub_swing count\n1st attempt vs 2nd+]
    end

    subgraph Conn[Connector Phase]
        CA[Are we in a pause,\na bridge, or a trap?]
    end

    Main --> Gate[Operation Gate\nGO · WATCH · HOLD]
    Sub --> Gate
    Conn --> Gate
```

---

## Signal Lifecycle (progress_pct)

```mermaid
flowchart LR
    BIRTH[Signal birth\n0%] --> E30[Entry zone\n33%]
    E30 --> MID[Midpoint\n66%]
    MID --> NEAR[Near target\n90%]
    NEAR --> TARGET[Target\n100%]

    E30 -->|GO| ACT[Act / Enter]
    MID -->|Partial TP| TRIM[Trim position]
    NEAR -->|Pre-exit| PREP[Prepare exit]
    TARGET -->|Full exit| CLOSE[Close position]
```

---

## Target → Signal → Entry

```mermaid
flowchart TD
    TGT[Target structure confirmed] --> SIG[Signal confirmed\nSequence completed]
    SIG --> ENTRY[Entry\nExpected value + risk defined]
    ENTRY --> TRADE[Execute trade]

    NO_TGT[No target] --> INVALID[❌ Entry invalid]
    NO_SIG[No signal] --> IGNORED[❌ Movement ignored]
```

*Most systems: signal → entry (no target)*  
*Decker: target → signal → entry (target-first philosophy)*

---

## AI Layer Boundary

```mermaid
flowchart LR
    subgraph Engine[Engine Layer]
        E1[Sequence labeler]
        E2[State machine]
        E3[Operation gate]
        E4[RULES engine]
    end

    subgraph AI[AI Layer]
        A1[LLM consultation\nTranslator only]
    end

    subgraph Human[Human / Agent Layer]
        H1[Decision\nAct on choices]
    end

    Engine -- "Structural state\nGO·WATCH·HOLD\nStrategy choices" --> AI
    AI -- "Natural language\nexplanation" --> Human
    Human -- "Execute" --> Market[Market]
```

*The AI receives the engine's output and explains it. It never overrides it.*

---

## References

- [Sequence Engine concept](../concept/sequence_engine.md) — Full concept explanation
- [Architecture](../docs/architecture.md) — Module breakdown
- [Model & Performance](../docs/model.md) — Algorithm story and metrics
- [RULES.yaml](../operation_rules/RULES.yaml) — The open-source rulebook
- [Article Series Part 2](../docs/medium/part2/README.md) — Deep dives
