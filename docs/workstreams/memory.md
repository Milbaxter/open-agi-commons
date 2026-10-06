# Memory · keep facts with a source and a lifetime

[Workstream index](README.md) · [Full stack](../stack.md)

**Goal:** help a fixed agent use earlier information without retaining false or obsolete facts.

Scope includes memory writes, retrieval, revision, forgetting, and deletion.
Start with explicit records. Each record needs a source, time, owner,
and a rule for access and removal.
Weight updates and continual training need a separate training contract.

## Fixed baseline

Compare no persistent memory, append-only memory, and one candidate policy.
Keep the model, prompt budget, tool access, and event sequence fixed.
Reset stores before each run.
Test delayed questions, corrections, contradictions, and deletion requests.
Measure answer accuracy, stale fact use, wrong writes, retrieval cost,
and data retained after deletion.

## Three proposed tasks

### 1. Make corrections supersede old facts

Build a memory store with source IDs and explicit revision links.
Use a sequence where a setting changes twice.
Include conflicting statements from sources with different authority.

**Verifier:** query the store after each event and compare with locked expected state.
**Acceptance:** corrected facts supersede their predecessors.
Unresolved conflicts remain explicit.
The store must not silently choose an unsupported fact.
**Initial budget:** 45 minutes; CPU only; no model calls.

### 2. Check deletion across derived stores

Add deletion to one reference memory adapter.
Cover the record store, index, cached summary, and restored checkpoint.
Use unique synthetic markers as test records.

**Verifier:** inspect each named store after deletion and after restart.
**Acceptance:** the markers are absent from every store in the declared scope.
Report any excluded backup or external store as a limitation.
Do not claim universal erasure from a local test.
**Initial budget:** 45 minutes; CPU only; fixed local fixtures.

### 3. Measure useful recall under a fixed context limit

Prepare long event sequences with fresh held-out questions.
Compare append-only memory with a source-aware selection policy.
Give both the same model and total context allowance.
Include stale facts and malicious text in earlier events.

**Verifier:** replay sequences in a clean store and score final answers independently.
**Acceptance:** fix a minimum answer gain and a maximum stale fact rate in advance.
Memory write and recall calls count toward the total budget.
**Initial budget:** 60 minutes for the harness.
Live model runs need a stated call, token, and storage limit.

## Failure modes and dependencies

A summary can change meaning. An old fact can overwrite a correction.
A deleted record can return from a checkpoint.
A remembered instruction can gain authority it never had.
Depend on [retrieval](retrieval.md) for source spans,
[reliability](reliability.md) for access and instruction boundaries,
and [evaluation](evaluation.md) for sequence labels.

A store test proves state rules. It does not prove better model recall.
Real runtime evidence needs the fixed model and complete event sequence.
Production work also needs user separation, expiry, migration,
and recovery after an interrupted write.

## Source map

- [Letta](https://github.com/letta-ai/letta): an open platform for stateful agents.
- [Letta memory filesystem docs](https://github.com/letta-ai/letta-docs-md/blob/main/concepts/memfs/index.md): a concrete memory state and versioning design to inspect.

Use these to identify interfaces and testable failure cases.
They are not evidence for the proposed policies here.
Follow the [ready-task gate](README.md#turn-a-proposal-into-a-ready-task).
