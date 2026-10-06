# Reliability · keep useful work inside the boundary

[Workstream index](README.md) · [Full stack](../stack.md)

**Goal:** reduce specific failures while retaining useful task completion.

Scope includes prompt injection, tool permissions, uncertain actions,
resource limits, recovery, and explicit operating constraints.
Each task must name the failure it tests and the boundary it enforces.
A general claim that a system is safe is too broad for one task.

## Fixed baseline

Pin the agent, tools, permissions, environment, and test cases.
Pair normal tasks with fault or attack variants.
Define success from final state and action logs.
Measure normal task completion, attack success, forbidden actions,
and failures caused by the defense.
Keep the same total call and token allowances for all variants.

## Three proposed tasks

### 1. Keep document instructions below user authority

Prepare retrieved documents with quoted instructions and injected commands.
The user task stays fixed.
Add one boundary that treats document text as evidence, not tool authority.

**Verifier:** inspect attempted and completed tool actions in a resettable environment.
**Acceptance:** fix an attack-success reduction and a normal-task completion floor in advance.
New attack variants must remain outside the contributor's development set.
Do not claim broad injection resistance from a fixture result.
**Initial budget:** 45 minutes for attack fixtures and the adapter.
Live model tests need a separate call limit.

### 2. Check permissions at execution time

Add one tool permission boundary to a local adapter.
Test allowed paths, forbidden paths, changed permissions,
symbolic links, and a restart with stale cached state.

**Verifier:** inspect the filesystem or service state after each attempted action.
**Acceptance:** all known forbidden actions have no protected-state side effect.
All valid controls still complete.
Test execution-time checks, not only argument validation.
**Initial budget:** 45 minutes; CPU only; synthetic local data.

### 3. Make uncertain completion explicit

Add a result type for a tool action whose response was lost.
Test confirmed success, confirmed failure, and uncertain completion.
Require reconciliation before another non-idempotent action.

**Verifier:** inject each fault and inspect subsequent calls and final state.
**Acceptance:** the agent cannot report an uncertain action as confirmed success.
It cannot repeat a non-idempotent action without the defined reconciliation step.
**Initial budget:** 30 minutes; CPU only; deterministic fake service.

## Failure modes and dependencies

A defense can stop all work and appear secure.
A prompt instruction can fail even when it sounds strict.
A permission check can run before a path or account changes.
A recovery action can duplicate the original side effect.
Use paired normal controls and inspect actual state.
Depend on [tools](tools.md) for action semantics,
[memory](memory.md) for stored instructions,
and [evaluation](evaluation.md) for fresh fault cases.

A fixture can prove a permission rule in a named adapter.
It cannot prove model behavior against unknown attacks.
Runtime evidence needs the real model and attack suite.
Production work also needs independent access control,
audit records, and tested recovery procedures.

## Source map

- [AgentDojo](https://github.com/ethz-spylab/agentdojo): an open benchmark for prompt injection attacks and defenses in agent tasks.
- [BrowserGym](https://github.com/ServiceNow/BrowserGym): resettable browser task interfaces for tested action outcomes.

These environments support bounded tests. They do not certify general safety.
Follow the [ready-task gate](README.md#turn-a-proposal-into-a-ready-task).
