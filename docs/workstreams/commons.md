# Commons · make useful work easy to repeat

[Workstream index](README.md) · [Full stack](../stack.md)

**Goal:** turn spare coding-tool capacity into work that another person can check and use.

Scope includes task contracts, evidence records, run manifests,
maintainer tools, review queues, and public credit.
This overview repo is the current place for that plumbing.
A dedicated `commons` component repo remains planned.

## Fixed baseline

Use one pinned task, its starting commit, and its expected artifacts.
Try the procedure in a clean checkout.
Record setup time, manual steps, verification time,
and missing information that prevents a repeat.
Measure completed independent repeats and review effort.
Do not use PR count as a scientific progress metric.

## Three proposed tasks

### 1. Reject incomplete task contracts

Extend the task validator to check baseline pins, allowed scope,
resource limits, verifier commands, and expected outputs.
Use a valid contract and fixtures with each required part missing.

**Verifier:** run the validator against locked fixtures.
**Acceptance:** each invalid fixture fails with an actionable message.
The valid fixture still passes.
A syntax check cannot prove the commands run; the maintainer must test them.
**Initial budget:** 45 minutes; CPU only; no external services.

### 2. Make evidence packages replayable

Build a manifest checker for commands, revisions, artifact hashes,
per-task outcomes, and complete resource totals.
Include one modified artifact and one missing attempt.

**Verifier:** reconstruct a fixture report from the saved files in a clean checkout.
**Acceptance:** modified or missing artifacts are detected.
The report reproduces exactly from the complete fixture package.
Model runs can vary; their statistical rule needs a separate contract.
**Initial budget:** 45 minutes; CPU only; small local artifacts.

### 3. Track verification work separately from merge volume

Add a review record that links author, verifier, claim, evidence, and decision.
Test an accepted result, a rejected result, a useful negative result,
and a correction after merge.

**Verifier:** recompute public credit from the fixed fixture history.
**Acceptance:** only eligible merged work receives merge credit.
Verified-result credit needs the linked independent evidence and review decision.
Corrections remain visible. One patch cannot create extra credit by splitting records.
**Initial budget:** 45 minutes; CPU only; no real account writes during tests.

## Failure modes and dependencies

A file hash proves identity, not correctness.
A label can be applied without evidence.
A task can be syntactically valid and impossible to run.
A leaderboard can encourage trivial patches or hide review cost.
Keep merge credit, verified claims, and replication credit distinct.
Store rejected and inconclusive outcomes as useful project knowledge.

Depend on [evaluation](evaluation.md) for verdicts and
[research](research.md) for claim records.
A fixture proves the tool's behavior on known records.
A workflow claim needs a real independent repeat and observed review effort.
Production project tooling also needs access control, rate limits,
error handling, and a clear correction process.

## Source map

- [MLCommons Croissant](https://github.com/MLCommons/croissant): dataset metadata and provenance structures to inspect.
- [Language Model Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness): reusable task and run interfaces.

Use established formats where they fit.
Keep the local contract small enough for a contributor to read and execute.
Follow the [ready-task gate](README.md#turn-a-proposal-into-a-ready-task).
