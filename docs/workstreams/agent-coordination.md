# Agent coordination · make delegation earn its cost

[Workstream index](README.md) · [Full stack](../stack.md)

**Goal:** improve checked outcomes through coordination under one shared budget.

This workstream studies the AI system under test.
The Commons contribution queue is a separate development process.
Scope includes task routing, handovers, shared state, and failure recovery.
More agents are useful only when the measured result justifies them.

## Fixed baseline

Build a strong single agent first.
Give it the same tools, context access, total tokens, and time allowance as the team.
Include a single agent that can use multiple sequential attempts.
Fix task splits, model revisions, and resource accounting.
Measure checked completion, coordination overhead, human help,
duplicate work, and unresolved conflicts.
Count all worker, router, critic, and judge calls.

## Three proposed tasks

### 1. Make handovers complete and bounded

Define a handover record with task ID, artifact hashes,
checked results, remaining budget, and open questions.
Test a valid handover, stale artifact, missing field, and duplicate delivery.

**Verifier:** validate records against locked fixtures and inspect receiver state.
**Acceptance:** malformed and stale handovers cannot advance the task.
Duplicate delivery does not apply the same change twice.
Every accepted record includes the shared budget balance.
**Initial budget:** 30 minutes; CPU only; no model calls.

### 2. Recover from one failed worker

Build a small task graph runner with durable state.
Inject a worker crash before and after artifact publication.
Resume from a checkpoint without resetting costs.

**Verifier:** compare final artifacts and ledgers with an uninterrupted run.
**Acceptance:** prerequisites remain enforced.
Completed work is not lost or counted twice.
A conflict produces an explicit blocked state.
**Initial budget:** 45 minutes; CPU only; deterministic worker stubs.

### 3. Test whether delegation helps

Choose tasks with separable subtasks and executable final checks.
Compare a single agent, fixed delegation, and one candidate router.
Keep total resources equal. Include tasks where delegation should add no value.

**Verifier:** repeat all policies on held-out tasks in a clean environment.
**Acceptance:** fix a completion gain and overhead limit before dispatch.
Reject a gain that depends on uncounted calls or extra human help.
Report where the single agent wins.
**Initial budget:** 60 minutes for the comparison adapter.
Live team runs need a shared call, token, and time limit.

## Failure modes and dependencies

Shared state can lose updates. Agents can repeat work.
Workers can accept unverified summaries from other workers.
A critic can agree with the author and still miss the defect.
Role separation alone does not make a check independent.
Use executable acceptance and an independent run.
Depend on [memory](memory.md) for durable state,
[commons](commons.md) for handovers, and
[evaluation](evaluation.md) for comparable outcomes.

Stub teams prove protocol mechanics.
Runtime evidence needs a fixed model and a fair single-agent comparison.
Production coordination also needs access boundaries between workers,
cancellation, state migration, and restart tests.

## Source map

- [LangGraph](https://github.com/langchain-ai/langgraph): an open orchestration project to inspect for state and execution interfaces.
- [AutoGen paper](https://www.microsoft.com/en-us/research/publication/autogen-enabling-next-gen-llm-applications-via-multi-agent-conversation-framework/): earlier research on agent coordination.

These sources identify candidate methods. They do not prove delegation helps our tasks.
Follow the [ready-task gate](README.md#turn-a-proposal-into-a-ready-task).
