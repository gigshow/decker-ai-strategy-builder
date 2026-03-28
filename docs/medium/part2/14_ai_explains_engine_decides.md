# I Let an AI Explain My Trades — But I Didn't Let It Make Them

*Part 2, Article #14 — Decker AI Series*

*The most important architectural decision in the Decker system wasn't about algorithms. It was about which layer is allowed to make decisions — and which layer is only allowed to explain them.*

---

Everyone building AI trading systems faces the same temptation: let the LLM decide.

The reasoning seems sound. Modern language models have read millions of pages of financial analysis. They can reason about market conditions, weigh multiple factors, and produce nuanced assessments. Surely they're capable of making a call?

They are. And that's exactly the problem.

An LLM *can* make a trading call. But it cannot tell you *why* the structural conditions for that call exist. It cannot guarantee that yesterday's call used the same framework as today's. It cannot reproduce the same output given the same inputs. And it cannot be audited.

That's not a software problem. That's a fundamental property of how language models work. They reason over language — not over formally defined state machines with deterministic transition functions.

So in the Decker system, I made a hard architectural choice: **the AI explains. The engine decides.**

---

## What "Decides" Actually Means

Let me be precise about the boundary.

The engine "decides" in the sense that it deterministically produces:
1. The current structural state (where we are in the cycle)
2. The operation gate (`GO` / `WATCH` / `HOLD`)
3. The matched RULES output (strategy text + ranked action choices)
4. The label quality metrics (confidence, stability, regime consistency)

All of this happens without a language model. Inputs are OHLCV candles. The process is a finite state machine with explicit transition rules. The outputs are structured data.

These are the **ground truth** of the system. They represent what the market structure is doing, interpreted through a formally defined framework.

The AI's role begins after these outputs exist.

---

## The Consultation Layer

The consultation service takes the full signal context — including engine state, gate value, RULES output, quality metrics, and signal progress — and passes it to an LLM with a structured prompt.

The LLM then produces a **natural language explanation** of what the structured data means. Not a new analysis — an explanation of an existing analysis.

Here's the practical difference:

**Without the consultation layer**: The system outputs `gate: "WATCH", state: "B_FORMING", sub_swing: 2`. These fields are precise and correct. They're also opaque to a human who hasn't internalized the framework.

**With the consultation layer**: The system outputs all of the above, plus:

> *"The 1h BTC structural cycle is currently in its test phase — the counter-force has made a second structural attempt. The test hasn't confirmed yet. The structural gate is WATCH: conditions are developing but not resolved. Key levels to watch: the test swing low at $82,400 and the confirmation target at $85,200. A clean break above $83,800 with the next labeled sequence would trigger GO."*

Same structural data. One version is machine-readable. The other is human-readable. The AI provides the translation.

---

## The Schema Version

When the LLM receives the engine snapshot, it receives a specific **schema version** — a version number that governs what fields are in the snapshot, their types, and their semantics.

This versioning exists because the engine evolves. New fields get added. Semantics change.

The schema version in the snapshot tells the LLM: *"interpret these fields according to this schema."* A prompt template includes schema-specific instructions. If the schema version changes, the prompt template is updated to match.

The LLM sees a structured object with a schema version tag. It doesn't generate the numbers. It explains what they mean.

---

## Why This Separation Is Hard to Maintain

The temptation to blur this boundary is constant. It shows up in several forms:

**"Just ask the LLM if it's a good entry."**
The LLM's assessment of "good entry" will be based on its training data, not on the current structural state. It will give you an answer that sounds confident but isn't grounded in the formal framework. The engine's gate is grounded. The LLM's "yes" is not.

**"Have the LLM override the engine when it disagrees."**
This completely defeats the purpose of the state machine. If the LLM can override the deterministic output, the state machine's guarantees — reproducibility, auditability, formal correctness — are nullified. You've introduced a nondeterministic layer on top of a deterministic one, and the nondeterministic layer wins.

**"Let the LLM reason about the signal and provide its own gate."**
This creates two competing sources of gate values. Which one does downstream logic use? You're now deciding which layer to trust, which reintroduces all the problems you were trying to solve.

The rule is simple: **the engine's output is never overridden by the AI layer**. The AI layer can add explanation, surface context, and translate structured data into language. It cannot modify structural state.

---

## The Human in the Loop

There's a third player in this system: the human trader.

The full operational flow is:

```
Engine → RULES → Consultation (AI) → Human (or automated agent) → Execution
```

At each layer, scope of authority is specific and non-overlapping:

| Layer | Authority | Scope |
|-------|-----------|-------|
| Engine | Structural state | What the market structure is doing |
| RULES | Operational policy | What actions are valid given the state |
| AI Consultation | Explanation | How to communicate the state and policy |
| Human / Agent | Execution | Whether and how to act |

The AI consultation layer is third in a chain of four. It's important — without it, the structural analysis is opaque to most users. But it is explicitly not the decision layer.

---

## What the AI Actually Does Well Here

This role — explaining structured data in natural language — is where language models excel. It's a translation task.

The LLM isn't being asked to:
- Predict future price movement
- Evaluate whether the structural state is correct
- Override or adjust the engine's output
- Make a recommendation independent of the engine

It's being asked to:
- Translate `state: "B_FORMING"` into "the market is currently in a test phase"
- Explain what `sub_swing: 2` means in the context of the current signal
- Surface the most relevant of the RULES choices in a natural sentence
- Explain what would need to happen structurally for the gate to change from `WATCH` to `GO`

These are tasks that require natural language fluency and the ability to explain technical concepts clearly. Language models are very good at this. Put them in a role that requires formal guarantees ("will this trade be profitable"), and they fail silently.

---

## Trust, Auditability, and the Real Stakes

The consequence of a bad trading decision isn't a wrong answer in a quiz. It's money.

If a trade goes wrong, you should be able to trace:
- The engine evaluated these candles and produced state X.
- State X matched RULES condition Y, producing strategy Z.
- The consultation AI explained Z to the trader.
- The trader chose action A from the choices array.
- Action A was executed at price P.

Every step is traceable. Every step has a formal reason. The trace ID links the engine evaluation to the signal record in the database to the trade outcome.

If you let the LLM make the call at step 2, you lose this. The LLM's reasoning is not formally auditable.

For a toy project, this doesn't matter. For a system managing real positions, it matters enormously.

---

## The Broader Principle

We have a tendency to think "more AI" is always better. But AI is a tool with specific properties — good at some things, structurally unsuited to others.

Language models are excellent translators. They're unreliable formal reasoners.

The Decker architecture uses AI in the role it's suited for: translating structured formal analysis into human-readable language. And it uses a formal state machine for the role *it's* suited for: deterministically classifying structural market states.

Neither is trying to do the other's job.

**The AI is the narrator. The engine is the author. Don't confuse them.**

This is the right model for AI-assisted decision-making in any high-stakes domain — not "let the AI decide," not "don't use AI," but "use AI for translation and explanation, and use formal systems for state and policy."

---

*← [Article 13: GO, WATCH, or HOLD](13_go_watch_hold.md) · [Article 15: Two Repos, Zero Drift →](15_two_repos_zero_drift.md)*

*Try consultation live: [api.decker-ai.com/docs](https://api.decker-ai.com/docs) · Ask the bot: [@deckerclawbot](https://t.me/deckerclawbot)*
