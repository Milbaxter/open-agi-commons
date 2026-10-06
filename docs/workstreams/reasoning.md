# Reasoning · turn plans into checked results

[Workstream index](README.md) · [Full stack](../stack.md)

**Goal:** solve more tasks within a fixed total search budget.

Scope includes planning, search, program synthesis, and proof search.
A fluent explanation is not the verifier.
Use execution, final-state tests, or a proof checker where possible.

## Fixed baseline

Use one model with a direct attempt and a strong repeated-attempt baseline.
Give the candidate the same total token, tool, and time allowances.
Fix task splits, prompts, sampling settings, and attempt count.
Report solved tasks, total attempts, verifier cost, and timeouts.
Keep all candidates, including discarded ones.

## Three proposed tasks

### 1. Enforce a search budget across branches

Build a shared ledger for a planner with multiple search branches.
Test a successful branch, repeated failure, cancellation, and a resumed run.
Use a deterministic model stub first.

**Verifier:** inspect the complete event ledger and inject boundary failures.
**Acceptance:** every branch consumes the same fixed allowance.
No branch can reset the budget by restarting.
Exhaustion returns the best checked partial result or a clear failure.
**Initial budget:** 45 minutes; CPU only; no model calls.

### 2. Check plans against executable state

Prepare one small planning domain with known state transitions.
Make the checker execute a proposed plan from a fixed initial state.
Include impossible actions and plans that reach the wrong goal.

**Verifier:** a separately written executor computes the final state.
**Acceptance:** all locked valid plans pass and all locked invalid plans fail.
Reject the right verbal answer if its action sequence cannot produce it.
**Initial budget:** 45 minutes; CPU only; fixed finite fixtures.
This checks the harness, not general planning ability.

### 3. Compare search policies on checked tasks

Choose one pinned code-task set or Lean theorem set.
Compare direct attempts, repeated sampling, and one search policy.
Keep total generation and verifier budgets equal.

**Verifier:** run held-out unit tests or the pinned Lean checker in a fresh environment.
For proofs, reject admitted results and record the allowed axioms.
**Acceptance:** fix the solved-task gain and regression bounds in advance.
Every attempt counts. A claimed proof must pass the actual checker.
**Initial budget:** 60 minutes for the adapter.
Live search needs a separate model and execution budget.

## Failure modes and dependencies

Search can exploit an incomplete test suite.
A proof can pass after changing its statement or permitted axioms.
A planner can hide failed attempts or use a more capable model.
Lock the task, verifier, model, and resource rules.
Depend on [tools](tools.md) for bounded execution,
[evaluation](evaluation.md) for hold-outs, and
[inference](inference.md) for generation accounting.

Toy domains prove state and budget mechanics.
Runtime evidence needs the real model and executable held-out tasks.
A claim covers only the tested domain and model.
Production planning also needs recovery from partial actions and changed observations.

## Source map

- [LeanDojo](https://github.com/lean-dojo/LeanDojo): programmatic interaction with Lean and benchmark tooling.
- [LeanDojo paper](https://arxiv.org/abs/2306.15626): retrieval-assisted theorem proving and evaluation design.

Pin the theorem statements, toolchain, libraries, and split.
Follow the [ready-task gate](README.md#turn-a-proposal-into-a-ready-task).
