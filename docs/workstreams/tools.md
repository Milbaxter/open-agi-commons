# Tools · check the state after the action

[Workstream index](README.md) · [Full stack](../stack.md)

**Goal:** let an agent complete useful actions within explicit permissions.

Scope includes tool schemas, adapters, browser actions, retries, and recovery.
Start in a disposable local environment.
A tool's success message is evidence to inspect, not proof of completion.

## Fixed baseline

Use one model and a fixed tool set in a resettable environment.
Give every task a known initial state and an independently checked target state.
Record allowed actions, forbidden actions, time limits, and call limits.
Measure completed tasks, invalid calls, duplicate side effects,
recovery success, and total resources.

## Three proposed tasks

### 1. Validate calls before execution

Add an adapter that checks argument types, allowed paths, and permitted operations.
Include missing fields, extra fields, path traversal, and oversized input.
Use a fake tool that records every execution.

**Verifier:** compare accepted and rejected calls with fixed expected labels.
**Acceptance:** all invalid fixtures are rejected before tool execution.
All valid fixtures reach the intended tool exactly once.
**Initial budget:** 30 minutes; CPU only; no external services.

### 2. Recover without duplicate writes

Implement one idempotent operation in a local test service.
Inject a timeout before the write and a lost response after the write.
Repeat the call with the same operation ID.

**Verifier:** inspect the service state and action log after every injected fault.
**Acceptance:** the target state contains one intended change.
Retries must not add duplicate changes.
A tool without an idempotency mechanism must return an explicit uncertain state.
**Initial budget:** 45 minutes; CPU only; disposable local state.

### 3. Verify browser task completion

Prepare a small adapter for a pinned self-hosted browser benchmark.
Choose tasks with final-state checks that do not need a language-model judge.
Test a direct agent and one recovery change.

**Verifier:** reset the environment and inspect the task's target state independently.
**Acceptance:** fix the completion gain, maximum forbidden actions,
and total call budget before dispatch.
Screenshots and transcripts alone do not establish completion.
**Initial budget:** 60 minutes for setup and checker work.
Model runs and benchmark service resources need separate limits.

## Failure modes and dependencies

A timed-out action may already have happened.
A tool can return success while the target state is wrong.
A page can contain instructions that conflict with the user's request.
A path check can fail through a symbolic link or a race.
Use execution-time access checks as well as schema checks.
Depend on [reliability](reliability.md) for authority boundaries,
[reasoning](reasoning.md) for plans, and
[evaluation](evaluation.md) for target-state checks.

A mock tool proves adapter behavior.
Runtime evidence needs the real adapter and resettable environment.
Production work also needs access controls, audit records,
cancellation, and explicit handling of uncertain side effects.

## Source map

- [BrowserGym](https://github.com/ServiceNow/BrowserGym): a research framework for browser task execution and benchmarks.
- [BrowserGym WebArena adapter](https://github.com/ServiceNow/BrowserGym/blob/main/browsergym/webarena/README.md): setup and evaluation dependencies to inspect.

Benchmark ports can differ from the original benchmark.
Some evaluations use paid model judges. Pin the checker and record its costs.
Follow the [ready-task gate](README.md#turn-a-proposal-into-a-ready-task).
