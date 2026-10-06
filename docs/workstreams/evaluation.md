# Evaluation · make the checker able to say no

[Workstream index](README.md) · [Full stack](../stack.md)

**Goal:** distinguish useful improvements from noise, test defects, and hidden extra cost.

Scope includes task sets, executable graders, statistical decisions,
contamination checks, and independent repeats.
Evaluation is a dependency of every other workstream.
Build the checker before asking agents to improve the score.

## Fixed baseline

Pin tasks, expected outputs, splits, grader code, and metric definitions.
Test known correct results and known failures.
Include a trivial policy that should fail.
Keep the acceptance set separate from development examples where feasible.
Record missing outputs and timeouts as failures under a stated rule.
Fix the number of trials and the decision method before testing changes.

## Three proposed tasks

### 1. Test the grader with deliberate defects

Build a small fixture suite for one grader.
Include a correct result, wrong result, empty result, malformed output,
missing task, duplicate task, and a result that imitates success text.

**Verifier:** a separate checker compares verdicts with fixed expected labels.
**Acceptance:** all locked fixtures receive the expected verdict.
The candidate must not edit the expected labels or acceptance grader.
A useful test must fail against at least one known defective grader.
**Initial budget:** 30 minutes; CPU only; no model calls.

### 2. Make run accounting complete

Add a result aggregator that preserves task IDs and every attempt.
Include failed and interrupted runs.
Calculate metrics from raw per-task outputs.

**Verifier:** recompute a small report by an independent implementation.
**Acceptance:** totals match exactly on fixed fixtures.
Missing outputs cannot disappear from the denominator.
Duplicate attempts cannot become separate solved tasks.
**Initial budget:** 45 minutes; CPU only; fixed run records.

### 3. Design a fresh acceptance set

Choose one downstream component and write tasks from a new source or time period.
Split by source or task family to reduce near-duplicate leakage.
Have a second worker label and inspect the tasks.

**Verifier:** check task executability, label agreement, and known good and bad outputs.
**Acceptance:** every task has a checked target and clear failure rule.
Document disagreements, rights, overlap checks, and remaining contamination risk.
Fresh tasks reduce leakage risk. They do not prove a model never saw similar data.
**Initial budget:** 60 minutes for a small reviewed set.
No capability claim until the fixed model actually runs it.

## Failure modes and dependencies

A judge can prefer a writing style instead of correctness.
A public test can become a training target.
A benchmark score can rise while useful outcomes fall.
A grader can accept the phrase "test passed" without running the test.
Prefer an executor or final-state check where possible.
If a model judge is needed, pin its version, prompt, and cost.
Check its errors against independently reviewed examples.

Depend on [commons](commons.md) for immutable evidence and
[tools](tools.md) for resettable environments.
Fixtures prove grader behavior on the tested cases.
Runtime evidence needs actual model outputs and per-task records.
Deployment evidence needs task diversity and drift checks beyond the initial benchmark.

## Source map

- [Language Model Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness): open task, model, and evaluation interfaces.
- [BEIR](https://github.com/beir-cellar/beir): a reference for retrieval evaluation across task types.

Reuse suitable upstream tasks and graders before creating a new framework.
Follow the [ready-task gate](README.md#turn-a-proposal-into-a-ready-task).
