# Two Repos, One Engine, Zero Drift — How We Version a Trading Algorithm

*Part 2, Article #15 — Decker AI Series*

*Every production trading system eventually faces the same invisible problem: the code that ran the backtest is no longer the code running live. Here's how we built the infrastructure to prevent that.*

---

There's a class of bugs that only show up in production. They're not logic errors. They're not race conditions. They're **version drift** — the slow divergence between what you tested and what you're running.

In most software systems, this is annoying. In a trading system, it can be expensive.

Consider: your backtest used an earlier engine version. The live system is running a newer one. Somewhere between those versions, the labeling behavior for a specific candle sequence changed. The backtested signal looks different from the live signal. The entry that worked in backtest fires at a different price in production. Or doesn't fire at all.

This is the drift problem. And it's particularly acute for an engine that lives in two places simultaneously.

---

## Two Repositories, One Algorithm

The Decker engine exists in two locations:

1. **Private monorepo** — alongside the API, database migrations, frontend, and operational tooling. All development happens here.
2. **Public repository** (`decker-ai`) — open-source documentation, samples, concepts, and the RULES.yaml rulebook.

Both must present a consistent view of the engine's capabilities. Any drift between them means external users are working with an outdated picture.

---

## The Sync Architecture

Here's how it works.

The monorepo is the **single source of truth**. When changes are merged to `main`, a sync pipeline runs:

**Step 1 — Overlay**: The current engine source is overlaid onto a local clone of the public repository.

**Step 2 — Selective document copy**: A manifest defines which documentation files get copied to the public repo and which stay private. Platform-specific roadmaps, database migrations, and business strategy documents stay private. Conceptual docs, the RULES.yaml, and architecture documentation move to the public repo.

**Step 3 — Push**: The synced clone is pushed to the public repo's `main` branch.

**Step 4 — Log**: A sync log records the commit SHA pairs — private repo and public repo — creating a traceable history.

**Step 5 — Verification**: A manifest verification script confirms that all version identifiers are consistent before any CI gate passes.

```bash
# Running the verify script produces:
Engine version:    0.11.2
Schema version:    1.2.0  
RULES version:     2.3.5 (2026-03-28)
Private HEAD:      453ac315
Public HEAD:       020450fd
Status:            CONSISTENT ✓
```

The SHA pair is the atomic record of sync state. If the public repo HEAD doesn't match expectations, drift has occurred and the gate fails.

---

## The Sync Manifest

The manifest defines what moves and what doesn't. This is a non-trivial boundary.

**Goes to the public repo:**
- Engine source code
- RULES.yaml rulebook
- Conceptual documentation (labeling guide, architecture, algorithm concepts)
- Test fixtures and golden datasets
- The signal state merge documentation

**Stays private:**
- Platform-specific roadmaps
- Database migration files
- Business strategy documents
- Production API configurations

The key policy: *"Prevents double truth."* If a document exists in both repos, it will eventually diverge. The manifest prevents this by making the boundary explicit — platform docs are platform truth, engine docs are engine truth.

---

## Versioning Three Things Simultaneously

The engine has three independent version axes, all of which need tracking:

**Engine version** — The software version of the engine package. Increments when algorithm behavior changes.

**Schema version** — The version of the output schema. A schema change (adding a new field) is a breaking change for consumers even if the algorithm logic is identical. Consumers check this field and handle breaking changes explicitly.

**RULES version** — The version of the operation rulebook. RULES can be updated without touching the engine code — a policy change, not an algorithm change.

When these three versions are logged together, any signal can be fully reproduced:

```
Engine: 0.11.2 / Schema: 1.2.0 / RULES: 2.3.5
```

You know exactly which algorithm evaluated the candles, which schema version structured the output, and which rules produced the operational recommendation.

This is the foundation of backtestability: not just knowing what price data was used, but knowing the exact version of every layer of the analysis stack.

---

## The Sync Log as Audit Trail

The sync log might look like simple record-keeping. In practice it's a temporal audit trail:

| Date | Public Repo Commit | Private Commit | What Changed |
|------|--------------------|----------------|--------------|
| 2026-03-28 | 020450f | 453ac315 | RULES 2.3.5, sub-swing columns, signal-state merge doc |
| 2026-03-28 | e63acd6 | 1b5328d9 | Governance documents, sync policy |
| 2026-03-28 | e58289d | a7890688 | SEQ_V2 sequence reanchor, label invariants |

Given a signal in the production database with a timestamp of `2026-03-28 14:32:00 UTC`, you can use the log to determine:
- Which private commit was live at that timestamp
- Which public repo commit that corresponds to
- Which RULES version was active
- Which schema version the output used

The trace ID system connects it all: a unique identifier on every signal evaluation links the signal to a specific point in the engine's version history. Any outcome — whether the trade profited, how it was scored in the performance analytics — can be correlated back to the exact algorithmic configuration that produced it.

---

## The CI Gate

The manifest integrates with CI through a verification script:

```python
# CI checks that all version identifiers are consistent
assert manifest["rules_version"] == expected_rules_version
assert manifest["schema_version"] == expected_schema_version  
assert manifest["git_head"] == current_git_head()
```

If any version identifier drifts out of alignment, the CI gate fails. This catches the case where someone bumped the RULES version without updating the manifest, or updated the schema version in code without reflecting it in docs.

The gate runs on every PR to `main`. It's the last line of defense against configuration drift.

---

## Why This Matters at Scale

A sync infrastructure might seem like over-engineering for a two-repo setup. But it embodies a principle that applies to any system where algorithm correctness is critical: **every version must be traceable, and traceability must be automated**.

Manual version tracking fails. People forget to update logs. Commits happen in the wrong order. "I think it was version 0.11" is not an audit trail.

The trace ID + sync log + manifest combination creates a chain where:
- Every signal has a trace ID
- Every trace ID links to a private commit
- Every private commit maps to a public commit via the sync log
- Every commit has a manifest record of all version identifiers

The chain is complete. Any point in the system's history can be reconstructed.

---

## Closing the Series

This series has covered the full Decker engine stack from bottom to top:

- **Labeling grammar** (Article #11): Candles as sequence tokens with formal grammatical rules
- **State machine** (Article #12): Five deterministic states tracking structural position
- **Operation gate** (Article #13): Ternary GO/WATCH/HOLD with 9-layer RULES evaluation
- **AI consultation** (Article #14): Language model as translator, not decision-maker
- **Sync infrastructure** (this article): Version tracking as the foundation of reproducibility

None of these layers is independently sufficient. A state machine without an audit trail is still opaque at scale. A consultation AI without a formal engine is just a chatbot with financial pretensions. A version log without a formal state machine is just documentation theater.

Together, they form a system where every part has a purpose, every boundary is explicit, and every output can be traced to a formal cause.

That's the engineering goal. Everything else is implementation detail.

---

*The full RULES.yaml rulebook is open-source: [operation_rules/RULES.yaml](../../../operation_rules/RULES.yaml)*  
*Try the engine live: [api.decker-ai.com/docs](https://api.decker-ai.com/docs)*  
*GitHub: [decker-ai](https://github.com/gigshow/decker-ai)*

*← [Article 14: AI Explains, Engine Decides](14_ai_explains_engine_decides.md) · [Back to Series Index →](README.md)*
