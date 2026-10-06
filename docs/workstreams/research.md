# Research · produce findings that survive a repeat

[Workstream index](README.md) · [Full stack](../stack.md)

**Goal:** turn a bounded question into an independently reproducible result.

Scope includes source review, hypothesis formation, experiment design,
code changes, and result analysis.
Start with narrow software questions on fixed models.
A generated report, paper, or positive review is not a verified finding.

## Fixed baseline

Choose one question about a downstream component.
Pin its experiment, metric, split, and resources before trying candidates.
Compare a scripted experiment process with an agent-assisted process.
Count all proposed candidates, failed runs, setup time, and review time.
Measure reproducible findings per total budget.
Keep positive, negative, and inconclusive results.

## Three proposed tasks

### 1. Make one claim traceable to evidence

Build a claim record that links a source, exact version,
measured quantity, tested conditions, and raw result artifact.
Use examples with missing evidence, wrong versions, and unsupported conclusions.

**Verifier:** resolve each link and compare records with locked expected labels.
**Acceptance:** every accepted measured claim links to a real artifact.
Unmeasured claims remain hypotheses.
A link check proves traceability, not scientific validity.
**Initial budget:** 30 minutes; CPU only; small local fixtures.

### 2. Bound experiment execution

Add an experiment wrapper that limits runtime, process count,
disk output, and named external calls.
Test timeout, crash, runaway output, and a successful run.
Use deterministic scripts in a disposable environment.

**Verifier:** inspect exit state, complete resource totals, and saved outputs.
**Acceptance:** each injected failure stops within the declared limits.
Partial output is saved and marked incomplete.
Worker code cannot edit the limit or verifier configuration.
**Initial budget:** 60 minutes; local CPU tests; no live model calls.

### 3. Repeat one downstream finding

Select a public claim about retrieval, memory, or inference.
Prepare a replication contract with the original conditions and any deviations.
First repeat the baseline. Then test the claimed change.

**Verifier:** a separate worker runs the pinned procedure from a clean environment.
**Acceptance:** report the measured difference and uncertainty under the fixed method.
A sound failure to reproduce can be accepted as a negative result.
Do not replace missing settings with silent guesses.
**Initial budget:** 60 minutes for contract preparation.
Experiment resources require a separate explicit allowance.

## Failure modes and dependencies

A research agent can change the metric after seeing results.
It can omit failed ideas, misread a paper, or report a planned run as complete.
Many trials can produce a winner by chance.
Record the complete trial set and confirm a selected winner on fresh data.
Depend on [evaluation](evaluation.md) for experimental decisions,
[reliability](reliability.md) for execution limits,
and [commons](commons.md) for evidence records.

Fixture checks prove bookkeeping and enforced limits.
Scientific evidence needs real runs and an independent repeat.
A narrow software finding does not establish broad research autonomy.

## Source map

- [The AI Scientist](https://github.com/SakanaAI/AI-Scientist): a research automation system, code, and example artifacts.
- [The AI Scientist paper](https://arxiv.org/abs/2408.06292): its method and reported experimental scope.

Its published templates include training workloads and GPU requirements.
They are research references, not our CPU starter environment.
Follow the [ready-task gate](README.md#turn-a-proposal-into-a-ready-task).
